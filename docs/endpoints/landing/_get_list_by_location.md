# GET /landing/list/by_location

## Get landings by location

**Method:** `GET`  
**Endpoint:** `/public/api/v1/landing/list/by_location`

## Description

Get landings by location

## Parameters

- **startLocation**: `string (required)` (required)

## Response

### 200

```json
[
  {
    "id": 42,
    "name": "Landing name"
  }
]
```

## Example Usage

### Python

```python
import requests

headers = {
    "api-key": "your_api_key_here",
    "Content-Type": "application/json"
}

response = requests.get(
    "https://pierdun.com/public/api/v1/landing/list/by_location",
    headers=headers
)

print(response.status_code)
print(response.json())
```

### cURL

```bash
curl -X GET \
  "https://pierdun.com/public/api/v1/landing/list/by_location" \
  -H "api-key: your_api_key_here"
```

## Notes

- Use `api-key` header for authentication (NOT Bearer token)
- Expected success status code: `200`
- Handle 502 errors with retry logic for POST/PUT/PATCH operations
