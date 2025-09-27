# 🤖 AI Agent Guide for Binom API

## Quick Start for AI Agents

### Authentication Setup
```python
import os
API_KEY = os.getenv('binomPublic')
BASE_URL = "https://pierdun.com/public/api/v1"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}
```

### Essential Parameters
Most endpoints require:
- `datePreset`: "last_7_days", "today", "yesterday", etc.
- `timezone`: "UTC" (always use UTC for consistency)

### Real Data Examples
All examples in this documentation are extracted from live Swagger UI and tested.

## Common Workflows

### 1. Campaign Management
```python
# Create campaign -> Add landings -> Add offers -> Start traffic
```

### 2. Performance Analysis  
```python
# Get stats -> Analyze metrics -> Optimize weights
```

### 3. Automated Reporting
```python
# Collect data -> Generate reports -> Send notifications
```

## Error Handling Patterns

### Standard Error Response
```python
def handle_binom_response(response):
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        raise ValueError(f"Bad request: {response.text}")
    elif response.status_code == 403:
        raise PermissionError("Access denied - check API key")
    elif response.status_code == 404:
        raise NotFoundError("Resource not found")
    else:
        raise Exception(f"API error {response.status_code}: {response.text}")
```

## Best Practices for AI Agents

1. **Always validate input data** before sending requests
2. **Implement retry logic** with exponential backoff
3. **Cache frequently accessed data** to reduce API calls
4. **Use batch operations** when available
5. **Monitor rate limits** and implement delays

---

*Generated from real Binom API v2 data*
