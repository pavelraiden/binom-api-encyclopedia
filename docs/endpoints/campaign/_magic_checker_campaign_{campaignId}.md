# Delete Campaign

**Method:** `DELETE`
**Path:** `/magic_checker/campaign/{campaignId}`

## Description
Remove Magic Checker From Campaign.

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
url = "https://pierdun.com/public/api/v1/magic_checker/campaign/{campaignId}"

headers = {
    "api-key": api_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# No parameters needed

response = requests.delete(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"Success: {type(data)} response")
else:
    print(f"Error: {response.status_code} - {response.text}")
```
### Curl
```__curl__
curl -X DELETE "https://pierdun.com/public/api/v1/magic_checker/campaign/{campaignId}" \
  -H "api-key: $binomPublic" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
```
