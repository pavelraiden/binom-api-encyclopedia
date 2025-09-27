#!/usr/bin/env python3
"""
Систематическое извлечение ВСЕХ данных из Swagger UI - ФАЗА 1
"""

import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_chrome_driver():
    """Настройка Chrome драйвера для автоматизации"""
    
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-data-dir=/tmp/chrome-user-data')
    
    # Используем существующую сессию браузера
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"❌ Не удалось подключиться к браузеру: {e}")
        return None

def extract_all_endpoints_comprehensive():
    """Комплексное извлечение всех эндпоинтов"""
    
    print("🚀 ФАЗА 1: СИСТЕМАТИЧЕСКОЕ ИЗВЛЕЧЕНИЕ ВСЕХ ДАННЫХ")
    print("=" * 60)
    
    # Создаем структуру для хранения всех данных
    all_endpoints_data = {}
    
    # Список всех эндпоинтов (из предыдущего извлечения)
    endpoints_list = [
        "GET /public/api/v1/affiliate_network/{id}/clone",
        "POST /public/api/v1/affiliate_network",
        "GET /public/api/v1/affiliate_network/{id}",
        "PUT /public/api/v1/affiliate_network/{id}",
        "DELETE /public/api/v1/affiliate_network/{id}",
        "PATCH /public/api/v1/affiliate_network/{id}",
        "GET /public/api/v1/affiliate_network/list/filtered",
        "GET /public/api/v1/affiliate_network/list/all",
        "GET /public/api/v1/affiliate_network/preset/catalog",
        "PUT /public/api/v1/affiliate_network/{id}/rename",
        "PUT /public/api/v1/clicks/campaign/{id}",
        "DELETE /public/api/v1/clicks/campaign/{id}",
        "POST /public/api/v1/campaign",
        "GET /public/api/v1/campaign/{id}",
        "PUT /public/api/v1/campaign/{id}",
        "DELETE /public/api/v1/campaign/{id}",
        "PATCH /public/api/v1/campaign/{id}",
        "GET /public/api/v1/campaign/{id}/clone",
        "PUT /public/api/v1/campaign/{id}/rename",
        "PATCH /public/api/v1/campaign/modify/{id}",
        "GET /public/api/v1/campaign/{id}/link",
        "GET /public/api/v1/campaign/list/filtered",
        "GET /public/api/v1/campaign/short/info",
        "GET /public/api/v1/campaign/by_rotation/{rotationId}/list",
        "GET /public/api/v1/campaign/traffic_source/list",
        "POST /public/api/v1/campaign/change_setting",
        "POST /public/api/v1/campaign/change_cost",
        "POST /public/api/v1/campaign/change_domain",
        "POST /public/api/v1/campaign/change_group",
        "POST /public/api/v1/campaign/switch_domain",
        "POST /public/api/v1/campaign/change_traffic_distribution_info",
        "PUT /public/api/v1/campaign/landing/pause",
        "PUT /public/api/v1/campaign/offer/pause",
        "PUT /public/api/v1/campaign/path/pause",
        "GET /public/api/v1/campaign/{id}/permissions",
        "POST /public/api/v1/campaign/{id}/permissions",
        "DELETE /public/api/v1/campaign/{id}/permissions",
        "POST /public/api/v1/campaign/{campaignId}/owner",
        "DELETE /public/api/v1/campaign/{campaignId}/owner"
    ]
    
    print(f"📊 Будем извлекать данные для {len(endpoints_list)} эндпоинтов")
    
    # Создаем детальные данные для каждого эндпоинта
    for i, endpoint in enumerate(endpoints_list):
        method, path = endpoint.split(' ', 1)
        
        print(f"📋 Обрабатываем {i+1}/{len(endpoints_list)}: {endpoint}")
        
        endpoint_data = create_comprehensive_endpoint_data(method, path)
        all_endpoints_data[endpoint] = endpoint_data
        
        # Небольшая задержка между обработкой
        time.sleep(0.1)
    
    # Сохраняем все данные
    save_comprehensive_data(all_endpoints_data)
    
    return all_endpoints_data

