# POST /offer

**Method:** `POST`
**Path:** `/offer`

## Description
Create Offer.

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
url = "https://pierdun.com/public/api/v1/offer"

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
curl -X POST "https://pierdun.com/public/api/v1/offer" \
  -H "api-key: $binomPublic" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
```



**WARNING: This endpoint is currently unstable.**

As of September 2025, the `POST /offer` endpoint consistently returns a `500 Internal Server Error` with the message `strtoupper(): Argument #1 ($string) must be of type string, null given`. This indicates a server-side issue, likely caused by a missing, undocumented, mandatory string field in the request.

We have submitted a bug report to the Binom team and are awaiting a fix or updated documentation. We advise against using this endpoint until the issue is resolved. Please refer to our [bug report](/docs/bug_reports/post_offer_500_error.md) for more details.

