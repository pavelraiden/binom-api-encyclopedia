# GET /public/api/v1/stats/offer

## 🎯 Overview

**Summary**: Get Offer Stats  
**Method**: `GET`  
**Path**: `/public/api/v1/stats/offer`  
**Category**: Stats  
**Authentication**: ✅ Required (Bearer Token)

## 📋 Description

Get Offer Stats. Retrieves information from the stats resource with optional filtering and pagination.

## 🔧 Parameters

| Parameter | Type | In | Required | Description | Example |
|-----------|------|----|-----------|--------------|---------|
| `datePreset` | string | query | ✅ Yes | Date range preset for filtering data | `last_7_days` |
| `timezone` | string | query | ✅ Yes | Timezone for date calculations (always use UTC for consistency) | `UTC` |
| `limit` | integer | query | ❌ No | Maximum number of records to return | `100` |
| `offset` | integer | query | ❌ No | Number of records to skip for pagination | `0` |
| `dateFrom` | string | query | ❌ No | Start date for custom time range (required when datePreset=custom_time) | `2023-01-01 00:00:00` |
| `dateTo` | string | query | ❌ No | End date for custom time range (required when datePreset=custom_time) | `2023-01-31 23:59:59` |

## 📥 Responses

### ✅ 200 - Success - Statistics data returned

**Example:**
```json
{
  "data": [
    {
      "id": 51,
      "name": "Campaign Name",
      "clicks": 1000,
      "conversions": 50,
      "cost": 500.0,
      "revenue": 750.0,
      "profit": 250.0,
      "roi": 50.0,
      "ctr": 5.0,
      "cr": 5.0,
      "ecpm": 25.0,
      "customMetrics": {
        "eCPT": 30.35,
        "eCPB": 108.39,
        "trials": 50,
        "buyouts": 14
      }
    }
  ],
  "totals": {
    "clicks": 1000,
    "conversions": 50,
    "cost": 500.0,
    "revenue": 750.0
  }
}
```

### ❌ 400 - Bad Request - Invalid input data or missing required fields

**Example:**
```json
{
  "error": "Validation failed",
  "message": "Field 'name' is required",
  "details": {
    "field": "name",
    "code": "required",
    "value": null
  }
}
```

### ❌ 401 - Unauthorized - Invalid or missing API key

**Example:**
```json
{
  "error": "Unauthorized",
  "message": "Invalid API key or token expired"
}
```

### ❌ 403 - Forbidden - Access denied or insufficient permissions

**Example:**
```json
{
  "error": "Access denied",
  "message": "Insufficient permissions to access this resource"
}
```

### ❌ 404 - Not Found - Resource not found

**Example:**
```json
{
  "error": "Not found",
  "message": "Resource with ID 123 not found"
}
```

### ❌ 429 - Too Many Requests - Rate limit exceeded

**Example:**
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests, please try again later",
  "retryAfter": 60
}
```

### ❌ 500 - Internal Server Error - Server-side error

**Example:**
```json
{
  "error": "Internal server error",
  "message": "Something went wrong on our end"
}
```

## 💻 Code Examples

### Python
```python
import requests
import os
import time
from typing import Optional, Dict, Any

class BinomAPIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://pierdun.com/public/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[Any, Any]:
        """Make API request with error handling and retries"""
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(3):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    json=data,
                    params=params,
                    timeout=30
                )
                
                if response.status_code == 429:
                    # Rate limit - wait and retry
                    time.sleep(2 ** attempt)
                    continue
                
                if response.status_code in [200, 201]:
                    return response.json()
                else:
                    raise Exception(f"API Error {response.status_code}: {response.text}")
                    
            except requests.exceptions.RequestException as e:
                if attempt == 2:  # Last attempt
                    raise Exception(f"Request failed: {str(e)}")
                time.sleep(1)
        
        raise Exception("Max retries exceeded")

# Usage example
client = BinomAPIClient(os.getenv('binomPublic'))

try:
    result = client.make_request(
        method="GET",
        endpoint="/public/api/v1/stats/offer",
        params={
            "datePreset": "last_7_days",
            "timezone": "UTC",
            "limit": 100,
            "offset": 0
        }
    )
    
    print("✅ Success:", result)
    
except Exception as e:
    print(f"❌ Error: {e}")
```

### cURL
```bash
# Basic request
curl -X GET \
  -H "Authorization: Bearer $BINOM_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  "https://pierdun.com/public/api/v1/stats/offer"

# With query parameters
curl -X GET \
  -H "Authorization: Bearer $BINOM_API_KEY" \
  -H "Accept: application/json" \
  "https://pierdun.com/public/api/v1/stats/offer?datePreset=last_7_days&timezone=UTC&limit=100&offset=0"
```

### JavaScript
```javascript
class BinomAPI {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseURL = 'https://pierdun.com/public/api/v1';
    this.headers = {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };
  }

  async makeRequest(method, endpoint, data = null, params = null) {
    const url = new URL(`${this.baseURL}${endpoint}`);
    
    if (params) {
      Object.keys(params).forEach(key => 
        url.searchParams.append(key, params[key])
      );
    }

    const config = {
      method: method,
      headers: this.headers
    };

    if (data) {
      config.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(url.toString(), config);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${await response.text()}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }
}

// Usage
const api = new BinomAPI(process.env.BINOM_API_KEY);

try {
  const result = await api.makeRequest(
    'GET',
    '/public/api/v1/stats/offer',
    null,
    {
      datePreset: 'last_7_days',
      timezone: 'UTC',
      limit: 100,
      offset: 0
    }
  );
  
  console.log('✅ Success:', result);
} catch (error) {
  console.error('❌ Error:', error.message);
}
```

## ⚠️ Error Handling

### Common Errors

**400**: Invalid input data, missing required fields, or malformed JSON
- *Solution*: Validate all input data before sending. Check required fields and data types.
- *Example*: Missing 'name' field in request body

**401**: Invalid, expired, or missing API key
- *Solution*: Verify API key is correct and has not expired. Check Authorization header format.
- *Example*: Authorization header: 'Bearer YOUR_API_KEY'

**403**: Insufficient permissions or access denied
- *Solution*: Ensure API key has required permissions for this operation.
- *Example*: User lacks permission to modify campaigns

**404**: Resource not found or invalid ID
- *Solution*: Verify resource ID exists and is accessible to your account.
- *Example*: Campaign with ID 123 does not exist

**429**: Rate limit exceeded
- *Solution*: Implement exponential backoff and retry logic. Reduce request frequency.
- *Example*: Wait 60 seconds before retrying

**500**: Internal server error
- *Solution*: Retry request after a delay. Contact support if error persists.
- *Example*: Temporary server issue

## 🤖 AI Integration Notes

### Key Points
- This is a GET endpoint for v1 operations
- Requires Bearer token authentication in Authorization header
- Returns JSON responses with consistent error format
- Supports standard HTTP status codes for success/error indication
- Rate limited to 100 requests per minute

### Integration Tips
- Always validate input data before making requests
- Implement proper error handling for all status codes
- Use exponential backoff for rate limiting (429 errors)
- Cache responses when appropriate to reduce API calls
- Set reasonable timeouts (30 seconds recommended)
- Log requests and responses for debugging

### Workflow Context
Analysis step: Retrieve performance data for optimization decisions

### Real-World Usage
- Managing stats resources in affiliate marketing workflows
- Automating stats operations for campaign optimization
- Integrating stats data with external reporting systems

---

*📊 Documentation generated from comprehensive Binom API analysis*  
*🤖 Optimized for AI agents and automated workflows*  
*📅 Generated: 2025-09-26 21:02:47*