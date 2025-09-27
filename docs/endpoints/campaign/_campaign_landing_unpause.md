# Update Unpause

**Method:** `PUT`
**Path:** `/campaign/landing/unpause`

## Description
Unpause landing in campaign.

## Parameters
No parameters.

## Request Body
```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Campaign name"
    },
    "trafficSourceId": {
      "type": "integer",
      "description": "Traffic source ID"
    },
    "cost": {
      "type": "number",
      "description": "Campaign cost"
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
url = "https://pierdun.com/public/api/v1/campaign/landing/unpause"

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
curl -X PUT "https://pierdun.com/public/api/v1/campaign/landing/unpause" \
  -H "api-key: $binomPublic" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
```
