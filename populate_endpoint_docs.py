#!/usr/bin/env python3
"""
Populate all endpoint documentation files with detailed information
from COMPLETE_BINOM_API_ENCYCLOPEDIA.json
"""

import json
import os
from pathlib import Path
import re

def load_encyclopedia():
    """Load the complete encyclopedia data"""
    with open('COMPLETE_BINOM_API_ENCYCLOPEDIA.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def sanitize_filename(endpoint_path, method):
    """Convert endpoint path to filename"""
    # Remove leading slash and replace special chars
    clean_path = endpoint_path.strip('/')
    clean_path = re.sub(r'[{}]', '', clean_path)  # Remove braces
    clean_path = clean_path.replace('/', '_')
    clean_path = clean_path.replace('-', '_')
    return f"{method.lower()}_{clean_path}.md"

def format_parameters(params):
    """Format parameters for documentation"""
    if not params:
        return "No parameters required."
    
    formatted = []
    for param in params:
        name = param.get('name', 'unknown')
        param_type = param.get('type', 'string')
        required = param.get('required', False)
        description = param.get('description', 'No description available')
        
        req_text = "**Required**" if required else "Optional"
        formatted.append(f"- `{name}` ({param_type}) - {req_text} - {description}")
    
    return "\n".join(formatted)

def format_schema(schema):
    """Format JSON schema for documentation"""
    if not schema:
        return "```json\n{}\n```"
    
    if isinstance(schema, dict):
        return f"```json\n{json.dumps(schema, indent=2)}\n```"
    else:
        return f"```json\n{schema}\n```"

def format_examples(examples):
    """Format code examples"""
    if not examples:
        return ""
    
    formatted = []
    for lang, code in examples.items():
        formatted.append(f"### {lang.title()}\n\n```{lang.lower()}\n{code}\n```")
    
    return "\n\n".join(formatted)

def create_endpoint_doc(endpoint_data):
    """Create documentation content for an endpoint"""
    method = endpoint_data.get('method', 'GET')
    path = endpoint_data.get('path', '')
    summary = endpoint_data.get('summary', 'No summary available')
    description = endpoint_data.get('description', 'No description available')
    parameters = endpoint_data.get('parameters', [])
    request_schema = endpoint_data.get('request_schema', {})
    response_schema = endpoint_data.get('response_schema', {})
    examples = endpoint_data.get('examples', {})
    tags = endpoint_data.get('tags', [])
    
    doc = f"""# {method} {path}

## Summary
{summary}

## Description
{description}

## Tags
{', '.join(tags) if tags else 'No tags'}

## Parameters
{format_parameters(parameters)}

## Request Schema
{format_schema(request_schema)}

## Response Schema
{format_schema(response_schema)}

## Examples
{format_examples(examples)}

## Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request - Check required parameters (datePreset, timezone) |
| 401 | Unauthorized - Invalid API key |
| 403 | Forbidden - Check Bearer token format |
| 404 | Not Found - Resource doesn't exist |
| 418 | I'm a teapot - Binom-specific error |
| 500 | Internal Server Error |

## Notes for AI Agents

- Always include `datePreset` and `timezone` parameters for stats endpoints
- Use Bearer token authentication: `Authorization: Bearer {{binomPublic}}`
- Validate all IDs before making requests
- Handle pagination with `limit` and `offset` parameters
- Check response status codes and implement proper error handling

---
*Generated from Binom API Encyclopedia*
"""
    
    return doc

def find_endpoint_file(docs_path, endpoint_data):
    """Find the corresponding documentation file for an endpoint"""
    method = endpoint_data.get('method', 'GET')
    path = endpoint_data.get('path', '')
    
    filename = sanitize_filename(path, method)
    
    # Search in all subdirectories
    for root, dirs, files in os.walk(docs_path):
        if filename in files:
            return os.path.join(root, filename)
    
    return None

def populate_all_docs():
    """Populate all endpoint documentation files"""
    print("Loading encyclopedia data...")
    encyclopedia = load_encyclopedia()
    
    docs_path = Path("docs/endpoints")
    if not docs_path.exists():
        print(f"Error: {docs_path} directory not found!")
        return
    
    endpoints = encyclopedia.get('endpoints', [])
    print(f"Found {len(endpoints)} endpoints to document")
    
    populated_count = 0
    missing_files = []
    
    for endpoint in endpoints:
        file_path = find_endpoint_file(docs_path, endpoint)
        
        if file_path:
            try:
                doc_content = create_endpoint_doc(endpoint)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(doc_content)
                
                populated_count += 1
                print(f"✓ Populated: {file_path}")
                
            except Exception as e:
                print(f"✗ Error writing {file_path}: {e}")
        else:
            missing_files.append(f"{endpoint.get('method', 'GET')} {endpoint.get('path', '')}")
    
    print(f"\n=== SUMMARY ===")
    print(f"Total endpoints: {len(endpoints)}")
    print(f"Successfully populated: {populated_count}")
    print(f"Missing files: {len(missing_files)}")
    
    if missing_files:
        print("\nMissing files:")
        for missing in missing_files[:10]:  # Show first 10
            print(f"  - {missing}")
        if len(missing_files) > 10:
            print(f"  ... and {len(missing_files) - 10} more")

def create_category_indexes():
    """Create index files for each category"""
    print("\nCreating category indexes...")
    
    encyclopedia = load_encyclopedia()
    categories = encyclopedia.get('categories', {})
    
    docs_path = Path("docs/endpoints")
    
    for category_name, category_data in categories.items():
        category_path = docs_path / category_name
        if category_path.exists():
            readme_path = category_path / "README.md"
            
            content = f"""# {category_name.replace('_', ' ').title()} API

## Description
{category_data.get('description', 'No description available')}

## Endpoints
Total endpoints in this category: **{category_data.get('endpoints', 0)}**

## Key Features
{chr(10).join(f'- {feature}' for feature in category_data.get('key_features', []))}

## Files in this directory
"""
            
            # List all .md files except README.md
            md_files = [f for f in category_path.glob("*.md") if f.name != "README.md"]
            md_files.sort()
            
            for md_file in md_files:
                # Extract method and path from filename
                filename = md_file.stem
                parts = filename.split('_', 1)
                if len(parts) >= 2:
                    method = parts[0].upper()
                    path_part = parts[1].replace('_', '/')
                    content += f"- [{method} /{path_part}]({md_file.name})\n"
            
            content += f"""
---
*Part of the Complete Binom API Encyclopedia*
"""
            
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ Created index: {readme_path}")

if __name__ == "__main__":
    print("🚀 Starting Binom API Encyclopedia population...")
    populate_all_docs()
    create_category_indexes()
    print("\n✅ Documentation population completed!")
