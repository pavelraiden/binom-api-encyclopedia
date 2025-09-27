#!/usr/bin/env python3
"""
Extract detailed endpoint information from Binom API Swagger UI
Including parameters, request/response schemas, examples, etc.
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

def setup_browser():
    """Setup Chrome browser for Swagger UI interaction"""
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def extract_endpoint_details(driver, endpoint_data):
    """Extract detailed information for a specific endpoint"""
    
    method = endpoint_data['method']
    path = endpoint_data['path']
    
    print(f"🔍 Извлекаем детали для {method} {path}")
    
    try:
        # Find the endpoint section by method and path
        endpoint_selector = f"//div[contains(@class, 'opblock') and .//span[text()='{method}'] and .//a[contains(text(), '{path}')]]"
        endpoint_element = driver.find_element(By.XPATH, endpoint_selector)
        
        # Click to expand the endpoint if not already expanded
        try:
            expand_button = endpoint_element.find_element(By.CSS_SELECTOR, ".opblock-summary")
            if "is-open" not in endpoint_element.get_attribute("class"):
                expand_button.click()
                time.sleep(1)
        except:
            pass
        
        details = {
            'method': method,
            'path': path,
            'summary': endpoint_data.get('summary', ''),
            'parameters': [],
            'request_body': {},
            'responses': {},
            'examples': {}
        }
        
        # Extract parameters
        try:
            params_section = endpoint_element.find_element(By.CSS_SELECTOR, ".parameters-container")
            param_rows = params_section.find_elements(By.CSS_SELECTOR, ".parameter__name")
            
            for param_row in param_rows:
                try:
                    param_name = param_row.text.strip()
                    param_container = param_row.find_element(By.XPATH, "./ancestor::tr")
                    
                    # Get parameter type
                    param_type = "string"
                    try:
                        type_element = param_container.find_element(By.CSS_SELECTOR, ".parameter__type")
                        param_type = type_element.text.strip()
                    except:
                        pass
                    
                    # Check if required
                    is_required = False
                    try:
                        required_element = param_container.find_element(By.CSS_SELECTOR, ".parameter__name .required")
                        is_required = True
                    except:
                        pass
                    
                    # Get description
                    description = ""
                    try:
                        desc_element = param_container.find_element(By.CSS_SELECTOR, ".parameter__description")
                        description = desc_element.text.strip()
                    except:
                        pass
                    
                    details['parameters'].append({
                        'name': param_name,
                        'type': param_type,
                        'required': is_required,
                        'description': description
                    })
                    
                except Exception as e:
                    print(f"  ⚠️ Ошибка извлечения параметра: {e}")
                    continue
                    
        except NoSuchElementException:
            print(f"  ℹ️ Параметры не найдены для {method} {path}")
        
        # Extract request body schema
        try:
            request_section = endpoint_element.find_element(By.CSS_SELECTOR, ".request-body")
            
            # Try to get example value
            try:
                example_button = request_section.find_element(By.XPATH, ".//button[contains(text(), 'Example Value')]")
                example_button.click()
                time.sleep(0.5)
                
                example_element = request_section.find_element(By.CSS_SELECTOR, ".highlight-code pre")
                example_text = example_element.text.strip()
                
                if example_text:
                    try:
                        details['request_body']['example'] = json.loads(example_text)
                    except:
                        details['request_body']['example'] = example_text
                        
            except:
                pass
            
            # Try to get schema
            try:
                schema_button = request_section.find_element(By.XPATH, ".//button[contains(text(), 'Schema')]")
                schema_button.click()
                time.sleep(0.5)
                
                schema_element = request_section.find_element(By.CSS_SELECTOR, ".model-box")
                schema_text = schema_element.text.strip()
                details['request_body']['schema'] = schema_text
                
            except:
                pass
                
        except NoSuchElementException:
            pass
        
        # Extract responses
        try:
            responses_section = endpoint_element.find_element(By.CSS_SELECTOR, ".responses-wrapper")
            response_items = responses_section.find_elements(By.CSS_SELECTOR, ".response")
            
            for response_item in response_items:
                try:
                    # Get status code
                    status_code = response_item.find_element(By.CSS_SELECTOR, ".response-col_status").text.strip()
                    
                    # Get description
                    description = ""
                    try:
                        desc_element = response_item.find_element(By.CSS_SELECTOR, ".response-col_description")
                        description = desc_element.text.strip()
                    except:
                        pass
                    
                    response_data = {
                        'description': description,
                        'example': None,
                        'schema': None
                    }
                    
                    # Try to get example
                    try:
                        example_section = response_item.find_element(By.CSS_SELECTOR, ".highlight-code pre")
                        example_text = example_section.text.strip()
                        
                        if example_text:
                            try:
                                response_data['example'] = json.loads(example_text)
                            except:
                                response_data['example'] = example_text
                    except:
                        pass
                    
                    details['responses'][status_code] = response_data
                    
                except Exception as e:
                    print(f"  ⚠️ Ошибка извлечения ответа: {e}")
                    continue
                    
        except NoSuchElementException:
            print(f"  ℹ️ Ответы не найдены для {method} {path}")
        
        return details
        
    except Exception as e:
        print(f"  ❌ Ошибка извлечения деталей для {method} {path}: {e}")
        return None

def extract_all_endpoint_details():
    """Extract detailed information for all endpoints"""
    
    print("🚀 ИЗВЛЕЧЕНИЕ ДЕТАЛЬНОЙ ИНФОРМАЦИИ ОБ ЭНДПОИНТАХ")
    print("=" * 60)
    
    # Load existing endpoints
    with open('extracted_endpoints.json', 'r', encoding='utf-8') as f:
        endpoints = json.load(f)
    
    print(f"📊 Загружено {len(endpoints)} эндпоинтов для детального анализа")
    
    # Setup browser
    print("🌐 Настройка браузера...")
    driver = setup_browser()
    
    try:
        # Navigate to Swagger UI
        print("📡 Переход к Swagger UI...")
        driver.get("https://pierdun.com/api/doc")
        
        # Wait for page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".swagger-ui"))
        )
        
        print("✅ Swagger UI загружен")
        
        detailed_endpoints = []
        
        # Process each endpoint
        for i, endpoint in enumerate(endpoints):
            print(f"\n📋 Обрабатываем {i+1}/{len(endpoints)}: {endpoint['method']} {endpoint['path']}")
            
            details = extract_endpoint_details(driver, endpoint)
            
            if details:
                detailed_endpoints.append(details)
                print(f"  ✅ Извлечено: {len(details['parameters'])} параметров, {len(details['responses'])} ответов")
            else:
                print(f"  ❌ Не удалось извлечь детали")
            
            # Small delay to avoid overwhelming the server
            time.sleep(0.5)
            
            # Save progress every 20 endpoints
            if (i + 1) % 20 == 0:
                print(f"💾 Сохранение промежуточного результата ({i+1} эндпоинтов)...")
                with open(f'detailed_endpoints_progress_{i+1}.json', 'w', encoding='utf-8') as f:
                    json.dump(detailed_endpoints, f, ensure_ascii=False, indent=2)
        
        # Save final results
        print(f"\n💾 Сохранение финальных результатов...")
        with open('detailed_endpoints.json', 'w', encoding='utf-8') as f:
            json.dump(detailed_endpoints, f, ensure_ascii=False, indent=2)
        
        print(f"🎉 ИЗВЛЕЧЕНИЕ ЗАВЕРШЕНО!")
        print(f"📊 Обработано {len(detailed_endpoints)} эндпоинтов с детальной информацией")
        
        return detailed_endpoints
        
    finally:
        driver.quit()

def generate_enhanced_documentation(detailed_endpoints):
    """Generate enhanced documentation with detailed information"""
    
    print("\n📝 ГЕНЕРАЦИЯ УЛУЧШЕННОЙ ДОКУМЕНТАЦИИ")
    print("=" * 45)
    
    # Load categorized endpoints
    with open('categorized_endpoints.json', 'r', encoding='utf-8') as f:
        categories = json.load(f)
    
    # Create mapping of endpoints to details
    details_map = {}
    for detail in detailed_endpoints:
        key = f"{detail['method']}:{detail['path']}"
        details_map[key] = detail
    
    enhanced_count = 0
    
    # Update each category's documentation
    for category, endpoints in categories.items():
        print(f"📂 Обновляем категорию: {category}")
        
        for endpoint in endpoints:
            method = endpoint['method']
            path = endpoint['path']
            key = f"{method}:{path}"
            
            if key in details_map:
                detail = details_map[key]
                
                # Generate enhanced endpoint documentation
                endpoint_filename = f"{method.lower()}_{path.replace('/', '_').replace('{', '').replace('}', '').replace('__', '_').strip('_')}.md"
                endpoint_path = f"docs/endpoints/{category}/{endpoint_filename}"
                
                enhanced_doc = generate_enhanced_endpoint_doc(detail)
                
                with open(endpoint_path, 'w', encoding='utf-8') as f:
                    f.write(enhanced_doc)
                
                enhanced_count += 1
    
    print(f"✅ Обновлено {enhanced_count} файлов документации")
    
    # Generate schemas directory
    generate_schemas_directory(detailed_endpoints)
    
    # Generate examples directory
    generate_examples_directory(detailed_endpoints)

def generate_enhanced_endpoint_doc(detail):
    """Generate enhanced documentation for a single endpoint"""
    
    method = detail['method']
    path = detail['path']
    summary = detail['summary']
    
    doc = f"""# {method} {path}

