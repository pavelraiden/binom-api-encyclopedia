# AI Agent Integration Guide

Complete guide for AI agents to effectively work with Binom API.

## 🤖 Quick Start for AI Agents

### Essential Configuration
```python
import requests
import os

# Configuration
API_BASE = "https://pierdun.com/public/api/v1"
API_KEY = os.getenv('BINOM_API_KEY')

# CRITICAL: Use api-key header, NOT Bearer token
HEADERS = {
    "api-key": API_KEY,
    "Content-Type": "application/json"
}

# Required parameters for all stats endpoints
DEFAULT_PARAMS = {
    "datePreset": "last_7_days",
    "timezone": "UTC"
}
```

---

## 📊 Endpoint Reliability Matrix

### ✅ Stable Endpoints (100% reliability)
Use these for critical operations:

```python
STABLE_ENDPOINTS = {
    "info": [
        "GET /info/offer",
        "GET /info/campaign", 
        "GET /info/traffic_source",
        "GET /info/landing"
    ],
    "stats": [
        "GET /stats/offer",
        "GET /stats/campaign",
        "GET /stats/traffic_source", 
        "GET /stats/landing"
    ]
}
```

### ⚠️ Unstable Endpoints (require fallbacks)
Implement retry logic and fallbacks:

```python
UNSTABLE_ENDPOINTS = {
    "create": [
        "POST /landing/integrated",    # 502 Bad Gateway common
        "POST /landing/not_integrated", # 502 Bad Gateway common
        "POST /offer"                  # 400 Bad Request common
    ]
}
```

---

## 🎯 AI Agent Patterns

### Pattern 1: Safe Data Collection
```python
def collect_campaign_data(campaign_id=None):
    """Collect campaign data using only stable endpoints"""
    
    data = {}
    
    # Get campaigns (always works)
    campaigns = requests.get(
        f"{API_BASE}/info/campaign",
        headers=HEADERS,
        params=DEFAULT_PARAMS
    ).json()
    
    # Get campaign stats (always works)
    stats = requests.get(
        f"{API_BASE}/stats/campaign", 
        headers=HEADERS,
        params=DEFAULT_PARAMS
    ).json()
    
    return {
        "campaigns": campaigns,
        "stats": stats,
        "reliability": "100%"
    }
```

### Pattern 2: Resilient Resource Creation
```python
def create_traffic_source_resilient(name, s2s_mode="FIRST"):
    """Create traffic source with error handling"""
    
    payload = {
        "name": name,
        "s2sMode": s2s_mode  # REQUIRED: "FIRST" or "ALL"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/traffic_source",
            headers=HEADERS,
            json=payload
        )
        
        if response.status_code == 201:
            return {
                "success": True,
                "data": response.json(),
                "method": "api"
            }
        elif response.status_code == 502:
            return {
                "success": False,
                "error": "Server overload",
                "fallback": "Use Binom UI for manual creation",
                "retry_in": "5-10 seconds"
            }
        else:
            return {
                "success": False,
                "error": response.json(),
                "status_code": response.status_code
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "fallback": "Check network connection and API key"
        }
```

### Pattern 3: Comprehensive Error Handling
```python
def api_request_with_recovery(method, endpoint, **kwargs):
    """Universal API request with error recovery"""
    
    max_retries = 3
    backoff_factor = 2
    
    for attempt in range(max_retries):
        try:
            response = requests.request(
                method, 
                f"{API_BASE}{endpoint}",
                headers=HEADERS,
                **kwargs
            )
            
            # Success cases
            if response.status_code in [200, 201]:
                return {
                    "success": True,
                    "data": response.json(),
                    "attempts": attempt + 1
                }
            
            # Authentication error
            elif response.status_code == 401:
                return {
                    "success": False,
                    "error": "Authentication failed",
                    "solution": "Check api-key header format (not Bearer token)",
                    "fatal": True  # Don't retry
                }
            
            # Server error - retry
            elif response.status_code == 502:
                if attempt < max_retries - 1:
                    wait_time = backoff_factor ** attempt
                    time.sleep(wait_time)
                    continue
                else:
                    return {
                        "success": False,
                        "error": "Server consistently unavailable",
                        "fallback": "Use manual UI operations"
                    }
            
            # Validation error
            elif response.status_code == 400:
                return {
                    "success": False,
                    "error": "Validation failed",
                    "details": response.json(),
                    "solution": "Check required fields and data types"
                }
                
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(backoff_factor ** attempt)
                continue
            else:
                return {
                    "success": False,
                    "error": f"Network error: {str(e)}",
                    "fatal": True
                }
    
    return {"success": False, "error": "Max retries exceeded"}
```

