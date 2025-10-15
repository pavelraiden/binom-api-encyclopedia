#!/usr/bin/env python3
"""
Умный скрипт замены офферов с автоматическим маппингом по номерам и пересчетом весов

Особенности:
- Автоматический маппинг офферов по номерам (#1, #2, #3)
- Автоматический пересчет весов на равные доли
- Поддержка множественных трекеров Binom
- Сохранение всех настроек кампаний
"""

import json
import re
import os
import sys
from pathlib import Path

# Добавляем путь к core модулям
sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))

from binom_api import BinomAPI
from transform_campaign_data import transform_campaign_for_update


def extract_offer_number(offer_name):
    """
    Извлечь номер оффера из названия (#1, #2, #3)
    
    Returns:
        int или None
    """
    match = re.search(r'#(\d+)', offer_name)
    return int(match.group(1)) if match else None


def create_smart_mapping(api, old_offer_pattern, new_offer_pattern):
    """
    Создать умный маппинг офферов по номерам
    
    Args:
        api: экземпляр BinomAPI
        old_offer_pattern: паттерн старых офферов (например, "Memorra")
        new_offer_pattern: паттерн новых офферов (например, "Cleanserra")
    
    Returns:
        dict: {old_id: new_id} с учетом номеров
    """
    print(f"\n🔍 Поиск офферов...")
    print(f"   Старые: содержат '{old_offer_pattern}'")
    print(f"   Новые: содержат '{new_offer_pattern}'")
    
    offers = api.get_offers(date_preset="all_time", limit=1000)
    
    old_offers = {}
    new_offers = {}
    
    for offer in offers:
        name = offer.get('name', '')
        offer_id = offer.get('id')
        
        if old_offer_pattern.lower() in name.lower():
            number = extract_offer_number(name)
            if number:
                old_offers[number] = {'id': offer_id, 'name': name}
                print(f"   Найден старый оффер #{number}: ID {offer_id}")
        
        if new_offer_pattern.lower() in name.lower():
            number = extract_offer_number(name)
            if number:
                new_offers[number] = {'id': offer_id, 'name': name}
                print(f"   Найден новый оффер #{number}: ID {offer_id}")
    
    # Создаем маппинг по номерам
    mapping = {}
    for number in old_offers:
        if number in new_offers:
            old_id = old_offers[number]['id']
            new_id = new_offers[number]['id']
            mapping[old_id] = new_id
            print(f"   ✅ Маппинг #{number}: {old_id} → {new_id}")
        else:
            print(f"   ⚠️  Для старого оффера #{number} не найден новый")
    
    return mapping


def recalculate_weights(offers):
    """
    Пересчитать веса офферов на равные доли
    
    Args:
        offers: список офферов
    
    Returns:
        список офферов с обновленными весами
    """
    if not offers:
        return offers
    
    total_offers = len(offers)
    base_weight = 100 // total_offers
    remainder = 100 % total_offers
    
    for i, offer in enumerate(offers):
        # Последнему офферу добавляем остаток
        if i == total_offers - 1:
            offer['weight'] = base_weight + remainder
        else:
            offer['weight'] = base_weight
    
    return offers


def find_and_replace_offers_smart(paths, replacement_map, recalc_weights=True, verbose=False):
    """
    Умная замена офферов с пересчетом весов
    
    Args:
        paths: список путей
        replacement_map: словарь замены {old_id: new_id}
        recalc_weights: пересчитывать ли веса
        verbose: выводить детали
    
    Returns:
        (modified_paths, found_count, replaced_count, details)
    """
    if not paths:
        return paths, 0, 0, []
    
    found_count = 0
    replaced_count = 0
    details = []
    
    for path in paths:
        if not isinstance(path, dict):
            continue
        
        path_name = path.get('name', 'unnamed')
        offers = path.get('offers', [])
        
        # Флаг - были ли замены в этом path
        path_modified = False
        
        for offer in offers:
            offer_id = offer.get('offerId')
            
            if offer_id in replacement_map:
                old_id = offer_id
                new_id = replacement_map[offer_id]
                
                # Заменяем ID
                offer['offerId'] = new_id
                
                found_count += 1
                replaced_count += 1
                path_modified = True
                
                detail = {
                    'path': path_name,
                    'old_offer_id': old_id,
                    'new_offer_id': new_id,
                    'offer_name': offer.get('name', 'N/A')
                }
                details.append(detail)
                
                if verbose:
                    print(f"      Заменен оффер {old_id} → {new_id} в path '{path_name}'")
        
        # Пересчитываем веса если были замены
        if path_modified and recalc_weights and offers:
            old_weights = [o.get('weight', 0) for o in offers]
            recalculate_weights(offers)
            new_weights = [o.get('weight', 0) for o in offers]
            
            if verbose:
                print(f"      Веса пересчитаны: {'/'.join(map(str, old_weights))} → {'/'.join(map(str, new_weights))}")
    
    return paths, found_count, replaced_count, details