## Overview

**Description**: {summary}  
**Method**: {method}  
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
    
    # Add parameters section
    if detail['parameters']:
        doc += "### Parameters\n\n"
        doc += "| Parameter | Type | Required | Description |\n"
        doc += "|-----------|------|----------|-------------|\n"
        
        for param in detail['parameters']:
            required = "✅ Yes" if param['required'] else "❌ No"
            doc += f"| {param['name']} | {param['type']} | {required} | {param['description']} |\n"
        
        doc += "\n"
    
    # Add request body section
    if detail['request_body']:
        doc += "### Request Body\n\n"
        
        if 'example' in detail['request_body']:
            doc += "**Example:**\n```json\n"
            if isinstance(detail['request_body']['example'], dict):
                doc += json.dumps(detail['request_body']['example'], indent=2, ensure_ascii=False)
            else:
                doc += str(detail['request_body']['example'])
            doc += "\n```\n\n"
        
        if 'schema' in detail['request_body']:
            doc += "**Schema:**\n```\n"
            doc += detail['request_body']['schema']
            doc += "\n```\n\n"
    
    # Add example requests
    doc += f"""### Example Request

**cURL:**
```bash
curl -X {method} \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  "https://pierdun.com{path}?datePreset=last_7_days&timezone=UTC"
```

**Python:**
```python
import requests
import os

API_KEY = os.getenv('binomPublic')
BASE_URL = "https://pierdun.com/public/api/v1"

headers = {{
    "Authorization": f"Bearer {{API_KEY}}",
    "Content-Type": "application/json"
}}

response = requests.{method.lower()}(
    f"{{BASE_URL}}{path}",
    headers=headers,
    params={{
        "datePreset": "last_7_days",
        "timezone": "UTC"
    }}
)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {{response.status_code}} - {{response.text}}")
```

## Response

"""
    
    # Add responses section
    if detail['responses']:
        for status_code, response_data in detail['responses'].items():
            doc += f"### {status_code} Response\n\n"
            doc += f"**Description**: {response_data['description']}\n\n"
            
            if response_data['example']:
                doc += "**Example:**\n```json\n"
                if isinstance(response_data['example'], dict):
                    doc += json.dumps(response_data['example'], indent=2, ensure_ascii=False)
                else:
                    doc += str(response_data['example'])
                doc += "\n```\n\n"
    
    # Add common error responses if not present
    if '400' not in detail['responses']:
        doc += """### 400 Bad Request
```json
{
  "error": "Invalid parameters. Check datePreset and timezone."
}
```

"""
    
    if '401' not in detail['responses']:
        doc += """### 401 Unauthorized
```json
{
  "error": "Invalid API key"
}
```

"""
    
    if '403' not in detail['responses']:
        doc += """### 403 Forbidden
```json
{
  "error": "Access denied"
}
```

"""
    
    doc += """## AI Usage Notes

This endpoint can be used for:
- [Specific use case based on endpoint functionality]
- [Integration with other endpoints]
- [Common automation scenarios]

## Related Endpoints

- [List of related endpoints]

## Best Practices

- Always include required parameters: `datePreset` and `timezone`
- Use pagination for large datasets (`limit` and `offset`)
- Handle rate limiting with appropriate delays
- Validate response status codes before processing data

---

*Documentation generated from Binom API Swagger specification*
"""
    
    return doc

