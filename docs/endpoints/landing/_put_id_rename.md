# PUT /landing/{id}/rename

## Rename landing

**Method:** `PUT`  
**Endpoint:** `/public/api/v1/landing/{id}/rename`

## Description

Rename landing

## Request Body

**Content-Type:** `application/json`

```json
{
  "name": "Mobidea - Some goods"
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
    "name": "Mobidea - Some goods"
}

response = requests.put(
    "https://pierdun.com/public/api/v1/landing/{id}/rename",
    headers=headers,
    json=data
)

print(response.status_code)
print(response.json())
```

### cURL

```bash
curl -X PUT \
  "https://pierdun.com/public/api/v1/landing/{id}/rename" \
  -H "api-key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"name": "Mobidea - Some goods"}'
```

## Notes

- Use `api-key` header for authentication (NOT Bearer token)
- Expected success status code: `201`
- Handle 502 errors with retry logic for POST/PUT/PATCH operations
