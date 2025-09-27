# POST /landing/import

## Import not integrated landings

**Method:** `POST`  
**Endpoint:** `/public/api/v1/landing/import`

## Description

Format: Name;Url;LanguageCode;[GroupName]

## Request Body

**Content-Type:** `application/json`

```json
{
  "landings": "Test Name;google.com;UK;MyGroup"
}
```

## Response

### 201

Success

### 202

```json
{
  "errors": {
    "1": [
      "Url: Value is too short"
    ],
    "3": [
      "Name: Value is too short"
    ]
  }
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
    "landings": "Test Name;google.com;UK;MyGroup"
}

response = requests.post(
    "https://pierdun.com/public/api/v1/landing/import",
    headers=headers,
    json=data
)

print(response.status_code)
print(response.json())
```

### cURL

```bash
curl -X POST \
  "https://pierdun.com/public/api/v1/landing/import" \
  -H "api-key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"landings": "Test Name;google.com;UK;MyGroup"}'
```

## Notes

- Use `api-key` header for authentication (NOT Bearer token)
- Expected success status code: `201`
- Handle 502 errors with retry logic for POST/PUT/PATCH operations
