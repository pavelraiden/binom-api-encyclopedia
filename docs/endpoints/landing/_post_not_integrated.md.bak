# POST /landing/not_integrated

## Create not integrated landing

**Method:** `POST`  
**Endpoint:** `/public/api/v1/landing/not_integrated`

## Description

Create not integrated landing

## Request Body

**Content-Type:** `application/json`

```json
{
  "name": "Land",
  "url": "http://example.com",
  "groupUuid": "ec02bd03-4504-46fa-aa35-5773dd8aed26",
  "languageCode": "RU"
}
```

## Response

### 201

```json
{
  "id": 1
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
    "name": "Land",
    "url": "http://example.com",
    "groupUuid": "ec02bd03-4504-46fa-aa35-5773dd8aed26",
    "languageCode": "RU"
}

response = requests.post(
    "https://pierdun.com/public/api/v1/landing/not_integrated",
    headers=headers,
    json=data
)

print(response.status_code)
print(response.json())
```

### cURL

```bash
curl -X POST \
  "https://pierdun.com/public/api/v1/landing/not_integrated" \
  -H "api-key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"name": "Land", "url": "http://example.com", "groupUuid": "ec02bd03-4504-46fa-aa35-5773dd8aed26", "languageCode": "RU"}'
```

## Notes

- Use `api-key` header for authentication (NOT Bearer token)
- Expected success status code: `201`
- Handle 502 errors with retry logic for POST/PUT/PATCH operations
