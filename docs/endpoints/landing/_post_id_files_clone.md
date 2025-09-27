# POST /landing/{id}/files/clone

## Clone landing files

**Method:** `POST`  
**Endpoint:** `/public/api/v1/landing/{id}/files/clone`

## Description

Clone landing files

## Response

### 201

```json
{
  "location": "landers/23dw2323d/index.html"
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

response = requests.post(
    "https://pierdun.com/public/api/v1/landing/{id}/files/clone",
    headers=headers
)

print(response.status_code)
print(response.json())
```

### cURL

```bash
curl -X POST \
  "https://pierdun.com/public/api/v1/landing/{id}/files/clone" \
  -H "api-key: your_api_key_here"
```

## Notes

- Use `api-key` header for authentication (NOT Bearer token)
- Expected success status code: `201`
- Handle 502 errors with retry logic for POST/PUT/PATCH operations
