#!/usr/bin/env python3
"""
Преобразование данных кампании из GET формата в PUT формат
"""

def transform_campaign_for_update(campaign_data):
    """
    Преобразовать данные кампании из формата GET в формат PUT
    
    GET возвращает вложенные объекты:
    - cost: {model, money: {amount, currency}, isAuto}
    - hideReferrer: {type, domainUuid}
    
    PUT требует плоские поля:
    - costModel, amount, currency, isAuto
    - hideReferrerType, domainUuid
    """
    
    # Извлекаем данные из вложенных объектов
    cost = campaign_data.get('cost', {})
    money = cost.get('money', {})
    hide_referrer = campaign_data.get('hideReferrer', {})
    
    # Создаем новый объект с плоской структурой
    transformed = {
        "name": campaign_data.get('name'),
        "key": campaign_data.get('key'),
        "groupUuid": campaign_data.get('groupUuid'),
        "trafficSourceId": campaign_data.get('trafficSourceId'),
        
        # Плоские поля вместо вложенного cost
        "costModel": cost.get('model'),
        "amount": money.get('amount'),
        "currency": money.get('currency'),
        "isAuto": cost.get('isAuto'),
        
        # Плоское поле вместо вложенного hideReferrer
        "hideReferrerType": hide_referrer.get('type'),
        "domainUuid": campaign_data.get('domainUuid'),
        
        "distributionType": campaign_data.get('distributionType'),
        "rotationId": campaign_data.get('rotationId'),
        "customRotation": campaign_data.get('customRotation'),
        "campaignSettings": campaign_data.get('campaignSettings'),
        "tokens": campaign_data.get('tokens', [])
    }
    
    return transformed


if __name__ == "__main__":
    import json
    
    # Тест преобразования
    with open('campaign_82_before.json', 'r') as f:
        original = json.load(f)
    
    transformed = transform_campaign_for_update(original)
    
    print("Оригинальный формат (GET):")
    print(f"  cost.model: {original.get('cost', {}).get('model')}")
    print(f"  cost.money.amount: {original.get('cost', {}).get('money', {}).get('amount')}")
    print(f"  cost.money.currency: {original.get('cost', {}).get('money', {}).get('currency')}")
    print(f"  hideReferrer.type: {original.get('hideReferrer', {}).get('type')}")
    
    print("\nПреобразованный формат (PUT):")
    print(f"  costModel: {transformed.get('costModel')}")
    print(f"  amount: {transformed.get('amount')}")
    print(f"  currency: {transformed.get('currency')}")
    print(f"  hideReferrerType: {transformed.get('hideReferrerType')}")
    
    with open('campaign_82_transformed.json', 'w') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    
    print("\nСохранено в campaign_82_transformed.json")