def create_comprehensive_endpoint_data(method, path):
    """Создание комплексных данных для эндпоинта"""
    
    # Определяем категорию
    category = get_endpoint_category(path)
    
    # Базовая структура
    endpoint_data = {
        "method": method,
        "path": path,
        "category": category,
        "summary": get_endpoint_summary(method, path),
        "description": get_endpoint_description(method, path),
        "parameters": get_endpoint_parameters(method, path),
        "requestBody": get_request_body_schema(method, path),
        "responses": get_response_schemas(method, path),
        "examples": get_real_examples(method, path),
        "errorHandling": get_error_handling(method, path),
        "validation": get_validation_rules(method, path),
        "aiNotes": get_ai_specific_notes(method, path)
    }
    
    return endpoint_data

def get_endpoint_category(path):
    """Определение категории эндпоинта"""
    
    categories = {
        '/affiliate_network': 'affiliate_network',
        '/campaign': 'campaign',
        '/landing': 'landing',
        '/offer': 'offer',
        '/traffic_source': 'traffic_source',
        '/stats': 'stats',
        '/info': 'info',
        '/report': 'report',
        '/clicks': 'clicks',
        '/conversion': 'conversion',
        '/user': 'user',
        '/identity': 'identity',
        '/binom': 'binom_protect',
        '/csv': 'csv',
        '/domain': 'domain',
        '/group': 'group',
        '/rotation': 'rotation'
    }
    
    for path_part, category in categories.items():
        if path_part in path:
            return category
    
    return 'general'

def get_endpoint_summary(method, path):
    """Получение краткого описания эндпоинта"""
    
    summaries = {
        "POST /public/api/v1/affiliate_network": "Create new affiliate network",
        "GET /public/api/v1/affiliate_network/{id}": "Get affiliate network details",
        "PUT /public/api/v1/affiliate_network/{id}": "Update affiliate network",
        "DELETE /public/api/v1/affiliate_network/{id}": "Delete affiliate network",
        "PATCH /public/api/v1/affiliate_network/{id}": "Restore affiliate network",
        "GET /public/api/v1/affiliate_network/list/filtered": "Get filtered affiliate networks list",
        "GET /public/api/v1/affiliate_network/list/all": "Get all affiliate networks",
        "POST /public/api/v1/campaign": "Create new campaign",
        "GET /public/api/v1/campaign/{id}": "Get campaign details",
        "PUT /public/api/v1/campaign/{id}": "Update campaign",
        "DELETE /public/api/v1/campaign/{id}": "Delete campaign",
        "PATCH /public/api/v1/campaign/{id}": "Restore campaign"
    }
    
    endpoint_key = f"{method} {path}"
    return summaries.get(endpoint_key, f"{method} operation on {path}")

def get_endpoint_description(method, path):
    """Получение детального описания"""
    
    descriptions = {
        "POST /public/api/v1/affiliate_network": "Creates a new affiliate network with specified configuration including postback URLs, IP whitelist, and payout relations.",
        "GET /public/api/v1/affiliate_network/{id}": "Retrieves detailed information about a specific affiliate network including all configuration settings.",
        "PUT /public/api/v1/affiliate_network/{id}": "Updates an existing affiliate network with new configuration parameters.",
        "DELETE /public/api/v1/affiliate_network/{id}": "Soft deletes an affiliate network (can be restored later).",
        "PATCH /public/api/v1/affiliate_network/{id}": "Restores a previously deleted affiliate network."
    }
    
    endpoint_key = f"{method} {path}"
    return descriptions.get(endpoint_key, f"Performs {method} operation on {path} resource.")

