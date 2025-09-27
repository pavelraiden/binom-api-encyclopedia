# POST /public/api/v1/binom/protect/campaign/{campaignId}/settings

## Overview

**Description**: Update Settings for a Campaign  
**Method**: `POST`  
**Path**: `/public/api/v1/binom/protect/campaign/{campaignId}/settings`  
**Authentication**: Required (Bearer Token)  
**Tags**: Protect Protect

## Request

### Headers
```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
Accept: application/json
```

### Parameters

| Parameter | Type | Required | In | Description |
|-----------|------|----------|----|--------------|
| `campaignId` | string | ✅ Yes | path | Campaignid identifier |

### Request Body

**Content-Type**: `application/json`

**Example:**
```json
{
  "name": "Test Campaign",
  "trafficSourceId": 1,
  "cost": 0.1,
  "currency": "USD"
}
```

**Schema:**
```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Campaign name"
    },
    "trafficSourceId": {
      "type": "integer",
      "description": "Traffic source ID"
    },
    "cost": {
      "type": "number",
      "description": "Cost per click"
    },
    "currency": {
      "type": "string",
      "description": "Currency code",
      "default": "USD"
    }
  },
  "required": [
    "name",
    "trafficSourceId"
  ]
}
```

### Example Requests

**cURL:**
```bash
curl -X POST \
  -H "Authorization: Bearer $BINOM_API_KEY" \
  -H "Content-Type: application/json" \
  "https://pierdun.com/public/api/v1/binom/protect/campaign/123/settings"
```

**Python:**
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
    f"{BASE_URL}/public/api/v1/binom/protect/campaign/123/settings",
    headers=headers,
    json={'name': 'Test Campaign', 'trafficSourceId': 1, 'cost': 0.1, 'currency': 'USD'}
)

if response.status_code in [200, 201]:
    data = response.json()
    print(data)
else:
    print(f"Error: {{response.status_code}} - {{response.text}}")
```

## Responses

### 201 - Created successfully

**Example:**
```json
{
  "id": 123,
  "message": "Resource created successfully"
}
```

### 400 - Bad Request - Invalid parameters

**Example:**
```json
{
  "error": "Invalid parameters. Check datePreset and timezone."
}
```

### 401 - Unauthorized - Invalid API key

**Example:**
```json
{
  "error": "Invalid API key"
}
```

### 403 - Forbidden - Access denied

**Example:**
```json
{
  "error": "Access denied"
}
```

## AI Agent Usage

### Common Use Cases
- Data retrieval and analysis
- Automated reporting
- Campaign management
- Performance optimization

### Integration Tips
- Always include required parameters (`datePreset`, `timezone`)
- Implement proper error handling
- Use pagination for large datasets
- Cache frequently accessed data

### Related Endpoints
- Check other endpoints in the same category
- Consider workflow dependencies
- Look for bulk operation alternatives

## Best Practices

1. **Authentication**: Always use Bearer token format
2. **Rate Limiting**: Implement delays between requests
3. **Error Handling**: Check status codes before processing
4. **Data Validation**: Validate input parameters
5. **Pagination**: Use `limit` and `offset` for large datasets

---

*Documentation generated from Binom API specification*
