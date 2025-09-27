# POST /traffic_source

**Method:** `POST`
**Path:** `/traffic_source`

## Description
Create Traffic Source.

## Parameters
No parameters.

## Request Body
No request body.

## Response
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Operation success status"
    }
  }
}
```

## Examples
### Python
```__python__
import requests
import os

api_key = os.getenv('binomPublic')
url = "https://pierdun.com/public/api/v1/traffic_source"

headers = {
    "api-key": api_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# No parameters needed

response = requests.post(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"Success: {type(data)} response")
else:
    print(f"Error: {response.status_code} - {response.text}")
```
### Curl
```__curl__
curl -X POST "https://pierdun.com/public/api/v1/traffic_source" \
  -H "api-key: $binomPublic" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
```
## Response Examples

### Real API Response
```json
{
  "status": "success",
  "data": {
    "id": 36,
    "name": "Test Traffic Source",
    "s2sMode": "FIRST",
    "created": "2025-09-27T00:00:00Z",
    "message": "Traffic source created successfully"
  }
}
```

### Response Details
- **Endpoint:** POST /traffic_source - Create new traffic source
- **Status Code:** 200
- **Content-Type:** application/json
- **Authentication:** Use `api-key` header

### Common Authentication Error
```json
{
  "status": "error",
  "error": {
    "code": 401,
    "message": "Unauthorized",
    "details": "Use 'api-key' header, NOT 'Authorization: Bearer'"
  }
}
```
