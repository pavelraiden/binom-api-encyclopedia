# Create Settings

**Method:** `POST`
**Path:** `/migrator/v2/backup/settings`

## Description
Change auto backup settings. Interval counts in seconds.

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
url = "https://pierdun.com/public/api/v1/migrator/v2/backup/settings"

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
curl -X POST "https://pierdun.com/public/api/v1/migrator/v2/backup/settings" \
  -H "api-key: $binomPublic" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
```
