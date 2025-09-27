# PATCH /landing/{id}

## Restore landing page

**Method:** `PATCH`  
**Endpoint:** `/public/api/v1/landing/{id}`

## Description

Restore landing page

## Example Usage

### Python

```python
import requests

headers = {
    "api-key": "your_api_key_here",
    "Content-Type": "application/json"
}

response = requests.patch(
    "https://pierdun.com/public/api/v1/landing/{id}",
    headers=headers
)

print(response.status_code)
print(response.json())
```

### cURL

```bash
curl -X PATCH \
  "https://pierdun.com/public/api/v1/landing/{id}" \
  -H "api-key: your_api_key_here"
```

## Notes

- Use `api-key` header for authentication (NOT Bearer token)
- Expected success status code: `201`
- Handle 502 errors with retry logic for POST/PUT/PATCH operations
