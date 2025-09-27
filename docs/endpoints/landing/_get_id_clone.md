# GET /landing/{id}/clone

## Clone landing

**Method:** `GET`  
**Endpoint:** `/public/api/v1/landing/{id}/clone`

## Description

Clone landing

## Response

### 200

```json
{
  "type": "integrated",
  "name": "New landing",
  "location": "https://example.com or landers/23dw2323d/index.html",
  "groupUuid": "ec02bd03-4504-46fa-aa35-5773dd8aed26",
  "languageCode": "RU"
}
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
    "https://pierdun.com/public/api/v1/landing/{id}/clone",
    headers=headers
)

print(response.status_code)
print(response.json())
```

### cURL

```bash
curl -X GET \
  "https://pierdun.com/public/api/v1/landing/{id}/clone" \
  -H "api-key: your_api_key_here"
```

## Notes

- Use `api-key` header for authentication (NOT Bearer token)
- Expected success status code: `200`
- Handle 502 errors with retry logic for POST/PUT/PATCH operations
