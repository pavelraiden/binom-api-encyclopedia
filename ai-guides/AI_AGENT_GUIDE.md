# AI Agent Guide for Binom API

This guide is specifically designed for AI agents working with the Binom API Encyclopedia.

## 🤖 Quick Navigation for AI Agents

### Most Common Endpoints by Use Case

#### Campaign Management
- `GET /public/api/v1/campaign/{id}` - Get campaign details
- `PUT /public/api/v1/campaign/{id}` - Update campaign
- `GET /public/api/v1/campaign/list/filtered` - List campaigns with filters
- `POST /public/api/v1/campaign` - Create new campaign

#### Statistics & Analytics
- `GET /public/api/v1/stats/campaign` - Campaign statistics
- `GET /public/api/v1/stats/landing` - Landing page statistics  
- `GET /public/api/v1/stats/offer` - Offer statistics
- `GET /public/api/v1/stats/traffic_source` - Traffic source statistics

#### Information Retrieval
- `GET /public/api/v1/info/campaign` - Campaign info
- `GET /public/api/v1/info/landing` - Landing page info
- `GET /public/api/v1/info/offer` - Offer info
- `GET /public/api/v1/info/traffic_source` - Traffic source info

#### Reporting
- `GET /public/api/v1/report/{page}` - Main reports
- `GET /public/api/v1/report/campaign/groupings` - Campaign groupings
- `GET /public/api/v1/report/landing/groupings` - Landing groupings

## 🔧 Essential Parameters for AI Agents

### Always Required
```python
REQUIRED_PARAMS = {
    "datePreset": "last_7_days",  # or "today", "yesterday", "last_30_days"
    "timezone": "UTC"             # Always use UTC for consistency
}
```

### Common Optional Parameters
```python
OPTIONAL_PARAMS = {
    "limit": 100,                 # Max 1000
    "offset": 0,                  # For pagination
    "sortColumn": "clicks",       # Sort by specific metric
    "sortType": "desc"            # "asc" or "desc"
}
```

## 🚀 AI Agent Code Templates

### Basic Request Template
```python
import requests
import os

def make_binom_request(endpoint, params=None, method='GET', data=None):
    """Standard Binom API request for AI agents"""
    
    API_KEY = os.getenv('binomPublic')
    BASE_URL = "https://pierdun.com/public/api/v1"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Always include required parameters
    default_params = {
        "datePreset": "last_7_days",
        "timezone": "UTC"
    }
    
    if params:
        default_params.update(params)
    
    url = f"{BASE_URL}{endpoint}"
    
    if method.upper() == 'GET':
        response = requests.get(url, headers=headers, params=default_params)
    elif method.upper() == 'POST':
        response = requests.post(url, headers=headers, json=data, params=default_params)
    elif method.upper() == 'PUT':
        response = requests.put(url, headers=headers, json=data, params=default_params)
    elif method.upper() == 'DELETE':
        response = requests.delete(url, headers=headers, params=default_params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")
```

### Campaign Analysis Template
```python
def analyze_campaign_performance(campaign_id, date_preset="last_7_days"):
    """Comprehensive campaign analysis for AI agents"""
    
    # Get campaign details
    campaign = make_binom_request(f"/campaign/{campaign_id}")
    
    # Get campaign statistics
    stats = make_binom_request("/stats/campaign", {
        "campaignIds[]": [campaign_id],
        "datePreset": date_preset
    })
    
    # Get landing page stats
    landing_stats = make_binom_request("/stats/landing", {
        "campaignIds[]": [campaign_id],
        "datePreset": date_preset
    })
    
    # Get offer stats
    offer_stats = make_binom_request("/stats/offer", {
        "campaignIds[]": [campaign_id],
        "datePreset": date_preset
    })
    
    return {
        "campaign": campaign,
        "stats": stats,
        "landing_stats": landing_stats,
        "offer_stats": offer_stats
    }
```

### Bulk Operations Template
```python
def get_all_campaigns_with_stats(date_preset="last_7_days"):
    """Get all campaigns with their statistics"""
    
    # Get campaign list
    campaigns = make_binom_request("/info/campaign", {
        "datePreset": date_preset,
        "limit": 1000
    })
    
    # Get bulk statistics
    campaign_ids = [c['id'] for c in campaigns]
    
    stats = make_binom_request("/stats/campaign", {
        "campaignIds[]": campaign_ids,
        "datePreset": date_preset,
        "limit": 1000
    })
    
    # Merge data
    stats_by_id = {s['campaignId']: s for s in stats}
    
    for campaign in campaigns:
        campaign['stats'] = stats_by_id.get(campaign['id'], {})
    
    return campaigns
```

## 🎯 AI Agent Best Practices

### 1. Error Handling
```python
def safe_binom_request(endpoint, params=None):
    """Error-safe request wrapper for AI agents"""
    try:
        return make_binom_request(endpoint, params)
    except Exception as e:
        if "400" in str(e):
            print("❌ Bad Request - Check required parameters (datePreset, timezone)")
        elif "401" in str(e):
            print("❌ Unauthorized - Check API key")
        elif "403" in str(e):
            print("❌ Forbidden - Check permissions")
        elif "429" in str(e):
            print("❌ Rate Limited - Wait and retry")
        else:
            print(f"❌ Unknown Error: {e}")
        return None
```

