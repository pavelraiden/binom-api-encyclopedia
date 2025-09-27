# PUT /landing/{id}

## Edit landing

**Method:** `PUT`  
**Endpoint:** `/public/api/v1/landing/{id}`

## Description

Edit landing

## Request Body

**Content-Type:** `application/json`

```json
{
  "type": "integrated",
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
    "type": "integrated",
    "name": "New landing",
    "location": "http://example.com",
    "groupUuid": "ec02bd03-4504-46fa-aa35-5773dd8aed26",
    "languageCode": "RU"
}

response = requests.put(
    "https://pierdun.com/public/api/v1/landing/{id}",
    headers=headers,
    json=data
)

print(response.status_code)
print(response.json())
```

### cURL

```bash
curl -X PUT \
  "https://pierdun.com/public/api/v1/landing/{id}" \
  -H "api-key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"type": "integrated", "name": "New landing", "location": "http://example.com", "groupUuid": "ec02bd03-4504-46fa-aa35-5773dd8aed26", "languageCode": "RU"}'
```

## Notes

- Use `api-key` header for authentication (NOT Bearer token)
- Expected success status code: `201`
- Handle 502 errors with retry logic for POST/PUT/PATCH operations
