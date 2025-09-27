# POST /landing/change_domain

## Change Domain for multiple Landings

**Method:** `POST`  
**Endpoint:** `/public/api/v1/landing/change_domain`

## Description

Change Domain for multiple Landings

## Request Body

**Content-Type:** `application/json`

```json
{
  "ids": [
    1
  ],
  "domain": "example.com"
}
```

## Response

### 200

```json
{
  "failedIds": [
    1
  ]
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
    "ids": [
        1
    ],
    "domain": "example.com"
}

response = requests.post(
    "https://pierdun.com/public/api/v1/landing/change_domain",
    headers=headers,
    json=data
)

print(response.status_code)
print(response.json())
```

### cURL

```bash
curl -X POST \
  "https://pierdun.com/public/api/v1/landing/change_domain" \
  -H "api-key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"ids": [1], "domain": "example.com"}'
```

## Notes

- Use `api-key` header for authentication (NOT Bearer token)
- Expected success status code: `201`
- Handle 502 errors with retry logic for POST/PUT/PATCH operations
