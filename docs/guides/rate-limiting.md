# Rate Limiting

## Overview

The Binom API implements rate limiting to ensure fair usage and system stability.

## Limits

- **Default Limit**: 1000 requests per hour per API key
- **Burst Limit**: 100 requests per minute

## Response Headers

The API includes rate limiting information in response headers:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Handling Rate Limits

When you exceed the rate limit, the API returns a `429 Too Many Requests` status code.

### Python Example

```python
import time
import requests

def make_request_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            print(f"Rate limited. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            continue
        
        return response
    
    raise Exception("Max retries exceeded")
```

## Best Practices

1. **Monitor Headers**: Always check rate limit headers in responses
2. **Implement Backoff**: Use exponential backoff for retries
3. **Cache Results**: Cache API responses when possible
4. **Batch Requests**: Use batch endpoints when available