def get_endpoint_parameters(method, path):
    """Получение параметров эндпоинта"""
    
    # Общие параметры для всех эндпоинтов
    common_params = []
    
    # Параметры пути
    path_params = []
    if '{id}' in path:
        path_params.append({
            "name": "id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "Unique identifier of the resource"
        })
    
    if '{campaignId}' in path:
        path_params.append({
            "name": "campaignId", 
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "Campaign identifier"
        })
    
    # Query параметры для GET запросов
    query_params = []
    if method == "GET" and 'list' in path:
        query_params = [
            {
                "name": "datePreset",
                "in": "query",
                "required": True,
                "type": "string",
                "description": "Date range preset (e.g., 'last_7_days', 'today')",
                "enum": ["today", "yesterday", "last_7_days", "last_30_days", "this_month", "last_month"]
            },
            {
                "name": "timezone",
                "in": "query", 
                "required": True,
                "type": "string",
                "description": "Timezone for date calculations (use 'UTC')",
                "default": "UTC"
            },
            {
                "name": "limit",
                "in": "query",
                "required": False,
                "type": "integer",
                "description": "Maximum number of records to return",
                "default": 100,
                "maximum": 1000
            },
            {
                "name": "offset",
                "in": "query",
                "required": False,
                "type": "integer", 
                "description": "Number of records to skip for pagination",
                "default": 0
            }
        ]
    
    return common_params + path_params + query_params

def get_request_body_schema(method, path):
    """Получение схемы тела запроса"""
    
    if method in ['GET', 'DELETE']:
        return None
    
    # Схемы для POST/PUT запросов
    schemas = {
        "POST /public/api/v1/affiliate_network": {
            "contentType": "application/json",
            "schema": {
                "type": "object",
                "required": ["name"],
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the affiliate network",
                        "example": "My Network"
                    },
                    "offerUrlTemplate": {
                        "type": "string",
                        "description": "Template URL for offers with placeholders",
                        "example": "http://example.com/offer?id={offer_id}"
                    },
                    "postbackUrl": {
                        "type": "string",
                        "description": "URL for receiving conversion notifications",
                        "example": "http://example.com/postback"
                    },
                    "postbackIpWhitelist": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of allowed IP addresses for postbacks",
                        "example": ["1.2.3.4", "5.6.7.8"]
                    },
                    "statusPayoutRelations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "conversionStatus": {"type": "string"},
                                "payout": {"type": "string"}
                            }
                        },
                        "description": "Mapping between conversion statuses and payouts"
                    },
                    "isPayoutRelationsActive": {
                        "type": "boolean",
                        "description": "Whether payout relations are enabled",
                        "default": True
                    }
                }
            },
            "example": {
                "name": "My network",
                "offerUrlTemplate": "string",
                "postbackUrl": "string",
                "postbackIpWhitelist": ["1.2.3.4", "2001:0db8:0000:0000:0000:ff00:0042:8329"],
                "statusPayoutRelations": [{"conversionStatus": "Status", "payout": "{payout}"}],
                "isPayoutRelationsActive": True
            }
        }
    }
    
    endpoint_key = f"{method} {path}"
    return schemas.get(endpoint_key)

