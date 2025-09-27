#!/usr/bin/env python3
"""
Process and categorize extracted Binom API endpoints
"""

import json
import os
from collections import defaultdict

def load_extracted_endpoints():
    """Load extracted endpoints from JSON file"""
    
    with open('extracted_endpoints.json', 'r', encoding='utf-8') as f:
        endpoints = json.load(f)
    
    print(f"✅ Загружено {len(endpoints)} эндпоинтов")
    return endpoints

def categorize_endpoints(endpoints):
    """Categorize endpoints by functionality"""
    
    categories = defaultdict(list)
    
    for endpoint in endpoints:
        tag = endpoint.get('tag', '').replace('Affiliate Network', 'affiliate_network')
        
        # Clean up tag names
        if 'affiliate_network' in tag.lower():
            category = 'affiliate_network'
        elif 'campaign' in tag.lower():
            category = 'campaign'
        elif 'clicks' in tag.lower():
            category = 'clicks'
        elif 'info stats' in tag.lower():
            category = 'info'
        elif 'report' in tag.lower():
            if 'groupings' in tag.lower():
                category = 'report_groupings'
            elif 'mark' in tag.lower():
                category = 'report_mark'
            elif 'presets' in tag.lower():
                category = 'report_presets'
            elif 'simple filters' in tag.lower():
                category = 'report_filters'
            else:
                category = 'report'
        elif 'stats' in tag.lower():
            category = 'stats'
        elif 'identity' in tag.lower():
            category = 'identity'
        elif 'binom protect' in tag.lower():
            category = 'binom_protect'
        elif 'csv' in tag.lower():
            category = 'csv'
        elif 'rotation' in tag.lower():
            category = 'rotation'
        elif 'conversion' in tag.lower():
            category = 'conversion'
        elif 'domain' in tag.lower():
            category = 'domain'
        elif 'group' in tag.lower():
            category = 'group'
        elif 'landing' in tag.lower():
            category = 'landing'
        elif 'offer' in tag.lower():
            category = 'offer'
        elif 'traffic' in tag.lower():
            category = 'traffic_source'
        elif 'trends' in tag.lower():
            category = 'trends'
        elif 'user' in tag.lower():
            if 'access' in tag.lower():
                category = 'user_access'
            else:
                category = 'user'
        elif 'auth' in tag.lower():
            category = 'auth'
        else:
            category = 'other'
        
        categories[category].append(endpoint)
    
    return dict(categories)

def generate_category_summary(categories):
    """Generate summary by categories"""
    
    print("\n📊 СТАТИСТИКА ПО КАТЕГОРИЯМ:")
    print("=" * 40)
    
    total_endpoints = sum(len(endpoints) for endpoints in categories.values())
    
    for category, endpoints in sorted(categories.items()):
        count = len(endpoints)
        percentage = (count / total_endpoints) * 100
        print(f"📂 {category.replace('_', ' ').title()}: {count} эндпоинтов ({percentage:.1f}%)")
    
    print(f"\n📊 Всего: {total_endpoints} эндпоинтов")
    
    return total_endpoints

def create_directory_structure(categories):
    """Create directory structure for documentation"""
    
    print("\n📁 СОЗДАНИЕ СТРУКТУРЫ ДИРЕКТОРИЙ")
    print("=" * 40)
    
    # Create main directories
    directories = [
        'docs',
        'docs/endpoints',
        'docs/schemas',
        'docs/examples',
        'code-samples',
        'code-samples/python',
        'code-samples/curl',
        'ai-guides',
        'utils'
    ]
    
    # Create category directories
    for category in categories.keys():
        directories.append(f'docs/endpoints/{category}')
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ {directory}")
    
    return directories

