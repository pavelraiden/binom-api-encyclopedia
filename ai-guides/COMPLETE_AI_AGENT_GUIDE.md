# 🤖 Complete AI Agent Guide for Binom API

## Quick Start for AI Agents

### Authentication
```python
import os
API_KEY = os.getenv('binomPublic')
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
```

### Essential Parameters
**CRITICAL**: Most endpoints require:
- `datePreset`: "last_7_days", "today", "yesterday", etc.
- `timezone`: "UTC" (always use UTC for consistency)

### Complete Endpoint Coverage
This encyclopedia covers **51 endpoints** across **5 categories**:

#### Affiliate Network (10 endpoints)
- `GET /public/api/v1/affiliate_network/{id}/clone`
- `POST /public/api/v1/affiliate_network`
- `GET /public/api/v1/affiliate_network/{id}`
- ... and 7 more

#### Clicks (2 endpoints)
- `PUT /public/api/v1/clicks/campaign/{id}`
- `DELETE /public/api/v1/clicks/campaign/{id}`

#### Campaign (27 endpoints)
- `POST /public/api/v1/campaign`
- `GET /public/api/v1/campaign/{id}`
- `PUT /public/api/v1/campaign/{id}`
- ... and 24 more

#### Stats (6 endpoints)
- `GET /public/api/v1/stats/offer`
- `GET /public/api/v1/stats/traffic_source`
- `GET /public/api/v1/stats/campaign`
- ... and 3 more

#### Info (6 endpoints)
- `GET /public/api/v1/info/offer`
- `GET /public/api/v1/info/traffic_source`
- `GET /public/api/v1/info/campaign`
- ... and 3 more


## Common Workflows

### 1. Campaign Setup Workflow
```python
# 1. Create affiliate network
network = create_affiliate_network(name="My Network", postback_url="...")

# 2. Create campaign
campaign = create_campaign(name="My Campaign", traffic_source_id=1)

# 3. Get campaign stats
stats = get_campaign_stats(campaign_id=campaign['id'], date_preset="last_7_days")
```

### 2. Performance Analysis Workflow
```python
# 1. Get campaign stats with custom metrics
stats = get_campaign_stats(
    date_preset="last_7_days",
    timezone="UTC",
    group_by="landingId"  # For landing page analysis
)

# 2. Analyze performance
for campaign in stats['data']:
    ecpt = campaign['customMetrics']['eCPT']
    trials = campaign['customMetrics']['trials']
    # Optimization logic here
```

## Error Handling Patterns

### Standard Error Handler
```python
def handle_binom_response(response):
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        error_data = response.json()
        raise ValueError(f"Validation error: {{error_data.get('message', 'Unknown error')}}")
    elif response.status_code == 401:
        raise PermissionError("Invalid API key")
    elif response.status_code == 403:
        raise PermissionError("Access denied")
    elif response.status_code == 404:
        raise NotFoundError("Resource not found")
    elif response.status_code == 429:
        raise RateLimitError("Rate limit exceeded")
    else:
        raise Exception(f"API error {{response.status_code}}: {{response.text}}")
```

## Best Practices for AI Agents

1. **Always validate input data** before sending requests
2. **Implement retry logic** with exponential backoff for 429 errors
3. **Cache frequently accessed data** to reduce API calls
4. **Use batch operations** when available
5. **Monitor rate limits** and implement delays
6. **Log all requests and responses** for debugging
7. **Handle all error codes** appropriately
8. **Use structured error handling** for better user feedback

## Rate Limiting Strategy

```python
import time
from functools import wraps

def rate_limited(max_per_minute=100):
    min_interval = 60.0 / max_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

@rate_limited(max_per_minute=90)  # Stay under 100/min limit
def make_api_request(endpoint, data=None):
    # Your API request logic here
    pass
```

---

*🎯 This guide covers all {len(data)} Binom API endpoints*  
*📊 Generated from comprehensive API analysis*  
*🤖 Optimized specifically for AI agent integration*