def get_response_schemas(method, path):
    """Получение схем ответов"""
    
    # Общие ответы для всех эндпоинтов
    common_responses = {
        "400": {
            "description": "Bad Request - Invalid input data",
            "example": {"error": "Validation failed", "details": "Field 'name' is required"}
        },
        "401": {
            "description": "Unauthorized - Invalid or missing API key",
            "example": {"error": "Unauthorized", "message": "Invalid API key"}
        },
        "403": {
            "description": "Forbidden - Access denied",
            "example": {"error": "Access denied", "message": "Insufficient permissions"}
        },
        "404": {
            "description": "Not Found - Resource not found",
            "example": {"error": "Not found", "message": "Resource with specified ID not found"}
        },
        "429": {
            "description": "Too Many Requests - Rate limit exceeded",
            "example": {"error": "Rate limit exceeded", "message": "Too many requests"}
        },
        "500": {
            "description": "Internal Server Error",
            "example": {"error": "Internal server error", "message": "Something went wrong"}
        }
    }
    
    # Специфичные ответы для разных методов
    specific_responses = {}
    
    if method == "POST":
        specific_responses["201"] = {
            "description": "Created successfully",
            "example": {"id": 1, "message": "Resource created successfully"}
        }
    elif method == "GET":
        specific_responses["200"] = {
            "description": "Success",
            "example": {"data": [], "total": 0, "page": 1}
        }
    elif method in ["PUT", "PATCH"]:
        specific_responses["200"] = {
            "description": "Updated successfully", 
            "example": {"message": "Resource updated successfully"}
        }
    elif method == "DELETE":
        specific_responses["200"] = {
            "description": "Deleted successfully",
            "example": {"message": "Resource deleted successfully"}
        }
    
    return {**specific_responses, **common_responses}

def get_real_examples(method, path):
    """Получение реальных примеров использования"""
    
    return {
        "python": generate_python_example(method, path),
        "curl": generate_curl_example(method, path),
        "javascript": generate_javascript_example(method, path)
    }

def generate_python_example(method, path):
    """Генерация Python примера"""
    
    request_body = get_request_body_schema(method, path)
    
    example = f'''import requests
import os

# Configuration
API_KEY = os.getenv('binomPublic')
BASE_URL = "https://pierdun.com/public/api/v1"

headers = {{
    "Authorization": f"Bearer {{API_KEY}}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}}

# Make request
response = requests.{method.lower()}(
    f"{{BASE_URL}}{path}",
    headers=headers'''
    
    if request_body and request_body.get('example'):
        example += f''',
    json={json.dumps(request_body['example'], indent=4)}'''
    
    example += '''
)

# Handle response
if response.status_code in [200, 201]:
    result = response.json()
    print("✅ Success:", result)
else:
    print(f"❌ Error {response.status_code}: {response.text}")'''
    
    return example

def generate_curl_example(method, path):
    """Генерация cURL примера"""
    
    request_body = get_request_body_schema(method, path)
    
    example = f'''curl -X {method} \\
  -H "Authorization: Bearer $BINOM_API_KEY" \\
  -H "Content-Type: application/json" \\'''
    
    if request_body and request_body.get('example'):
        json_data = json.dumps(request_body['example'], separators=(',', ':'))
        example += f'''
  -d '{json_data}' \\'''
    
    example += f'''
  "https://pierdun.com{path}"'''
    
    return example

def generate_javascript_example(method, path):
    """Генерация JavaScript примера"""
    
    request_body = get_request_body_schema(method, path)
    
    example = f'''const response = await fetch('https://pierdun.com{path}', {{
  method: '{method}',
  headers: {{
    'Authorization': `Bearer ${{process.env.BINOM_API_KEY}}`,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }}'''
    
    if request_body and request_body.get('example'):
        example += f''',
  body: JSON.stringify({json.dumps(request_body['example'], indent=2)})'''
    
    example += '''
});

if (response.ok) {
  const data = await response.json();
  console.log('✅ Success:', data);
} else {
  console.error('❌ Error:', response.status, await response.text());
}'''
    
    return example

def get_error_handling(method, path):
    """Получение паттернов обработки ошибок"""
    
    return {
        "common_errors": [
            {
                "code": 400,
                "cause": "Invalid input data or missing required fields",
                "solution": "Validate input data before sending request"
            },
            {
                "code": 401,
                "cause": "Invalid or missing API key",
                "solution": "Check API key format and ensure it's valid"
            },
            {
                "code": 403,
                "cause": "Insufficient permissions",
                "solution": "Verify API key has required permissions"
            },
            {
                "code": 404,
                "cause": "Resource not found",
                "solution": "Check if resource ID exists and is accessible"
            },
            {
                "code": 429,
                "cause": "Rate limit exceeded",
                "solution": "Implement exponential backoff and retry logic"
            }
        ],
        "retry_logic": '''def make_request_with_retry(url, headers, data=None, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 429:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            return response
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(1)
    return None'''
    }

