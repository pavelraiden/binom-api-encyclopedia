# Create Change Group

**Method:** `POST`
**Path:** `/offer/change_group`

## Description
Change Group for multiple offers

## Parameters
No parameters.

## Request Body
```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Offer name"
    },
    "url": {
      "type": "string",
      "description": "Offer URL"
    },
    "payout": {
      "type": "number",
      "description": "Offer payout"
    }
  }
}
```

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
url = "https://pierdun.com/public/api/v1/offer/change_group"

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
curl -X POST "https://pierdun.com/public/api/v1/offer/change_group" \
  -H "api-key: $binomPublic" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
```
