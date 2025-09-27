# POST /landing/integrated

## Create integrated landing

**Method:** `POST`  
**Endpoint:** `/public/api/v1/landing/integrated`

## Description

Create integrated landing

## Request Body

**Content-Type:** `application/json`

```json
{
  "name": "Land",
  "path": "landers/ec02bd03-4504-46fa-aa35-5773dd8aed42/index.html",
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
    "path": "landers/ec02bd03-4504-46fa-aa35-5773dd8aed42/index.html",
    "groupUuid": "ec02bd03-4504-46fa-aa35-5773dd8aed26",
    "languageCode": "RU"
}

response = requests.post(
    "https://pierdun.com/public/api/v1/landing/integrated",
    headers=headers,
    json=data
)

print(response.status_code)
print(response.json())
```

### cURL

```bash
curl -X POST \
  "https://pierdun.com/public/api/v1/landing/integrated" \
  -H "api-key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"name": "Land", "path": "landers/ec02bd03-4504-46fa-aa35-5773dd8aed42/index.html", "groupUuid": "ec02bd03-4504-46fa-aa35-5773dd8aed26", "languageCode": "RU"}'
```

## Notes

- Use `api-key` header for authentication (NOT Bearer token)
- Expected success status code: `201`
- Handle 502 errors with retry logic for POST/PUT/PATCH operations
## Response Examples

### Real API Response
```json
{
  "status": "error",
  "error": {
    "code": 502,
    "message": "Bad Gateway",
    "details": "Server temporarily unavailable. Please retry in 5-10 seconds."
  }
}
```

### Response Details
- **Status Code:** 400
- **Content-Type:** application/json
- **Response Time:** ~200-500ms

### Common Errors
```json
{
  "status": "error",
  "error": {
    "code": 401,
    "message": "Unauthorized",
    "details": "Use 'api-key' header, NOT 'Authorization: Bearer'"
  }
}
```

**Note:** Always use `api-key` header for authentication, NOT `Authorization: Bearer`.
