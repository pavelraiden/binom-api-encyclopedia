# Authentication Guide

The Binom API uses Bearer token authentication for secure access to your data. This guide covers everything you need to know about authenticating with the API.

## Authentication Method

Binom API exclusively uses **Bearer token authentication**. Other authentication methods are not supported.

### Correct Authentication Format

```http
Authorization: Bearer YOUR_API_KEY
```

### ❌ Incorrect Formats (Do Not Use)

```http
X-API-Key: YOUR_API_KEY          # Not supported
api-key: YOUR_API_KEY            # Not supported
?api_key=YOUR_API_KEY            # Not supported in query params
```

## Getting Your API Key

Your API key is available in your Binom dashboard:

1. Log into your Binom account
2. Navigate to **Settings** → **API Keys**
3. Generate a new API key or copy an existing one
4. Store it securely (treat it like a password)

## Implementation Examples

### Python with requests

```python
import requests
import os

# Store your API key securely
API_KEY = os.getenv('BINOM_API_KEY')  # Use environment variables
BASE_URL = "https://pierdun.com/public/api/v1"

# Correct headers configuration
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Test authentication
def test_auth():
    response = requests.get(
        f"{BASE_URL}/info/offer",
        headers=headers,
        params={"datePreset": "today", "timezone": "UTC", "limit": 1}
    )
    
    if response.status_code == 200:
        print("✅ Authentication successful!")
        return True
    elif response.status_code == 401:
        print("❌ Authentication failed: Invalid API key")
        return False
    elif response.status_code == 403:
        print("❌ Authentication failed: Check Bearer token format")
        return False
    else:
        print(f"❌ Unexpected error: {response.status_code}")
        return False

# Usage
if test_auth():
    print("Ready to make API calls!")
```

### JavaScript with axios

```javascript
const axios = require('axios');

const API_KEY = process.env.BINOM_API_KEY; // Use environment variables
const BASE_URL = 'https://pierdun.com/public/api/v1';

// Create axios instance with default headers
const binomAPI = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});

// Test authentication
async function testAuth() {
    try {
        const response = await binomAPI.get('/info/offer', {
            params: {
                datePreset: 'today',
                timezone: 'UTC',
                limit: 1
            }
        });
        
        console.log('✅ Authentication successful!');
        return true;
    } catch (error) {
        if (error.response?.status === 401) {
            console.log('❌ Authentication failed: Invalid API key');
        } else if (error.response?.status === 403) {
            console.log('❌ Authentication failed: Check Bearer token format');
        } else {
            console.log(`❌ Unexpected error: ${error.response?.status}`);
        }
        return false;
    }
}

// Usage
testAuth().then(success => {
    if (success) {
        console.log('Ready to make API calls!');
    }
});
```

### curl

```bash
# Store API key in environment variable for security
export BINOM_API_KEY="your_api_key_here"

# Test authentication
curl -X GET "https://pierdun.com/public/api/v1/info/offer" \
  -H "Authorization: Bearer $BINOM_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -G \
  -d "datePreset=today" \
  -d "timezone=UTC" \
  -d "limit=1"
```

## Security Best Practices

### 1. Environment Variables

Never hardcode API keys in your source code. Use environment variables:

```python
# ✅ Good
API_KEY = os.getenv('BINOM_API_KEY')

# ❌ Bad
API_KEY = "your_actual_api_key_here"
```

### 2. Secure Storage

Store API keys securely:
- Use environment variables in production
- Use secure key management services (AWS Secrets Manager, Azure Key Vault)
- Never commit API keys to version control

### 3. Key Rotation

Regularly rotate your API keys:
- Generate new keys periodically
- Revoke old keys after updating your applications
- Monitor key usage for suspicious activity

### 4. Scope Limitation

Use API keys with minimal required permissions:
- Create separate keys for different applications
- Limit key permissions to necessary operations only
- Monitor and audit key usage

## Common Authentication Errors

### 401 Unauthorized

**Cause**: Invalid or missing API key

**Solutions**:
- Verify your API key is correct
- Check that the key is active in your Binom dashboard
- Ensure you're using the correct Binom instance URL

### 403 Forbidden

**Cause**: Incorrect authentication format

**Solutions**:
- Use `Authorization: Bearer YOUR_API_KEY` format
- Remove any other authentication headers
- Verify the Bearer token format is correct

### Rate Limiting

**Cause**: Too many requests in a short period

**Solutions**:
- Implement exponential backoff
- Respect rate limits (check response headers)
- Cache responses when possible

## Testing Your Authentication

Use this simple test to verify your authentication setup:

```python
import requests

def test_binom_auth(api_key):
    """Test Binom API authentication"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    params = {
        "datePreset": "today",
        "timezone": "UTC",
        "limit": 1
    }
    
    try:
        response = requests.get(
            "https://pierdun.com/public/api/v1/info/offer",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Authentication successful!")
            print(f"Response: {len(response.json())} offers found")
            return True
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False

# Usage
if __name__ == "__main__":
    api_key = input("Enter your API key: ")
    test_binom_auth(api_key)
```

## API Key Management

### Creating New Keys

1. Access your Binom dashboard
2. Go to **Settings** → **API Keys**
3. Click **Generate New Key**
4. Set appropriate permissions
5. Copy and store the key securely

### Revoking Keys

1. Access your Binom dashboard
2. Go to **Settings** → **API Keys**
3. Find the key to revoke
4. Click **Revoke** or **Delete**
5. Update your applications with new keys

## Next Steps

Now that you understand authentication:

1. [Explore basic examples](basic-examples.md) with proper authentication
2. [Learn about core concepts](../core-concepts/api-overview.md)
3. [Understand error handling](../core-concepts/error-handling.md)

---

**Previous**: [← Getting Started](getting-started.md) | **Next**: [Basic Examples →](basic-examples.md)