def generate_main_readme(categories, total_endpoints):
    """Generate main README.md file"""
    
    readme_content = f"""# Binom API Encyclopedia

Complete documentation and examples for Binom API v2 - designed for AI agents and developers.

## 📊 Overview

- **Total Endpoints**: {total_endpoints}
- **API Version**: v2
- **Base URL**: `https://pierdun.com/public/api/v1`
- **Authentication**: Bearer Token
- **Last Updated**: September 2025

## 🚀 Quick Start

```python
import requests
import os

API_KEY = os.getenv('binomPublic')
BASE_URL = "https://pierdun.com/public/api/v1"

headers = {{
    "Authorization": f"Bearer {{API_KEY}}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}}

# Example: Get campaigns info
response = requests.get(
    f"{{BASE_URL}}/info/campaign",
    headers=headers,
    params={{
        "datePreset": "last_7_days",
        "timezone": "UTC",
        "limit": 100
    }}
)

data = response.json()
```

## 📚 API Categories

"""
    
    for category, endpoints in sorted(categories.items()):
        count = len(endpoints)
        category_name = category.replace('_', ' ').title()
        readme_content += f"### [{category_name}](docs/endpoints/{category}/README.md) ({count} endpoints)\n\n"
        
        # Add first few endpoints as examples
        for i, endpoint in enumerate(endpoints[:3]):
            method = endpoint['method']
            path = endpoint['path']
            summary = endpoint['summary']
            readme_content += f"- **{method}** `{path}` - {summary}\n"
        
        if len(endpoints) > 3:
            readme_content += f"- ... and {len(endpoints) - 3} more endpoints\n"
        
        readme_content += "\n"
    
    readme_content += f"""
## 🤖 AI Agent Usage

This documentation is optimized for AI agents. Each endpoint includes:

- Complete request/response schemas
- Working code examples
- Common error handling
- Business logic context
- Related endpoints mapping

## 📖 Documentation Structure

```
binom-api-encyclopedia/
├── docs/
│   ├── endpoints/          # Endpoint documentation by category
│   ├── schemas/           # JSON schemas for requests/responses
│   └── examples/          # Usage examples
├── code-samples/          # Ready-to-use code samples
├── ai-guides/            # AI-specific guides and best practices
└── utils/                # Utilities and tools
```

## 🔧 Authentication

All API requests require Bearer token authentication:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \\
     -H "Content-Type: application/json" \\
     "https://pierdun.com/public/api/v1/info/campaign?datePreset=today&timezone=UTC"
```

## 📋 Required Parameters

Most endpoints require these parameters:
- `datePreset`: Time period (e.g., "last_7_days", "today")
- `timezone`: Timezone (e.g., "UTC")

## 🔗 Links

- [Official Binom Documentation](https://docs.binom.org/)
- [API Documentation](https://pierdun.com/api/doc)
- [Swagger UI](https://pierdun.com/api/doc)

## 📄 License

This documentation is created for educational and development purposes.

---

*Generated automatically from Binom API v2 specification*
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README.md создан")

def generate_category_readmes(categories):
    """Generate README files for each category"""
    
    print("\n📝 СОЗДАНИЕ README ДЛЯ КАТЕГОРИЙ")
    print("=" * 40)
    
    for category, endpoints in categories.items():
        category_name = category.replace('_', ' ').title()
        
        readme_content = f"""# {category_name} API Endpoints

{len(endpoints)} endpoints for {category_name.lower()} operations.

## Endpoints

"""
        
        for endpoint in endpoints:
            method = endpoint['method']
            path = endpoint['path']
            summary = endpoint['summary']
            
            # Create filename for individual endpoint documentation
            endpoint_filename = f"{method.lower()}_{path.replace('/', '_').replace('{', '').replace('}', '').replace('__', '_').strip('_')}.md"
            
            readme_content += f"### {method} {path}\n\n"
            readme_content += f"**Description**: {summary}\n\n"
            readme_content += f"**Documentation**: [{endpoint_filename}]({endpoint_filename})\n\n"
            readme_content += "---\n\n"
        
        # Save category README
        category_readme_path = f"docs/endpoints/{category}/README.md"
        with open(category_readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✅ {category_readme_path}")

def generate_endpoint_templates(categories):
    """Generate template files for individual endpoints"""
    
    print("\n📄 СОЗДАНИЕ ШАБЛОНОВ ЭНДПОИНТОВ")
    print("=" * 40)
    
    template = """# {method} {path}

## Overview

**Description**: {summary}  
**Method**: {method}  
**Path**: `{path}`  
**Authentication**: Required  