def process_tracker(tracker_name, api_key, base_url, old_pattern, new_pattern, options):
    """
    Обработать один трекер Binom
    
    Args:
        tracker_name: название трекера
        api_key: API ключ
        base_url: базовый URL API
        old_pattern: паттерн старых офферов
        new_pattern: паттерн новых офферов
        options: опции выполнения
    
    Returns:
        dict с результатами
    """
    print("\n" + "="*80)
    print(f"ОБРАБОТКА ТРЕКЕРА: {tracker_name}")
    print("="*80)
    
    # Создаем API клиент для этого трекера
    api = BinomAPI(api_key=api_key, base_url=base_url, debug=False)
    
    # Создаем умный маппинг
    replacement_map = create_smart_mapping(api, old_pattern, new_pattern)
    
    if not replacement_map:
        print(f"\n⚠️  Не найдено офферов для замены в трекере {tracker_name}")
        return {
            'tracker': tracker_name,
            'campaigns_processed': 0,
            'offers_replaced': 0,
            'errors': []
        }
    
    # Получаем кампании
    print(f"\n📊 Получение кампаний...")
    min_clicks = options.get('min_clicks', 5000)
    date_preset = options.get('date_preset', 'last_30_days')
    
    stats = api.get_stats_campaigns(date_preset=date_preset, limit=1000)
    campaigns = [
        {'id': int(c['id']), 'name': c.get('name', f"Campaign {c['id']}")}
        for c in stats
        if c.get('id', '').isdigit() and int(c.get('clicks', 0)) > min_clicks
    ]
    
    print(f"   Найдено кампаний с >{min_clicks} кликов: {len(campaigns)}")
    
    if not campaigns:
        print(f"\n⚠️  Нет кампаний для обработки в трекере {tracker_name}")
        return {
            'tracker': tracker_name,
            'campaigns_processed': 0,
            'offers_replaced': 0,
            'errors': []
        }
    
    # Обрабатываем кампании
    results = []
    total_replaced = 0
    errors = []
    
    dry_run = options.get('dry_run', True)
    
    for i, campaign in enumerate(campaigns, 1):
        print(f"\n[{i}/{len(campaigns)}] Кампания ID {campaign['id']}: {campaign['name'][:60]}")
        
        try:
            # Получаем детали
            campaign_data = api.get_campaign_details(campaign['id'])
            custom_rotation = campaign_data.get('customRotation')
            
            if not custom_rotation:
                print(f"  ⚪ Нет customRotation")
                continue
            
            found = 0
            replaced = 0
            
            # Обработка defaultPaths
            default_paths = custom_rotation.get('defaultPaths', [])
            if default_paths:
                modified, f, r, _ = find_and_replace_offers_smart(
                    default_paths, replacement_map, 
                    recalc_weights=True, verbose=True
                )
                if f > 0:
                    custom_rotation['defaultPaths'] = modified
                    found += f
                    replaced += r
            
            # Обработка rules
            rules = custom_rotation.get('rules', [])
            for rule in rules:
                rule_paths = rule.get('paths', [])
                if rule_paths:
                    modified, f, r, _ = find_and_replace_offers_smart(
                        rule_paths, replacement_map,
                        recalc_weights=True, verbose=True
                    )
                    if f > 0:
                        rule['paths'] = modified
                        found += f
                        replaced += r
            
            if found == 0:
                print(f"  ⚪ Офферы не найдены")
                continue
            
            if dry_run:
                print(f"  🔍 DRY RUN: Будет заменено {replaced} офферов")
            else:
                # Обновляем кампанию
                update_data = transform_campaign_for_update(campaign_data)
                api.update_campaign(campaign['id'], update_data)
                print(f"  ✅ Обновлено {replaced} офферов")
                
                import time
                time.sleep(options.get('delay', 0.5))
            
            total_replaced += replaced
            results.append({
                'id': campaign['id'],
                'name': campaign['name'],
                'replaced': replaced
            })
            
        except Exception as e:
            error_msg = f"Кампания {campaign['id']}: {str(e)}"
            print(f"  ❌ Ошибка: {error_msg}")
            errors.append(error_msg)
    
    return {
        'tracker': tracker_name,
        'campaigns_processed': len(results),
        'offers_replaced': total_replaced,
        'errors': errors,
        'results': results
    }


