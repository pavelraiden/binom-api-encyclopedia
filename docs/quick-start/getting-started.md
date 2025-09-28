# Getting Started with Binom API

Welcome to the Binom API! This guide will help you make your first successful API call in just 5 minutes.

## Prerequisites

Before you begin, ensure you have:
- A Binom account with API access
- Your API key (Bearer token)
- A tool to make HTTP requests (curl, Postman, or your preferred programming language)

## Your First API Call

Let's start with a simple request to get your account information:

### Using curl

```bash
curl -X GET "https://pierdun.com/public/api/v1/info/offer" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -G \
  -d "datePreset=today" \
  -d "timezone=UTC" \
  -d "limit=5"
```

### Using Python

```python
import requests
import os

# Configuration
API_KEY = "YOUR_API_KEY"  # Replace with your actual API key
BASE_URL = "https://pierdun.com/public/api/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Required parameters for all requests
params = {
    "datePreset": "today",
    "timezone": "UTC",
    "limit": 5
}

# Make the request
response = requests.get(f"{BASE_URL}/info/offer", headers=headers, params=params)

if response.status_code == 200:
    offers = response.json()
    print(f"✅ Success! Found {len(offers)} offers")
    for offer in offers:
        print(f"- {offer.get('name', 'Unnamed offer')}")
else:
    print(f"❌ Error: {response.status_code} - {response.text}")
```

### Using JavaScript (Node.js)

```javascript
const axios = require('axios');

const API_KEY = 'YOUR_API_KEY'; // Replace with your actual API key
const BASE_URL = 'https://pierdun.com/public/api/v1';

const headers = {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
};

const params = {
    datePreset: 'today',
    timezone: 'UTC',
    limit: 5
};

axios.get(`${BASE_URL}/info/offer`, { headers, params })
    .then(response => {
        console.log(`✅ Success! Found ${response.data.length} offers`);
        response.data.forEach(offer => {
            console.log(`- ${offer.name || 'Unnamed offer'}`);
        });
    })
    .catch(error => {
        console.error(`❌ Error: ${error.response?.status} - ${error.response?.data}`);
    });
```

## Understanding the Response

A successful response will look like this:

```json
[
    {
        "id": 1,
        "name": "Example Offer",
        "status": "active",
        "url": "https://example.com/offer",
        "payout": 10.00,
        "currency": "USD",
        "created_at": "2025-09-28T10:00:00Z"
    }
]
```

## Common Response Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Your request was processed successfully |
| 400 | Bad Request | Check your parameters (datePreset and timezone are required) |
| 401 | Unauthorized | Verify your API key is correct |
| 403 | Forbidden | Check your API key format (should use Bearer token) |
| 429 | Rate Limited | Wait a moment and try again |
| 500 | Server Error | Contact support if this persists |

## Critical Requirements

**⚠️ Important**: Every API request MUST include these parameters:

- `datePreset`: Specifies the time period (e.g., "today", "last_7_days")
- `timezone`: Timezone for date calculations (e.g., "UTC", "America/New_York")

**Authentication**: Use Bearer token format:
```
Authorization: Bearer YOUR_API_KEY
```

## Next Steps

Now that you've made your first successful API call, you can:

1. [Learn about authentication](authentication.md) in detail
2. [Explore basic examples](basic-examples.md) for common use cases
3. [Understand core concepts](../core-concepts/api-overview.md) for deeper integration

## Troubleshooting

### "403 Forbidden" Error
- Ensure you're using `Authorization: Bearer YOUR_API_KEY` (not `X-API-Key`)
- Verify your API key is active and has the necessary permissions

### "400 Bad Request" Error
- Always include `datePreset` and `timezone` parameters
- Check parameter spelling and values

### Empty Response
- Try different `datePreset` values (e.g., "last_7_days" instead of "today")
- Verify you have data for the specified time period

## Support

If you encounter issues:
- Check our [error handling guide](../core-concepts/error-handling.md)
- Review [common issues](../bug_reports/) and solutions
- Contact support with your request details (excluding your API key)

---

**Next**: [Authentication Guide →](authentication.md)
