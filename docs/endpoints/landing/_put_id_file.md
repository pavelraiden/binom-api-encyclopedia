# PUT /landing/{id}/file

## Edit landing file

**Method:** `PUT`  
**Endpoint:** `/public/api/v1/landing/{id}/file`

## Description

Edit landing file

## Request Body

**Content-Type:** `application/json`

```json
{
  "content": "<html>..."
}
```

## Response

### 201

```json
{
  "landing_file": "landers/ec02bd03-4504-46fa-aa35-5773dd8aed42/index.html"
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
    "content": "<html>..."
}

response = requests.put(
    "https://pierdun.com/public/api/v1/landing/{id}/file",
    headers=headers,
    json=data
)

print(response.status_code)
print(response.json())
```

### cURL

```bash
curl -X PUT \
  "https://pierdun.com/public/api/v1/landing/{id}/file" \
  -H "api-key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"content": "<html>..."}'
```

## Notes

- Use `api-key` header for authentication (NOT Bearer token)
- Expected success status code: `201`
- Handle 502 errors with retry logic for POST/PUT/PATCH operations
