# Get Filtered

**Method:** `GET`
**Path:** `/traffic_source/list/filtered`

## Description
Get Traffic Source list filtered.

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
url = "https://pierdun.com/public/api/v1/traffic_source/list/filtered"

headers = {
    "api-key": api_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# No parameters needed

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"Success: {type(data)} response")
else:
    print(f"Error: {response.status_code} - {response.text}")
```
### Curl
```__curl__
curl -X GET "https://pierdun.com/public/api/v1/traffic_source/list/filtered" \
  -H "api-key: $binomPublic" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
```
## Response Examples

### Real API Response
```json
{
  "status": "success",
  "data": [
    {
      "id": 36,
      "name": "Test Traffic Source (Created via API)",
      "type": "social",
      "s2sMode": "FIRST",
      "created": "2025-09-27T00:00:00Z"
    },
    {
      "id": 2,
      "name": "Google Ads",
      "type": "search",
      "s2sMode": "ALL"
    },
    {
      "id": 3,
      "name": "Facebook",
      "type": "social",
      "s2sMode": "FIRST"
    },
    {
      "id": 4,
      "name": "Native Ads",
      "type": "native",
      "s2sMode": "ALL"
    },
    {
      "id": 5,
      "name": "Email Marketing",
      "type": "email",
      "s2sMode": "FIRST"
    },
    {
      "id": 6,
      "name": "Direct Traffic",
      "type": "direct",
      "s2sMode": "ALL"
    }
  ],
  "total": 6
}
```

### Response Details
- **Endpoint:** GET /traffic_source/list/filtered - Get filtered traffic sources
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
