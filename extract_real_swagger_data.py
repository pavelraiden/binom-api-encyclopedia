#!/usr/bin/env python3
"""
Автоматическое извлечение реальных данных из Swagger UI
"""

import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_driver():
    """Настройка Chrome драйвера"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def extract_real_endpoint_data():
    """Извлечение реальных данных из Swagger UI"""
    
    print("🚀 ИЗВЛЕЧЕНИЕ РЕАЛЬНЫХ ДАННЫХ ИЗ SWAGGER UI")
    print("=" * 55)
    
    # Используем уже открытую страницу через JavaScript в браузере
    # Создаем JavaScript скрипт для извлечения данных
    
    js_script = """
    // Функция для извлечения всех реальных данных
    function extractAllRealData() {
        const realData = {};
        const operations = document.querySelectorAll('.opblock');
        
        console.log(`Found ${operations.length} operations to process`);
        
        let processedCount = 0;
        
        operations.forEach((operation, index) => {
            try {
                // Получаем базовую информацию
                const methodElement = operation.querySelector('.opblock-summary-method');
                const pathElement = operation.querySelector('.opblock-summary-path a');
                const summaryElement = operation.querySelector('.opblock-summary-description');
                
                if (!methodElement || !pathElement) return;
                
                const method = methodElement.textContent.trim();
                const path = pathElement.textContent.trim();
                const summary = summaryElement ? summaryElement.textContent.trim() : '';
                const endpointKey = `${method} ${path}`;
                
                console.log(`Processing ${index + 1}/${operations.length}: ${endpointKey}`);
                
                // Раскрываем операцию
                const summaryButton = operation.querySelector('.opblock-summary');
                if (summaryButton && !operation.classList.contains('is-open')) {
                    summaryButton.click();
                    // Небольшая задержка
                    setTimeout(() => {}, 100);
                }
                
                const endpointData = {
                    method: method,
                    path: path,
                    summary: summary,
                    parameters: [],
                    requestBody: null,
                    responses: {}
                };
                
                // Извлекаем параметры
                const parametersSection = operation.querySelector('.parameters');
                if (parametersSection) {
                    const paramTable = parametersSection.querySelector('table tbody');
                    if (paramTable) {
                        const rows = paramTable.querySelectorAll('tr');
                        rows.forEach(row => {
                            const cells = row.querySelectorAll('td');
                            if (cells.length >= 2) {
                                const nameCell = cells[0];
                                const descCell = cells[1];
                                
                                const nameText = nameCell.textContent.trim();
                                const isRequired = nameCell.querySelector('.required') !== null;
                                const description = descCell.textContent.trim();
                                
                                // Извлекаем имя параметра
                                const paramName = nameText.split('\\n')[0].replace('*', '').trim();
                                
                                // Определяем тип
                                let type = 'string';
                                if (nameText.includes('integer')) type = 'integer';
                                else if (nameText.includes('boolean')) type = 'boolean';
                                else if (nameText.includes('array')) type = 'array';
                                
                                endpointData.parameters.push({
                                    name: paramName,
                                    type: type,
                                    required: isRequired,
                                    description: description,
                                    in: path.includes(`{${paramName}}`) ? 'path' : 'query'
                                });
                            }
                        });
                    }
                }
                
                // Извлекаем тело запроса
                const requestBodySection = operation.querySelector('.request-body');
                if (requestBodySection) {
                    const requestBodyData = {
                        contentType: 'application/json',
                        example: null,
                        schema: null
                    };
                    
                    // Ищем пример
                    const exampleButton = requestBodySection.querySelector('button[title*="Example"], .btn[title*="Example"]');
                    if (exampleButton) {
                        exampleButton.click();
                        setTimeout(() => {}, 50);
                        
                        const codeBlock = requestBodySection.querySelector('.highlight-code pre, .microlight');
                        if (codeBlock) {
                            const codeText = codeBlock.textContent.trim();
                            try {
                                requestBodyData.example = JSON.parse(codeText);
                            } catch (e) {
                                requestBodyData.example = codeText;
                            }
                        }
                    }
                    
                    // Ищем схему
                    const schemaButton = requestBodySection.querySelector('button[title*="Schema"], .btn[title*="Schema"]');
                    if (schemaButton) {
                        schemaButton.click();
                        setTimeout(() => {}, 50);
                        
                        const schemaElement = requestBodySection.querySelector('.model-box, .model');
                        if (schemaElement) {
                            requestBodyData.schema = schemaElement.textContent.trim();
                        }
                    }
                    
                    if (requestBodyData.example || requestBodyData.schema) {
                        endpointData.requestBody = requestBodyData;
                    }
                }
                
                // Извлекаем ответы
                const responsesSection = operation.querySelector('.responses-wrapper');
                if (responsesSection) {
                    const responseRows = responsesSection.querySelectorAll('table tbody tr');
                    responseRows.forEach(row => {
                        const cells = row.querySelectorAll('td');
                        if (cells.length >= 2) {
                            const statusCode = cells[0].textContent.trim();
                            const description = cells[1].textContent.trim();
                            
                            const responseData = {
                                description: description,
                                example: null
                            };
                            
                            // Ищем пример ответа
                            const responseCodeBlock = row.querySelector('.highlight-code pre, .microlight');
                            if (responseCodeBlock) {
                                const codeText = responseCodeBlock.textContent.trim();
                                try {
                                    responseData.example = JSON.parse(codeText);
                                } catch (e) {
                                    responseData.example = codeText;
                                }
                            }
                            
                            endpointData.responses[statusCode] = responseData;
                        }
                    });
                }
                
                realData[endpointKey] = endpointData;
                processedCount++;
                
            } catch (e) {
                console.log(`Error processing operation ${index}: ${e.message}`);
            }
        });
        
        console.log(`Successfully processed ${processedCount} endpoints`);
        return realData;
    }
    
    // Запускаем извлечение
    return extractAllRealData();
    """
    
    # Сохраняем JavaScript скрипт
    with open('/home/ubuntu/binom-api-encyclopedia/extract_swagger_data.js', 'w', encoding='utf-8') as f:
        f.write(js_script)
    
    print("✅ JavaScript скрипт создан")
    print("📋 Для извлечения данных выполните в консоли браузера:")
    print("   1. Откройте https://pierdun.com/api/doc")
    print("   2. Выполните скрипт из файла extract_swagger_data.js")
    print("   3. Сохраните результат в real_swagger_data.json")
    
    return js_script

def create_real_data_processor():
    """Создание процессора для обработки реальных данных"""
    
    processor_code = '''#!/usr/bin/env python3
"""
Процессор реальных данных из Swagger UI
"""

import json
import os

def process_real_swagger_data():
    """Обработка реальных данных из Swagger UI"""
    
    print("🔄 ОБРАБОТКА РЕАЛЬНЫХ ДАННЫХ")
    print("=" * 35)
    
    # Загружаем реальные данные
    if not os.path.exists('real_swagger_data.json'):
        print("❌ Файл real_swagger_data.json не найден")
        print("   Сначала извлеките данные из Swagger UI")
        return None
    
    with open('real_swagger_data.json', 'r', encoding='utf-8') as f:
        real_data = json.load(f)
    
    print(f"📊 Загружено {len(real_data)} реальных эндпоинтов")
    
    # Статистика
    with_params = len([e for e in real_data.values() if e.get('parameters')])
    with_body = len([e for e in real_data.values() if e.get('requestBody')])
    with_responses = len([e for e in real_data.values() if e.get('responses')])
    
    print(f"   - С параметрами: {with_params}")
    print(f"   - С телом запроса: {with_body}")
    print(f"   - С ответами: {with_responses}")
    
    # Обновляем документацию
    update_documentation_with_real_data(real_data)
    
    return real_data

def update_documentation_with_real_data(real_data):
    """Обновление документации реальными данными"""
    
    print("📝 Обновление документации реальными данными...")
    
    # Загружаем категории
    with open('categorized_endpoints.json', 'r', encoding='utf-8') as f:
        categories = json.load(f)
    
    updated_count = 0
    
    for category, endpoints in categories.items():
        print(f"📂 Обновляем категорию: {category}")
        
        for endpoint in endpoints:
            method = endpoint['method']
            path = endpoint['path']
            endpoint_key = f"{method} {path}"
            
            if endpoint_key in real_data:
                real_endpoint = real_data[endpoint_key]
                
                # Генерируем улучшенную документацию
                enhanced_doc = generate_real_endpoint_documentation(real_endpoint)
                
                # Сохраняем
                filename = f"{method.lower()}_{path.replace('/', '_').replace('{', '').replace('}', '').replace('__', '_').strip('_')}.md"
                filepath = f"docs/endpoints/{category}/{filename}"
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(enhanced_doc)
                
                updated_count += 1
    
    print(f"✅ Обновлено {updated_count} файлов документации")

def generate_real_endpoint_documentation(endpoint_data):
    """Генерация документации на основе реальных данных"""
    
    method = endpoint_data['method']
    path = endpoint_data['path']
    summary = endpoint_data['summary']
    
    doc = f"""# {method} {path}

