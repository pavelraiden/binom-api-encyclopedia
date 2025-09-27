# POST /public/api/v1/traffic_source

## Overview

**Description**: Create Traffic Source.  
**Method**: POST  
**Path**: `/public/api/v1/traffic_source`  
**Authentication**: Required  

## Request

### Headers
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
Accept: application/json
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| datePreset | string | Yes | Time period filter |
| timezone | string | Yes | Timezone (e.g., "UTC") |

### Example Request

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  "https://pierdun.com/public/api/v1/traffic_source?datePreset=last_7_days&timezone=UTC"
```

```python
import requests
import os

API_KEY = os.getenv('binomPublic')
BASE_URL = "https://pierdun.com/public/api/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(
    f"{BASE_URL}/public/api/v1/traffic_source",
    headers=headers,
    params={
        "datePreset": "last_7_days",
        "timezone": "UTC"
    }
)

data = response.json()
print(data)
```

## Response

### Success Response (200)

```json
{
  "status": "success",
  "data": []
}
```

### Error Responses

#### 400 Bad Request
```json
{
  "error": "Invalid parameters"
}
```

#### 401 Unauthorized
```json
{
  "error": "Invalid API key"
}
```

#### 403 Forbidden
```json
{
  "error": "Access denied"
}
```

## AI Usage Notes

- This endpoint is commonly used for: [TO BE FILLED]
- Related endpoints: [TO BE FILLED]
- Common use cases: [TO BE FILLED]

## Related Endpoints

- [TO BE FILLED]

## Examples

### Basic Usage
[TO BE FILLED]

### Advanced Usage
[TO BE FILLED]

## Common Issues

- **Issue**: [TO BE FILLED]
  **Solution**: [TO BE FILLED]

---

*This documentation is auto-generated and needs manual enrichment*
