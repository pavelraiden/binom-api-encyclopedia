# Create Note

**Method:** `POST`
**Path:** `/note/{uuid}`

## Description
Create Note. uuid: You need generate uuid version 4 any generator. For example this: https://www.uuidgenerator.net/version4 Format looks like this: 0acc95cc-ad7a-48e5-9bdc-c4b86de6c620

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
url = "https://pierdun.com/public/api/v1/note/{uuid}"

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
curl -X POST "https://pierdun.com/public/api/v1/note/{uuid}" \
  -H "api-key: $binomPublic" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
```