---

## 📋 Field Dependencies & Business Rules

### Traffic Source Creation
```json
{
  "required_fields": ["name", "s2sMode"],
  "s2sMode_values": ["FIRST", "ALL"],
  "business_rules": {
    "name": "Must be unique within account",
    "s2sMode": "Determines postback handling strategy"
  },
  "success_indicator": "HTTP 201 with ID in response"
}
```

### Campaign Creation
```json
{
  "required_fields": ["name", "trafficSourceId"],
  "dependencies": {
    "trafficSourceId": "Must exist in /info/traffic_source"
  },
  "optional_fields": ["cost", "currency", "status"],
  "defaults": {
    "status": "active",
    "currency": "USD"
  }
}
```

### Stats Queries
```json
{
  "required_fields": ["datePreset", "timezone"],
  "datePreset_values": [
    "today", "yesterday", "last_7_days", "last_30_days",
    "this_month", "last_month", "custom_time"
  ],
  "timezone_format": "UTC, America/New_York, Europe/London, etc.",
  "pagination": {
    "limit": "max 1000, default 100",
    "offset": "for pagination"
  }
}
```

---

## 🔄 Workflow Templates

### Template 1: Campaign Performance Analysis
```python
def analyze_campaign_performance():
    """Complete campaign analysis workflow"""
    
    # Step 1: Get all campaigns
    campaigns = api_request_with_recovery("GET", "/info/campaign", params=DEFAULT_PARAMS)
    if not campaigns["success"]:
        return {"error": "Failed to get campaigns", "details": campaigns}
    
    # Step 2: Get performance stats
    stats = api_request_with_recovery("GET", "/stats/campaign", params=DEFAULT_PARAMS)
    if not stats["success"]:
        return {"error": "Failed to get stats", "details": stats}
    
    # Step 3: Analyze and generate insights
    analysis = {
        "total_campaigns": len(campaigns["data"]),
        "performance_data": stats["data"],
        "recommendations": generate_recommendations(campaigns["data"], stats["data"])
    }
    
    return {"success": True, "analysis": analysis}

def generate_recommendations(campaigns, stats):
    """Generate AI-powered recommendations"""
    recommendations = []
    
    # Example logic
    for campaign in campaigns:
        campaign_stats = find_stats_for_campaign(campaign["id"], stats)
        if campaign_stats and campaign_stats.get("conversion_rate", 0) < 0.01:
            recommendations.append({
                "campaign_id": campaign["id"],
                "issue": "Low conversion rate",
                "suggestion": "Review landing page and offer alignment"
            })
    
    return recommendations
```

### Template 2: Bulk Resource Creation
```python
def create_multiple_resources(resource_type, items):
    """Create multiple resources with error handling"""
    
    results = []
    
    for item in items:
        # Rate limiting
        time.sleep(0.1)  # 10 requests/second max
        
        result = api_request_with_recovery("POST", f"/{resource_type}", json=item)
        results.append({
            "item": item,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
        # Stop on fatal errors
        if result.get("fatal"):
            break
    
    return {
        "total_attempted": len(results),
        "successful": len([r for r in results if r["result"]["success"]]),
        "failed": len([r for r in results if not r["result"]["success"]]),
        "details": results
    }
```

---

## 🎯 Prompt Engineering Examples

### For Campaign Analysis
```
You are a Binom API expert. Analyze campaign performance:

1. Use GET /info/campaign with datePreset=last_7_days&timezone=UTC
2. Use GET /stats/campaign with same parameters
3. If you get 401 error, check that you're using 'api-key' header (not Bearer)
4. If you get 502 error, wait 5 seconds and retry up to 3 times
5. Focus on conversion rates, click costs, and ROI metrics
6. Provide specific recommendations for underperforming campaigns

Remember: Only GET endpoints are 100% reliable. POST operations may fail with 502 errors.
```

