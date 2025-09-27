# POST /public/api/v1/affiliate_network

## 🎯 Overview

**Description**: Create Affiliate Network.  
**Method**: `POST`  
**Path**: `/public/api/v1/affiliate_network`  
**Authentication**: ✅ Required (Bearer Token)  
**Category**: Affiliate Network  
**Data Source**: ✅ Real Swagger UI Examples

## 📋 Request Details

### Headers
```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
Accept: application/json
```

### Parameters

❌ No parameters required

### Request Body

**Content-Type**: `application/json`

**🔥 REAL EXAMPLE FROM SWAGGER UI:**
```json
{
  "name": "My network",
  "offerUrlTemplate": "string",
  "postbackUrl": "string",
  "postbackIpWhitelist": [
    "1.2.3.4",
    "2001:0db8:0000:0000:0000:ff00:0042:8329"
  ],
  "statusPayoutRelations": [
    {
      "conversionStatus": "Status",
      "payout": "{payout}"
    }
  ],
  "isPayoutRelationsActive": true
}
```

**Field Analysis:**
- `name`: str - Human-readable name for the resource
- `offerUrlTemplate`: str - Template URL for offers with placeholders
- `postbackUrl`: str - URL for receiving conversion notifications
- `postbackIpWhitelist`: array of str - List of allowed IP addresses for postbacks
- `statusPayoutRelations`: array of dict - Mapping between conversion statuses and payouts
- `isPayoutRelationsActive`: bool - Whether payout relations are enabled

## 📤 Responses

### ✅ 201 - Affiliate Network created successfully

**Real Response Example:**
```json
{
  "id": 1
}
```

### ❌ 400 - Bad request

*No example available*

### ❌ 403 - Access Denied

*No example available*

## 💻 Code Examples

### Python (with real data)
```python
import requests
import os

# Configuration
API_KEY = os.getenv('binomPublic')
BASE_URL = "https://pierdun.com/public/api/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Real request example
response = requests.post(
    f"{BASE_URL}/public/api/v1/affiliate_network",
    headers=headers,
    json={
    "name": "My network",
    "offerUrlTemplate": "string",
    "postbackUrl": "string",
    "postbackIpWhitelist": [
        "1.2.3.4",
        "2001:0db8:0000:0000:0000:ff00:0042:8329"
    ],
    "statusPayoutRelations": [
        {
            "conversionStatus": "Status",
            "payout": "{payout}"
        }
    ],
    "isPayoutRelationsActive": true
}
)

# Handle response
if response.status_code == 201:
    result = response.json()
    print("✅ Success:", result)
elif response.status_code == 400:
    print("❌ Bad Request:", response.text)
elif response.status_code == 403:
    print("❌ Access Denied - Check your API key")
else:
    print(f"❌ Error {response.status_code}: {response.text}")
```

### cURL (with real data)
```bash
curl -X POST \
  -H "Authorization: Bearer $BINOM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"My network","offerUrlTemplate":"string","postbackUrl":"string","postbackIpWhitelist":["1.2.3.4","2001:0db8:0000:0000:0000:ff00:0042:8329"],"statusPayoutRelations":[{"conversionStatus":"Status","payout":"{payout}"}],"isPayoutRelationsActive":true}' \
  "https://pierdun.com/public/api/v1/affiliate_network"
```

## 🤖 AI Agent Integration

### Key Points for AI Agents
- ✅ **Real data validated**: All examples are from live Swagger UI
- ✅ **Error handling**: Implement proper status code checking
- ✅ **Authentication**: Always use Bearer token format
- ✅ **Rate limiting**: Add delays between requests

### Common Integration Patterns
```python
def create_affiliate_network(name, postback_url, offer_template):
    """AI-friendly wrapper function"""
    payload = {
        "name": name,
        "offerUrlTemplate": offer_template,
        "postbackUrl": postback_url,
        "postbackIpWhitelist": [],
        "statusPayoutRelations": [],
        "isPayoutRelationsActive": True
    }
    
    response = make_binom_request("POST", "/affiliate_network", payload)
    return response
```

### Error Handling Best Practices
- **400 Bad Request**: Validate input data format
- **403 Access Denied**: Check API key and permissions  
- **Rate Limiting**: Implement exponential backoff
- **Network Errors**: Add retry logic with delays

---

*📊 Documentation generated from real Binom API v2 Swagger specification*  
*🤖 Optimized for AI agents and automated workflows*
