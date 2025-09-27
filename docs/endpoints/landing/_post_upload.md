# POST /landing/upload

## Upload landing files

**Method:** `POST`  
**Endpoint:** `/public/api/v1/landing/upload`

## Description

Upload landing files

## Request Body

**Content-Type:** `multipart/form-data`

```json
{
  "file": "string($file) - Landing File"
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
    "file": "string($file) - Landing File"
}

response = requests.post(
    "https://pierdun.com/public/api/v1/landing/upload",
    headers=headers,
    json=data
)

print(response.status_code)
print(response.json())
```

### cURL

```bash
curl -X POST \
  "https://pierdun.com/public/api/v1/landing/upload" \
  -H "api-key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"file": "string($file) - Landing File"}'
```

## Notes

- Use `api-key` header for authentication (NOT Bearer token)
- Expected success status code: `201`
- Handle 502 errors with retry logic for POST/PUT/PATCH operations
