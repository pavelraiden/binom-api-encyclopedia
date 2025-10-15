#!/usr/bin/env python3
"""
Модуль для работы с Binom API v1
Использует Bearer авторизацию через переменную окружения binomPublic
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta


class BinomAPI:
    """Класс для работы с Binom API"""
    
    def __init__(self, api_key=None, base_url=None, debug=False):
        self.api_key = api_key or os.getenv('binomPublic')
        if not self.api_key:
            raise ValueError("API ключ не найден")
        
        self.base_url = base_url or "https://pierdun.com/public/api/v1"
        self.debug = debug
        self.headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                     data: Optional[Dict] = None) -> Dict:
        """
        Выполнить HTTP запрос к API
        
        Args:
            method: HTTP метод (GET, POST, PUT, DELETE)
            endpoint: Эндпоинт API (без base_url)
            params: Query параметры
            data: Данные для тела запроса
            
        Returns:
            Ответ API в виде словаря
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=data,
                timeout=30
            )
            
            # Логирование для отладки
            if self.debug:
                print(f"\n{'='*80}")
                print(f"Request: {method} {url}")
                if params:
                    print(f"Params: {json.dumps(params, indent=2)}")
                if data:
                    print(f"Data: {json.dumps(data, indent=2)}")
                print(f"Status: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                print(f"{'='*80}\n")
            
            if response.status_code >= 400:
                error_msg = f"API Error {response.status_code}: {response.text}"
                raise Exception(error_msg)
            
            return response.json() if response.text else {}
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка запроса: {str(e)}")
    
    def get_offers(self, name: Optional[str] = None, status: str = "all", 
                   date_preset: str = "last_30_days", limit: int = 1000) -> List[Dict]:
        """
        Получить список офферов
        
        Args:
            name: Фильтр по названию
            status: Статус (all, active, with_traffic, deleted)
            date_preset: Временной период
            limit: Максимальное количество записей
            
        Returns:
            Список офферов
        """
        params = {
            "datePreset": date_preset,
            "timezone": "UTC",
            "status": status,
            "limit": limit,
            "offset": 0,
            "sortColumn": "clicks",
            "sortType": "desc"
        }
        
        if name:
            params["name"] = name
        
        return self._make_request("GET", "/info/offer", params=params)
    
    def get_campaigns(self, status: str = "all", date_preset: str = "last_30_days", 
                     limit: int = 1000) -> List[Dict]:
        """
        Получить список кампаний
        
        Args:
            status: Статус (all, active, with_traffic, deleted)
            date_preset: Временной период
            limit: Максимальное количество записей
            
        Returns:
            Список кампаний
        """
        params = {
            "datePreset": date_preset,
            "timezone": "UTC",
            "status": status,
            "limit": limit,
            "offset": 0,
            "sortColumn": "clicks",
            "sortType": "desc"
        }
        
        return self._make_request("GET", "/info/campaign", params=params)
    
    def get_campaign_details(self, campaign_id: int) -> Dict:
        """
        Получить детальную информацию о кампании
        
        Args:
            campaign_id: ID кампании
            
        Returns:
            Детали кампании
        """
        return self._make_request("GET", f"/campaign/{campaign_id}")
    
    def update_campaign(self, campaign_id: int, campaign_data: Dict) -> Dict:
        """
        Обновить кампанию
        
        Args:
            campaign_id: ID кампании
            campaign_data: Данные для обновления
            
        Returns:
            Результат обновления
        """
        return self._make_request("PUT", f"/campaign/{campaign_id}", data=campaign_data)
    
    def get_stats_campaigns(self, date_preset: str = "last_30_days", 
                           limit: int = 1000) -> List[Dict]:
        """
        Получить статистику по кампаниям
        
        Args:
            date_preset: Временной период
            limit: Максимальное количество записей
            
        Returns:
            Статистика кампаний
        """
        params = {
            "datePreset": date_preset,
            "timezone": "UTC",
            "limit": limit,
            "offset": 0,
            "sortColumn": "clicks",
            "sortType": "desc"
        }
        
        return self._make_request("GET", "/stats/campaign", params=params)


if __name__ == "__main__":
    # Тест подключения
    api = BinomAPI()
    print("✅ API инициализирован успешно")
    print(f"Base URL: {api.base_url}")
    print(f"API Key: {api.api_key[:10]}...")