def generate_schemas_directory(detailed_endpoints):
    """Generate JSON schemas for requests and responses"""
    
    print("📋 Генерация JSON схем...")
    
    os.makedirs('docs/schemas', exist_ok=True)
    
    schemas = {}
    
    for detail in detailed_endpoints:
        endpoint_key = f"{detail['method'].lower()}_{detail['path'].replace('/', '_').replace('{', '').replace('}', '').replace('__', '_').strip('_')}"
        
        endpoint_schemas = {}
        
        # Request schema
        if detail['request_body']:
            endpoint_schemas['request'] = detail['request_body']
        
        # Response schemas
        if detail['responses']:
            endpoint_schemas['responses'] = detail['responses']
        
        if endpoint_schemas:
            schemas[endpoint_key] = endpoint_schemas
    
    # Save schemas
    with open('docs/schemas/all_schemas.json', 'w', encoding='utf-8') as f:
        json.dump(schemas, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Сохранено {len(schemas)} схем в docs/schemas/all_schemas.json")

def generate_examples_directory(detailed_endpoints):
    """Generate working code examples"""
    
    print("💻 Генерация примеров кода...")
    
    os.makedirs('code-samples/python', exist_ok=True)
    os.makedirs('code-samples/curl', exist_ok=True)
    
    # Generate Python examples
    python_examples = []
    curl_examples = []
    
    for detail in detailed_endpoints:
        method = detail['method']
        path = detail['path']
        
        # Python example
        python_code = f'''#!/usr/bin/env python3
"""
Example usage of {method} {path}
{detail['summary']}
"""

import requests
import os
import json

def {method.lower()}_{path.replace('/', '_').replace('{', '').replace('}', '').replace('__', '_').strip('_')}():
    """
    {detail['summary']}
    """
    
    API_KEY = os.getenv('binomPublic')
    BASE_URL = "https://pierdun.com/public/api/v1"
    
    headers = {{
        "Authorization": f"Bearer {{API_KEY}}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }}
    
    params = {{
        "datePreset": "last_7_days",
        "timezone": "UTC"
    }}
'''
        
        # Add specific parameters if available
        if detail['parameters']:
            python_code += "\n    # Additional parameters:\n"
            for param in detail['parameters']:
                if param['name'] not in ['datePreset', 'timezone']:
                    python_code += f"    # params['{param['name']}'] = {param['type']}  # {param['description']}\n"
        
        python_code += f'''
    
    try:
        response = requests.{method.lower()}(
            f"{{BASE_URL}}{path}",
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return data
        else:
            print(f"❌ Error: {{response.status_code}} - {{response.text}}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {{e}}")
        return None

if __name__ == "__main__":
    result = {method.lower()}_{path.replace('/', '_').replace('{', '').replace('}', '').replace('__', '_').strip('_')}()
'''
        
        python_examples.append({
            'filename': f"{method.lower()}_{path.replace('/', '_').replace('{', '').replace('}', '').replace('__', '_').strip('_')}.py",
            'code': python_code
        })
        
        # cURL example
        curl_code = f'''#!/bin/bash
# {detail['summary']}
# {method} {path}

curl -X {method} \\
  -H "Authorization: Bearer $BINOM_API_KEY" \\
  -H "Content-Type: application/json" \\
  -H "Accept: application/json" \\
  "https://pierdun.com{path}?datePreset=last_7_days&timezone=UTC"
'''
        
        curl_examples.append({
            'filename': f"{method.lower()}_{path.replace('/', '_').replace('{', '').replace('}', '').replace('__', '_').strip('_')}.sh",
            'code': curl_code
        })
    
    # Save Python examples
    for example in python_examples:
        with open(f"code-samples/python/{example['filename']}", 'w', encoding='utf-8') as f:
            f.write(example['code'])
    
    # Save cURL examples
    for example in curl_examples:
        with open(f"code-samples/curl/{example['filename']}", 'w', encoding='utf-8') as f:
            f.write(example['code'])
    
    print(f"✅ Создано {len(python_examples)} Python примеров")
    print(f"✅ Создано {len(curl_examples)} cURL примеров")

def main():
    """Main function"""
    
    # Extract detailed endpoint information
    detailed_endpoints = extract_all_endpoint_details()
    
    if detailed_endpoints:
        # Generate enhanced documentation
        generate_enhanced_documentation(detailed_endpoints)
        
        print(f"\n🎉 ДЕТАЛЬНОЕ ИЗВЛЕЧЕНИЕ ЗАВЕРШЕНО!")
        print(f"📊 Обработано {len(detailed_endpoints)} эндпоинтов")
        print(f"📝 Создана улучшенная документация с примерами и схемами")
    else:
        print("❌ Не удалось извлечь детальную информацию")

if __name__ == "__main__":
    main()