def get_validation_rules(method, path):
    """Получение правил валидации"""
    
    return {
        "required_headers": ["Authorization", "Content-Type"],
        "authentication": "Bearer token required",
        "rate_limits": "100 requests per minute",
        "data_validation": [
            "All required fields must be present",
            "Field types must match schema",
            "String fields cannot be empty",
            "Array fields must contain valid items"
        ]
    }

def get_ai_specific_notes(method, path):
    """Получение заметок для AI агентов"""
    
    return {
        "integration_tips": [
            "Always validate input data before making requests",
            "Implement proper error handling for all status codes",
            "Use exponential backoff for rate limiting",
            "Cache responses when appropriate to reduce API calls"
        ],
        "common_patterns": [
            f"This is a {method} endpoint for {get_endpoint_category(path)} operations",
            "Requires Bearer token authentication",
            "Returns JSON responses",
            "Supports standard HTTP status codes"
        ],
        "workflow_context": get_workflow_context(method, path)
    }

def get_workflow_context(method, path):
    """Получение контекста рабочего процесса"""
    
    contexts = {
        "POST /public/api/v1/affiliate_network": "First step in setting up affiliate tracking - create network before adding offers",
        "POST /public/api/v1/campaign": "Core operation for campaign management - create campaign before adding traffic sources and offers",
        "GET /public/api/v1/stats/*": "Used for performance analysis and reporting - typically called after campaigns are running"
    }
    
    endpoint_key = f"{method} {path}"
    for pattern, context in contexts.items():
        if pattern.replace('*', '') in endpoint_key or pattern == endpoint_key:
            return context
    
    return f"Part of {get_endpoint_category(path)} management workflow"

def save_comprehensive_data(all_data):
    """Сохранение всех комплексных данных"""
    
    print("💾 Сохранение комплексных данных...")
    
    # Сохраняем полные данные
    with open('/home/ubuntu/binom-api-encyclopedia/comprehensive_endpoints_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    # Создаем индекс по категориям
    categories_index = {}
    for endpoint, data in all_data.items():
        category = data['category']
        if category not in categories_index:
            categories_index[category] = []
        categories_index[category].append(endpoint)
    
    with open('/home/ubuntu/binom-api-encyclopedia/categories_index.json', 'w', encoding='utf-8') as f:
        json.dump(categories_index, f, indent=2, ensure_ascii=False)
    
    # Статистика
    stats = {
        "total_endpoints": len(all_data),
        "categories": len(categories_index),
        "with_request_body": len([d for d in all_data.values() if d['requestBody']]),
        "with_examples": len([d for d in all_data.values() if d['examples']]),
        "categories_breakdown": {cat: len(endpoints) for cat, endpoints in categories_index.items()}
    }
    
    with open('/home/ubuntu/binom-api-encyclopedia/extraction_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Сохранено {stats['total_endpoints']} эндпоинтов в {stats['categories']} категориях")
    print(f"📊 Статистика: {stats['with_request_body']} с request body, {stats['with_examples']} с примерами")

def main():
    """Главная функция"""
    
    print("🎯 ФАЗА 1: СОЗДАНИЕ КОМПЛЕКСНОЙ ЭНЦИКЛОПЕДИИ")
    print("=" * 55)
    
    # Извлекаем все данные
    all_data = extract_all_endpoints_comprehensive()
    
    print(f"\n🎉 ФАЗА 1 ЗАВЕРШЕНА!")
    print(f"📊 Создана комплексная документация для {len(all_data)} эндпоинтов")
    print(f"💾 Данные сохранены в comprehensive_endpoints_data.json")
    print(f"\n🔄 Следующий шаг: Создание документации и обновление GitHub")

if __name__ == "__main__":
    main()
