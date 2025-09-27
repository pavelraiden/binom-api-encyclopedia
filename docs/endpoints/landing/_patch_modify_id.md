# PATCH /landing/modify/{id}

## Partially update landing

**Method:** `PATCH`  
**Endpoint:** `/public/api/v1/landing/modify/{id}`

## Description

to clear groupUuid or languageCode use 'none', 'erase' or 'empty'

## Request Body

**Content-Type:** `application/json`

```json
{
  "name": "New landing",
  "location": "http://example.com",
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

data = {
    "name": "New landing",
    "location": "http://example.com",
    "groupUuid": "ec02bd03-4504-46fa-aa35-5773dd8aed26",
    "languageCode": "RU"
}

response = requests.patch(
    "https://pierdun.com/public/api/v1/landing/modify/{id}",
    headers=headers,
    json=data
)

print(response.status_code)
print(response.json())
```

### cURL

```bash
curl -X PATCH \
  "https://pierdun.com/public/api/v1/landing/modify/{id}" \
  -H "api-key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"name": "New landing", "location": "http://example.com", "groupUuid": "ec02bd03-4504-46fa-aa35-5773dd8aed26", "languageCode": "RU"}'
```

## Notes

- Use `api-key` header for authentication (NOT Bearer token)
- Expected success status code: `201`
- Handle 502 errors with retry logic for POST/PUT/PATCH operations
