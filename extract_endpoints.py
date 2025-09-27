#!/usr/bin/env python3
"""
Extract all Binom API endpoints from Swagger documentation
"""

import requests
import json
import os
from urllib.parse import urljoin

def extract_swagger_spec():
    """Extract OpenAPI/Swagger specification from Binom API docs"""
    
    print("🔍 ИЗВЛЕЧЕНИЕ SWAGGER СПЕЦИФИКАЦИИ")
    print("=" * 50)
    
    # Попробуем разные возможные URL для Swagger JSON
    swagger_urls = [
        "https://pierdun.com/api/doc.json",
        "https://pierdun.com/api/doc/swagger.json", 
        "https://pierdun.com/api/swagger.json",
        "https://pierdun.com/public/api/v1/doc.json",
        "https://pierdun.com/api/doc?format=json"
    ]
    
    for url in swagger_urls:
        try:
            print(f"📡 Пробуем URL: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                try:
                    swagger_data = response.json()
                    print(f"✅ Swagger спецификация найдена: {url}")
                    
                    # Сохраняем полную спецификацию
                    with open('swagger_spec.json', 'w', encoding='utf-8') as f:
                        json.dump(swagger_data, f, ensure_ascii=False, indent=2)
                    
                    return swagger_data
                    
                except json.JSONDecodeError:
                    print(f"❌ Не JSON формат: {url}")
                    continue
            else:
                print(f"❌ HTTP {response.status_code}: {url}")
                
        except Exception as e:
            print(f"❌ Ошибка запроса {url}: {e}")
            continue
    
    print("❌ Swagger спецификация не найдена через стандартные URL")
    return None

def parse_swagger_endpoints(swagger_data):
    """Парсинг эндпоинтов из Swagger спецификации"""
    
    print("\n📋 ПАРСИНГ ЭНДПОИНТОВ")
    print("=" * 30)
    
    endpoints = []
    
    if not swagger_data or 'paths' not in swagger_data:
        print("❌ Некорректная структура Swagger")
        return endpoints
    
    paths = swagger_data.get('paths', {})
    
    for path, methods in paths.items():
        for method, details in methods.items():
            if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                
                endpoint = {
                    'path': path,
                    'method': method.upper(),
                    'summary': details.get('summary', ''),
                    'description': details.get('description', ''),
                    'operationId': details.get('operationId', ''),
                    'tags': details.get('tags', []),
                    'parameters': details.get('parameters', []),
                    'requestBody': details.get('requestBody', {}),
                    'responses': details.get('responses', {}),
                    'security': details.get('security', [])
                }
                
                endpoints.append(endpoint)
                
                print(f"✅ {method.upper()} {path} - {details.get('summary', 'No summary')}")
    
    print(f"\n📊 Всего найдено эндпоинтов: {len(endpoints)}")
    
    # Сохраняем список эндпоинтов
    with open('endpoints_list.json', 'w', encoding='utf-8') as f:
        json.dump(endpoints, f, ensure_ascii=False, indent=2)
    
    return endpoints

def extract_from_html():
    """Извлечение эндпоинтов из HTML страницы документации"""
    
    print("\n🌐 ИЗВЛЕЧЕНИЕ ИЗ HTML ДОКУМЕНТАЦИИ")
    print("=" * 40)
    
    try:
        response = requests.get("https://pierdun.com/api/doc", timeout=15)
        
        if response.status_code != 200:
            print(f"❌ Ошибка доступа к документации: {response.status_code}")
            return []
        
        html_content = response.text
        
        # Сохраняем HTML для анализа
        with open('api_doc.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ HTML документация сохранена в api_doc.html")
        
        # Простой парсинг эндпоинтов из HTML
        endpoints = []
        
        # Ищем паттерны эндпоинтов
        import re
        
        # Паттерн для поиска эндпоинтов в HTML
        endpoint_pattern = r'(GET|POST|PUT|DELETE|PATCH)\s*/public/api/v1/([^\s<>"]+)'
        
        matches = re.findall(endpoint_pattern, html_content, re.IGNORECASE)
        
        for method, path_part in matches:
            full_path = f"/public/api/v1/{path_part}"
            
            endpoint = {
                'method': method.upper(),
                'path': full_path,
                'source': 'html_extraction'
            }
            
            endpoints.append(endpoint)
            print(f"✅ {method.upper()} {full_path}")
        
        print(f"\n📊 Извлечено из HTML: {len(endpoints)} эндпоинтов")
        
        # Удаляем дубликаты
        unique_endpoints = []
        seen = set()
        
        for endpoint in endpoints:
            key = f"{endpoint['method']}:{endpoint['path']}"
            if key not in seen:
                seen.add(key)
                unique_endpoints.append(endpoint)
        
        print(f"📊 Уникальных эндпоинтов: {len(unique_endpoints)}")
        
        # Сохраняем результат
        with open('endpoints_from_html.json', 'w', encoding='utf-8') as f:
            json.dump(unique_endpoints, f, ensure_ascii=False, indent=2)
        
        return unique_endpoints
        
    except Exception as e:
        print(f"❌ Ошибка извлечения из HTML: {e}")
        return []

def categorize_endpoints(endpoints):
    """Категоризация эндпоинтов по функциональности"""
    
    print("\n🏷️ КАТЕГОРИЗАЦИЯ ЭНДПОИНТОВ")
    print("=" * 35)
    
    categories = {
        'affiliate_network': [],
        'campaign': [],
        'clicks': [],
        'info': [],
        'report': [],
        'stats': [],
        'identity': [],
        'binom_protect': [],
        'csv': [],
        'rotation': [],
        'other': []
    }
    
    for endpoint in endpoints:
        path = endpoint.get('path', '')
        
        if '/affiliate_network' in path:
            categories['affiliate_network'].append(endpoint)
        elif '/campaign' in path:
            categories['campaign'].append(endpoint)
        elif '/clicks' in path:
            categories['clicks'].append(endpoint)
        elif '/info/' in path:
            categories['info'].append(endpoint)
        elif '/report' in path:
            categories['report'].append(endpoint)
        elif '/stats/' in path:
            categories['stats'].append(endpoint)
        elif '/identity' in path:
            categories['identity'].append(endpoint)
        elif '/binom/protect' in path:
            categories['binom_protect'].append(endpoint)
        elif '/csv' in path:
            categories['csv'].append(endpoint)
        elif 'landing/pause' in path or 'offer/pause' in path or 'path/pause' in path:
            categories['rotation'].append(endpoint)
        else:
            categories['other'].append(endpoint)
    
    # Выводим статистику по категориям
    for category, endpoints_list in categories.items():
        if endpoints_list:
            print(f"📂 {category}: {len(endpoints_list)} эндпоинтов")
    
    # Сохраняем категоризированные эндпоинты
    with open('endpoints_categorized.json', 'w', encoding='utf-8') as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)
    
    return categories

def generate_endpoint_summary():
    """Генерация сводки по всем эндпоинтам"""
    
    print("\n📊 ГЕНЕРАЦИЯ СВОДКИ")
    print("=" * 25)
    
    # Загружаем все найденные эндпоинты
    all_endpoints = []
    
    # Из Swagger (если есть)
    if os.path.exists('endpoints_list.json'):
        with open('endpoints_list.json', 'r', encoding='utf-8') as f:
            swagger_endpoints = json.load(f)
            all_endpoints.extend(swagger_endpoints)
            print(f"✅ Загружено из Swagger: {len(swagger_endpoints)}")
    
    # Из HTML
    if os.path.exists('endpoints_from_html.json'):
        with open('endpoints_from_html.json', 'r', encoding='utf-8') as f:
            html_endpoints = json.load(f)
            all_endpoints.extend(html_endpoints)
            print(f"✅ Загружено из HTML: {len(html_endpoints)}")
    
    # Удаляем дубликаты
    unique_endpoints = []
    seen = set()
    
    for endpoint in all_endpoints:
        key = f"{endpoint.get('method', 'UNKNOWN')}:{endpoint.get('path', '')}"
        if key not in seen:
            seen.add(key)
            unique_endpoints.append(endpoint)
    
    print(f"📊 Всего уникальных эндпоинтов: {len(unique_endpoints)}")
    
    # Сохраняем финальный список
    with open('all_endpoints_final.json', 'w', encoding='utf-8') as f:
        json.dump(unique_endpoints, f, ensure_ascii=False, indent=2)
    
    # Категоризируем
    categories = categorize_endpoints(unique_endpoints)
    
    # Создаем markdown сводку
    summary_md = f"""# Binom API Endpoints Summary

## Overview
- **Total Endpoints**: {len(unique_endpoints)}
- **Extraction Date**: {json.dumps(None, default=str)}
- **Source**: Swagger + HTML Documentation

## Categories

"""
    
    for category, endpoints_list in categories.items():
        if endpoints_list:
            summary_md += f"### {category.replace('_', ' ').title()} ({len(endpoints_list)} endpoints)\n\n"
            
            for endpoint in endpoints_list:
                method = endpoint.get('method', 'UNKNOWN')
                path = endpoint.get('path', '')
                summary = endpoint.get('summary', endpoint.get('description', ''))
                
                summary_md += f"- **{method}** `{path}` - {summary}\n"
            
            summary_md += "\n"
    
    # Сохраняем markdown сводку
    with open('ENDPOINTS_SUMMARY.md', 'w', encoding='utf-8') as f:
        f.write(summary_md)
    
    print("✅ Сводка сохранена в ENDPOINTS_SUMMARY.md")
    
    return unique_endpoints, categories

def main():
    """Основная функция извлечения эндпоинтов"""
    
    print("🚀 ИЗВЛЕЧЕНИЕ ВСЕХ BINOM API ЭНДПОИНТОВ")
    print("=" * 60)
    
    # Пробуем извлечь Swagger спецификацию
    swagger_data = extract_swagger_spec()
    
    if swagger_data:
        swagger_endpoints = parse_swagger_endpoints(swagger_data)
    else:
        swagger_endpoints = []
    
    # Извлекаем из HTML документации
    html_endpoints = extract_from_html()
    
    # Генерируем финальную сводку
    all_endpoints, categories = generate_endpoint_summary()
    
    print(f"\n🎉 ИЗВЛЕЧЕНИЕ ЗАВЕРШЕНО!")
    print(f"📊 Всего найдено эндпоинтов: {len(all_endpoints)}")
    print(f"📁 Созданы файлы:")
    print(f"   - all_endpoints_final.json")
    print(f"   - endpoints_categorized.json") 
    print(f"   - ENDPOINTS_SUMMARY.md")
    
    if swagger_data:
        print(f"   - swagger_spec.json")
        print(f"   - endpoints_list.json")
    
    if html_endpoints:
        print(f"   - endpoints_from_html.json")
        print(f"   - api_doc.html")
    
    return all_endpoints, categories

if __name__ == "__main__":
    main()