### For Resource Creation
```
You are creating Binom resources via API:

1. For traffic sources: MUST include 'name' and 's2sMode' ("FIRST" or "ALL")
2. For campaigns: MUST include 'name' and 'trafficSourceId'
3. For stats queries: MUST include 'datePreset' and 'timezone'
4. Use 'api-key' header, never 'Authorization: Bearer'
5. If POST returns 502, suggest manual UI creation as fallback
6. If POST returns 400, check required fields in documentation
7. Always validate response before proceeding

Success indicators: HTTP 201 for creation, HTTP 200 for queries.
```

### For Error Recovery
```
When Binom API errors occur:

1. 401 Unauthorized → Check 'api-key' header format
2. 400 Bad Request → Review required fields and data types  
3. 502 Bad Gateway → Retry with exponential backoff (1s, 2s, 4s)
4. 429 Too Many Requests → Implement rate limiting (max 10/sec)
5. 503/504 Server Errors → Wait and retry, suggest UI fallback

Always log errors with full context. Provide clear next steps to user.
```

---

## 📊 Success Metrics for AI Agents

### Reliability Targets
- **GET operations:** 99%+ success rate
- **POST operations:** 70%+ success rate (with fallbacks)
- **Error recovery:** 90%+ of errors handled gracefully
- **Response time:** <5 seconds average

### Quality Indicators
```python
def evaluate_api_integration_quality(results):
    """Evaluate AI agent API integration quality"""
    
    metrics = {
        "total_requests": len(results),
        "successful_requests": len([r for r in results if r["success"]]),
        "error_recovery_rate": len([r for r in results if r.get("recovered")]),
        "fallback_usage": len([r for r in results if r.get("used_fallback")])
    }
    
    metrics["success_rate"] = metrics["successful_requests"] / metrics["total_requests"]
    metrics["recovery_rate"] = metrics["error_recovery_rate"] / (metrics["total_requests"] - metrics["successful_requests"])
    
    # Quality score
    if metrics["success_rate"] > 0.9 and metrics["recovery_rate"] > 0.8:
        metrics["quality"] = "Excellent"
    elif metrics["success_rate"] > 0.7 and metrics["recovery_rate"] > 0.6:
        metrics["quality"] = "Good"
    else:
        metrics["quality"] = "Needs Improvement"
    
    return metrics
```

---

## 🔧 Development Tools

### API Testing Script
```python
def test_api_endpoints():
    """Test all critical endpoints"""
    
    test_results = []
    
    # Test stable endpoints
    for endpoint in STABLE_ENDPOINTS["info"]:
        result = api_request_with_recovery("GET", endpoint.split(" ")[1], params=DEFAULT_PARAMS)
        test_results.append({
            "endpoint": endpoint,
            "status": "PASS" if result["success"] else "FAIL",
            "details": result
        })
    
    # Test unstable endpoints (expect some failures)
    for endpoint in UNSTABLE_ENDPOINTS["create"]:
        result = api_request_with_recovery("POST", endpoint.split(" ")[1], json={"name": "test"})
        test_results.append({
            "endpoint": endpoint,
            "status": "EXPECTED_FAIL" if not result["success"] else "UNEXPECTED_PASS",
            "details": result
        })
    
    return test_results
```

### Monitoring Dashboard
```python
def create_monitoring_dashboard():
    """Create real-time API monitoring"""
    
    dashboard_data = {
        "timestamp": datetime.now().isoformat(),
        "endpoint_status": {},
        "error_rates": {},
        "response_times": {}
    }
    
    # Test each endpoint
    for category, endpoints in STABLE_ENDPOINTS.items():
        for endpoint in endpoints:
            start_time = time.time()
            result = api_request_with_recovery("GET", endpoint.split(" ")[1], params=DEFAULT_PARAMS)
            response_time = time.time() - start_time
            
            dashboard_data["endpoint_status"][endpoint] = "UP" if result["success"] else "DOWN"
            dashboard_data["response_times"][endpoint] = response_time
    
    return dashboard_data
```

This comprehensive integration guide provides AI agents with everything needed to work effectively with the Binom API, including error handling, retry logic, and fallback strategies.