### 2. Pagination Handling
```python
def get_all_paginated_data(endpoint, params=None):
    """Get all data with automatic pagination"""
    all_data = []
    offset = 0
    limit = 100
    
    while True:
        current_params = {"limit": limit, "offset": offset}
        if params:
            current_params.update(params)
        
        data = safe_binom_request(endpoint, current_params)
        
        if not data or len(data) == 0:
            break
        
        all_data.extend(data)
        
        if len(data) < limit:
            break
        
        offset += limit
    
    return all_data
```

### 3. Data Validation
```python
def validate_campaign_data(campaign_data):
    """Validate campaign data for AI processing"""
    required_fields = ['id', 'name', 'trafficSourceId']
    
    for field in required_fields:
        if field not in campaign_data:
            return False, f"Missing required field: {field}"
    
    return True, "Valid"
```

## 📊 Common AI Use Cases

### 1. Campaign Optimization
```python
def find_best_performing_campaigns(min_clicks=1000, date_preset="last_30_days"):
    """Find campaigns with best ROI for optimization"""
    
    campaigns = get_all_campaigns_with_stats(date_preset)
    
    # Filter by minimum clicks
    filtered = [c for c in campaigns if c.get('stats', {}).get('clicks', 0) >= min_clicks]
    
    # Sort by ROI or other metrics
    sorted_campaigns = sorted(filtered, 
                            key=lambda x: x.get('stats', {}).get('roi', 0), 
                            reverse=True)
    
    return sorted_campaigns[:10]  # Top 10
```

### 2. Landing Page Analysis
```python
def analyze_landing_page_performance(campaign_id):
    """Analyze landing page performance within a campaign"""
    
    # Get campaign structure
    campaign = make_binom_request(f"/campaign/{campaign_id}")
    
    # Get landing stats
    landing_stats = make_binom_request("/stats/landing", {
        "campaignIds[]": [campaign_id],
        "groupBy": "landingId"
    })
    
    # Calculate performance metrics
    for stat in landing_stats:
        if stat.get('clicks', 0) > 0:
            stat['ctr'] = (stat.get('conversions', 0) / stat.get('clicks', 1)) * 100
            stat['cost_per_conversion'] = stat.get('cost', 0) / max(stat.get('conversions', 1), 1)
    
    return sorted(landing_stats, key=lambda x: x.get('ctr', 0), reverse=True)
```

### 3. Automated Reporting
```python
def generate_daily_report():
    """Generate automated daily performance report"""
    
    # Get yesterday's data
    campaigns = get_all_campaigns_with_stats("yesterday")
    
    # Calculate totals
    total_clicks = sum(c.get('stats', {}).get('clicks', 0) for c in campaigns)
    total_conversions = sum(c.get('stats', {}).get('conversions', 0) for c in campaigns)
    total_cost = sum(c.get('stats', {}).get('cost', 0) for c in campaigns)
    
    # Find top performers
    top_campaigns = sorted(campaigns, 
                          key=lambda x: x.get('stats', {}).get('conversions', 0), 
                          reverse=True)[:5]
    
    report = {
        "date": "yesterday",
        "summary": {
            "total_clicks": total_clicks,
            "total_conversions": total_conversions,
            "total_cost": total_cost,
            "average_ctr": (total_conversions / max(total_clicks, 1)) * 100
        },
        "top_campaigns": top_campaigns
    }
    
    return report
```

## 🔍 Endpoint Discovery for AI Agents

### By Functionality
- **CRUD Operations**: Look for endpoints with `/{id}` patterns
- **Bulk Operations**: Look for endpoints with `/multiple` or `/change_` prefixes
- **Statistics**: All endpoints under `/stats/` category
- **Information**: All endpoints under `/info/` category
- **Reporting**: All endpoints under `/report/` category

### By HTTP Method
- **GET**: Data retrieval, statistics, information
- **POST**: Create new resources, bulk operations
- **PUT**: Update existing resources
- **DELETE**: Remove resources
- **PATCH**: Partial updates, restore operations

## 🚨 Common Pitfalls for AI Agents

1. **Missing Required Parameters**: Always include `datePreset` and `timezone`
2. **Rate Limiting**: Implement delays between requests
3. **Large Data Sets**: Use pagination for datasets > 100 items
4. **Authentication**: Ensure Bearer token is correctly formatted
5. **Date Formats**: Use ISO format for custom date ranges
6. **ID Validation**: Verify resource IDs exist before operations

## 📚 Quick Reference

### Status Codes
- `200`: Success
- `400`: Bad Request (check parameters)
- `401`: Unauthorized (check API key)
- `403`: Forbidden (check permissions)
- `404`: Not Found (check endpoint/ID)
- `429`: Rate Limited (wait and retry)
- `500`: Server Error (retry later)

### Date Presets
- `today`, `yesterday`
- `this_week`, `last_week`
- `last_7_days`, `last_14_days`, `last_30_days`
- `this_month`, `last_month`
- `this_year`, `last_year`
- `all_time`, `custom_time`

---

*This guide is optimized for AI agents and will be updated as new patterns emerge.*
