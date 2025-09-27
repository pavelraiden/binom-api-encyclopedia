# GET /landing/{id}/file

## Get landing file content

**Method:** `GET`  
**Endpoint:** `/public/api/v1/landing/{id}/file`

## Description

Get landing file content

## Response

### 200

```json
{
  "content": "<html>..."
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
    "https://pierdun.com/public/api/v1/landing/{id}/file",
    headers=headers
)

print(response.status_code)
print(response.json())
```

### cURL

```bash
curl -X GET \
  "https://pierdun.com/public/api/v1/landing/{id}/file" \
  -H "api-key: your_api_key_here"
```

## Notes

- Use `api-key` header for authentication (NOT Bearer token)
- Expected success status code: `200`
- Handle 502 errors with retry logic for POST/PUT/PATCH operations