def main():
    # Конфигурация
    config = {
        'old_offer_pattern': 'Memorra',
        'new_offer_pattern': 'Cleanserra',
        'options': {
            'min_clicks': 5000,
            'date_preset': 'last_30_days',
            'dry_run': False,  # PRODUCTION режим
            'delay': 0.5
        }
    }
    
    # Трекеры
    trackers = [
        {
            'name': 'PierDun',
            'api_key': os.getenv('binomPublic'),
            'base_url': 'https://pierdun.com/public/api/v1'
        },
        {
            'name': 'Newareay',
            'api_key': os.getenv('Binom_Newareay'),
            'base_url': 'https://newareay.com/public/api/v1'
        },
        {
            'name': 'Warphelsing',
            'api_key': os.getenv('WARPHELSING_KEY'),
            'base_url': 'https://warphelsing.com/public/api/v1'
        }
    ]
    
    print("="*80)
    print("УМНАЯ ЗАМЕНА ОФФЕРОВ ВО ВСЕХ ТРЕКЕРАХ")
    print("="*80)
    print(f"\nСтарые офферы: {config['old_offer_pattern']}")
    print(f"Новые офферы: {config['new_offer_pattern']}")
    print(f"Режим: {'DRY RUN' if config['options']['dry_run'] else 'PRODUCTION'}")
    
    # Обработка всех трекеров
    all_results = []
    
    for tracker in trackers:
        if not tracker['api_key']:
            print(f"\n⚠️  Пропуск трекера {tracker['name']} - нет API ключа")
            continue
        
        result = process_tracker(
            tracker['name'],
            tracker['api_key'],
            tracker['base_url'],
            config['old_offer_pattern'],
            config['new_offer_pattern'],
            config['options']
        )
        
        all_results.append(result)
    
    # Итоговая статистика
    print("\n" + "="*80)
    print("ИТОГОВАЯ СТАТИСТИКА ПО ВСЕМ ТРЕКЕРАМ")
    print("="*80)
    
    for result in all_results:
        print(f"\n📊 {result['tracker']}:")
        print(f"   Обработано кампаний: {result['campaigns_processed']}")
        print(f"   Заменено офферов: {result['offers_replaced']}")
        print(f"   Ошибок: {len(result['errors'])}")
    
    total_campaigns = sum(r['campaigns_processed'] for r in all_results)
    total_offers = sum(r['offers_replaced'] for r in all_results)
    total_errors = sum(len(r['errors']) for r in all_results)
    
    print(f"\n🎯 ВСЕГО:")
    print(f"   Кампаний обработано: {total_campaigns}")
    print(f"   Офферов заменено: {total_offers}")
    print(f"   Ошибок: {total_errors}")
    
    # Сохранение результатов
    output_file = 'multi_tracker_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'config': config,
            'trackers': all_results,
            'totals': {
                'campaigns': total_campaigns,
                'offers': total_offers,
                'errors': total_errors
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nРезультаты сохранены в {output_file}")


if __name__ == "__main__":
    main()