## Overview

**Description**: {summary}  
**Method**: `{method}`  
**Path**: `{path}`  
**Authentication**: Required (Bearer Token)

## Request

### Headers
```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
Accept: application/json
```

"""
    
    # Параметры
    if endpoint_data.get('parameters'):
        doc += "### Parameters\\n\\n"
        doc += "| Parameter | Type | Required | In | Description |\\n"
        doc += "|-----------|------|----------|----|-----------------|\\n"
        
        for param in endpoint_data['parameters']:
            required = "✅ Yes" if param['required'] else "❌ No"
            doc += f"| `{param['name']}` | {param['type']} | {required} | {param['in']} | {param['description']} |\\n"
        
        doc += "\\n"
    
    # Тело запроса
    if endpoint_data.get('requestBody'):
        body = endpoint_data['requestBody']
        doc += "### Request Body\\n\\n"
        doc += f"**Content-Type**: `{body['contentType']}`\\n\\n"
        
        if body.get('example'):
            doc += "**Real Example:**\\n```json\\n"
            doc += json.dumps(body['example'], indent=2, ensure_ascii=False)
            doc += "\\n```\\n\\n"
        
        if body.get('schema'):
            doc += "**Schema:**\\n```\\n"
            doc += str(body['schema'])
            doc += "\\n```\\n\\n"
    
    # Ответы
    if endpoint_data.get('responses'):
        doc += "## Responses\\n\\n"
        
        for status_code, response_data in endpoint_data['responses'].items():
            doc += f"### {status_code} - {response_data['description']}\\n\\n"
            
            if response_data.get('example'):
                doc += "**Real Example:**\\n```json\\n"
                doc += json.dumps(response_data['example'], indent=2, ensure_ascii=False)
                doc += "\\n```\\n\\n"
    
    # Практические примеры
    doc += f"""## Code Examples

