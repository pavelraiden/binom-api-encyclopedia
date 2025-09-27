# GET /landing/language/list

## Get Languages with landings list

**Method:** `GET`  
**Endpoint:** `/public/api/v1/landing/language/list`

## Description

Get Languages with landings list

## Response

### 200

```json
[
  {
    "code": "RU",
    "name": "Russian(RU)",
    "landingsCount": 9
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
    "https://pierdun.com/public/api/v1/landing/language/list",
    headers=headers
)

print(response.status_code)
print(response.json())
```

### cURL

```bash
curl -X GET \
  "https://pierdun.com/public/api/v1/landing/language/list" \
  -H "api-key: your_api_key_here"
```

## Notes

- Use `api-key` header for authentication (NOT Bearer token)
- Expected success status code: `200`
- Handle 502 errors with retry logic for POST/PUT/PATCH operations
