# Update Generate

**Method:** `PUT`
**Path:** `/user/2fa/secret/generate`

## Description
Generate two-factor secrets for current user, when two-factor authentication is disabled

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
url = "https://pierdun.com/public/api/v1/user/2fa/secret/generate"

headers = {
    "api-key": api_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# No parameters needed

response = requests.put(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"Success: {type(data)} response")
else:
    print(f"Error: {response.status_code} - {response.text}")
```
### Curl
```__curl__
curl -X PUT "https://pierdun.com/public/api/v1/user/2fa/secret/generate" \
  -H "api-key: $binomPublic" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
```