### Python
```python
import requests
import os

API_KEY = os.getenv('binomPublic')
BASE_URL = "https://pierdun.com/public/api/v1"

headers = {{
    "Authorization": f"Bearer {{API_KEY}}",
    "Content-Type": "application/json"
}}

# Example request
response = requests.{method.lower()}(
    f"{{BASE_URL}}{path}",
    headers=headers"""
    
    if endpoint_data.get('requestBody') and endpoint_data['requestBody'].get('example'):
        doc += f""",
    json={json.dumps(endpoint_data['requestBody']['example'], indent=4)}"""
    
    doc += """
)

if response.status_code in [200, 201]:
    data = response.json()
    print("Success:", data)
else:
    print(f"Error: {response.status_code} - {response.text}")
```

### cURL
```bash
curl -X """ + method + """ \\
  -H "Authorization: Bearer $BINOM_API_KEY" \\
  -H "Content-Type: application/json" \\"""
    
    if endpoint_data.get('requestBody') and endpoint_data['requestBody'].get('example'):
        doc += f"""
  -d '{json.dumps(endpoint_data['requestBody']['example'])}' \\"""
    
    doc += f"""
  "https://pierdun.com{path}"
```

## AI Agent Notes

- **Real data extracted**: ✅ This documentation contains actual examples from Swagger UI
- **Tested parameters**: All parameters and schemas are from live API documentation
- **Error handling**: Implement proper status code checking
- **Rate limiting**: Add delays between requests to avoid API limits

---

*Documentation generated from real Binom API v2 Swagger specification*
"""
    
    return doc

if __name__ == "__main__":
    process_real_swagger_data()
'''
    
    with open('/home/ubuntu/binom-api-encyclopedia/process_real_data.py', 'w', encoding='utf-8') as f:
        f.write(processor_code)
    
    print("✅ Процессор реальных данных создан")

def main():
    """Главная функция"""
    
    print("🎯 СОЗДАНИЕ ИНСТРУМЕНТОВ ДЛЯ ИЗВЛЕЧЕНИЯ РЕАЛЬНЫХ ДАННЫХ")
    print("=" * 65)
    
    # Создаем JavaScript скрипт
    js_script = extract_real_endpoint_data()
    
    # Создаем процессор
    create_real_data_processor()
    
    print("\\n🎉 ИНСТРУМЕНТЫ ГОТОВЫ!")
    print("📋 Следующие шаги:")
    print("   1. Выполните JavaScript в консоли браузера")
    print("   2. Сохраните результат в real_swagger_data.json")
    print("   3. Запустите process_real_data.py")
    print("   4. Получите настоящую энциклопедию с реальными данными!")

if __name__ == "__main__":
    main()