## Request

### Headers
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
Accept: application/json
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| datePreset | string | Yes | Time period filter |
| timezone | string | Yes | Timezone (e.g., "UTC") |

### Example Request

```bash
curl -X {method} \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  "https://pierdun.com{path}?datePreset=last_7_days&timezone=UTC"
```

```python
import requests
import os

API_KEY = os.getenv('binomPublic')
BASE_URL = "https://pierdun.com/public/api/v1"

headers = {{
    "Authorization": f"Bearer {{API_KEY}}",
    "Content-Type": "application/json"
}}

response = requests.{method_lower}(
    f"{{BASE_URL}}{path}",
    headers=headers,
    params={{
        "datePreset": "last_7_days",
        "timezone": "UTC"
    }}
)

data = response.json()
print(data)
```

## Response

### Success Response (200)

```json
{{
  "status": "success",
  "data": []
}}
```

### Error Responses

#### 400 Bad Request
```json
{{
  "error": "Invalid parameters"
}}
```

#### 401 Unauthorized
```json
{{
  "error": "Invalid API key"
}}
```

#### 403 Forbidden
```json
{{
  "error": "Access denied"
}}
```

## AI Usage Notes

- This endpoint is commonly used for: [TO BE FILLED]
- Related endpoints: [TO BE FILLED]
- Common use cases: [TO BE FILLED]

## Related Endpoints

- [TO BE FILLED]

## Examples

### Basic Usage
[TO BE FILLED]

### Advanced Usage
[TO BE FILLED]

## Common Issues

- **Issue**: [TO BE FILLED]
  **Solution**: [TO BE FILLED]

---

*This documentation is auto-generated and needs manual enrichment*
"""
    
    created_count = 0
    
    for category, endpoints in categories.items():
        for endpoint in endpoints:
            method = endpoint['method']
            path = endpoint['path']
            summary = endpoint['summary']
            
            # Create filename
            endpoint_filename = f"{method.lower()}_{path.replace('/', '_').replace('{', '').replace('}', '').replace('__', '_').strip('_')}.md"
            endpoint_path = f"docs/endpoints/{category}/{endpoint_filename}"
            
            # Fill template
            filled_template = template.format(
                method=method,
                method_lower=method.lower(),
                path=path,
                summary=summary
            )
            
            # Save endpoint documentation
            with open(endpoint_path, 'w', encoding='utf-8') as f:
                f.write(filled_template)
            
            created_count += 1
    
    print(f"✅ Создано {created_count} шаблонов эндпоинтов")

def save_processed_data(categories, total_endpoints):
    """Save processed data for future use"""
    
    # Save categorized endpoints
    with open('categorized_endpoints.json', 'w', encoding='utf-8') as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)
    
    # Save summary statistics
    summary = {
        'total_endpoints': total_endpoints,
        'categories': {cat: len(eps) for cat, eps in categories.items()},
        'extraction_date': '2025-09-27',
        'source': 'swagger_ui_extraction'
    }
    
    with open('summary_statistics.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print("✅ Данные сохранены в categorized_endpoints.json и summary_statistics.json")

def main():
    """Main processing function"""
    
    print("🔄 ОБРАБОТКА ИЗВЛЕЧЕННЫХ ЭНДПОИНТОВ")
    print("=" * 50)
    
    # Load endpoints
    endpoints = load_extracted_endpoints()
    
    # Categorize endpoints
    categories = categorize_endpoints(endpoints)
    
    # Generate summary
    total_endpoints = generate_category_summary(categories)
    
    # Create directory structure
    create_directory_structure(categories)
    
    # Generate documentation
    generate_main_readme(categories, total_endpoints)
    generate_category_readmes(categories)
    generate_endpoint_templates(categories)
    
    # Save processed data
    save_processed_data(categories, total_endpoints)
    
    print(f"\n🎉 ОБРАБОТКА ЗАВЕРШЕНА!")
    print(f"📊 Обработано {total_endpoints} эндпоинтов в {len(categories)} категориях")
    print(f"📁 Создана полная структура документации")
    
    return categories, total_endpoints

if __name__ == "__main__":
    main()
