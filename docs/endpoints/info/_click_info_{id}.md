# Get Info

**Method:** `GET`
**Path:** `/click/info/{id}`

## Description
Get click info by ID.

## Parameters
| Name | Type | Required | Description |
|---|---|---|---|
| datePreset | string | False | Time period for data filtering |
| timezone | string | False | Timezone for date calculations |
| id | integer | True | Resource ID |

## Request Body
No request body.

## Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "id": {
        "type": "integer",
        "description": "Resource ID"
      },
      "name": {
        "type": "string",
        "description": "Resource name"
      }
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
url = "https://pierdun.com/public/api/v1/click/info/{id}"

headers = {
    "api-key": api_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

params = {
    "datePreset": "last_7_days",
    "timezone": "UTC"
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print(f"Success: {type(data)} response")
else:
    print(f"Error: {response.status_code} - {response.text}")
```
### Curl
```__curl__
curl -X GET "https://pierdun.com/public/api/v1/click/info/{id}?datePreset=last_7_days&timezone=UTC" \
  -H "api-key: $binomPublic" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
```
