# GET /landing/list/filtered

## Get Landing list filtered

**Method:** `GET`  
**Endpoint:** `/public/api/v1/landing/list/filtered`

## Description

Get Landing list filtered

## Parameters

- **name**: `string`
- **groupUuid**: `string`
- **language**: `string`
- **limit**: `integer`
- **offset**: `integer`
- **sortColumn**: `id|name|groupUuid|languageCode`
- **sortType**: `asc|desc`

## Response

### 200

```json
[
  {
    "id": 42,
    "name": "Landing name",
    "groupUuid": "66067d5f-e6ea-4652-8cb6-83976342d383",
    "languageCode": "RU",
    "location": "https://example.com",
    "isDomainBanned": false
  }
]
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
    "https://pierdun.com/public/api/v1/landing/list/filtered",
    headers=headers
)

print(response.status_code)
print(response.json())
```

### cURL

```bash
curl -X GET \
  "https://pierdun.com/public/api/v1/landing/list/filtered" \
  -H "api-key: your_api_key_here"
```

## Notes

- Use `api-key` header for authentication (NOT Bearer token)
- Expected success status code: `200`
- Handle 502 errors with retry logic for POST/PUT/PATCH operations
