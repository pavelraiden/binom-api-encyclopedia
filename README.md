# Binom API Encyclopedia

Complete documentation and examples for Binom API v2 - designed for AI agents and developers.

## 📊 Overview

- **Total Endpoints**: 177
- **API Version**: v2
- **Base URL**: `https://pierdun.com/public/api/v1`
- **Authentication**: Bearer Token
- **Documentation Status**: ✅ Complete with examples and schemas
- **Last Updated**: September 2025

## 🚀 Quick Start

```python
import requests
import os

API_KEY = os.getenv('binomPublic')
BASE_URL = "https://pierdun.com/public/api/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Example: Get campaigns info
response = requests.get(
    f"{BASE_URL}/info/campaign",
    headers=headers,
    params={
        "datePreset": "last_7_days",
        "timezone": "UTC",
        "limit": 100
    }
)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code} - {response.text}")
```

## 📚 API Categories

### [Affiliate Network](docs/endpoints/affiliate_network/README.md) (10 endpoints)

- **GET** `/public/api/v1/affiliate_network/{id}/clone` - Clone Affiliate Network.
- **POST** `/public/api/v1/affiliate_network` - Create Affiliate Network.
- **GET** `/public/api/v1/affiliate_network/{id}` - Get Affiliate Network details.
- ... and 7 more endpoints

### [Auth](docs/endpoints/auth/README.md) (2 endpoints)

- **GET** `/public/api/v1/user/role` - User Role.
- **POST** `/public/api/v1/user/logout` - User Logout.

### [Binom Protect](docs/endpoints/binom_protect/README.md) (7 endpoints)

*Bot protection and security features*

- **POST** `/public/api/v1/binom/protect/beta/disable` - Disable Beta
- **GET** `/public/api/v1/binom/protect/beta/status` - Get Beta status
- **GET** `/public/api/v1/binom/protect/methods` - Get available bot detection methods and presets
- ... and 4 more endpoints

### [Campaign](docs/endpoints/campaign/README.md) (24 endpoints)

*Create, manage, and optimize advertising campaigns*

- **POST** `/public/api/v1/campaign/change_setting` - Edit Settings for multiple Campaigns
- **POST** `/public/api/v1/campaign/change_cost` - Change cost for multiple Campaigns
- **POST** `/public/api/v1/campaign/change_domain` - Change Domain for multiple Campaigns
- ... and 21 more endpoints

### [Clicks](docs/endpoints/clicks/README.md) (2 endpoints)

*Track and manage click data*

- **PUT** `/public/api/v1/clicks/campaign/{id}` - Update campaign`s clicks cost.
- **DELETE** `/public/api/v1/clicks/campaign/{id}` - Delete campaign`s clicks.

### [Conversion](docs/endpoints/conversion/README.md) (8 endpoints)

*Handle conversion tracking and management*

- **GET** `/public/api/v1/conversion/{id}/clone` - Clone Conversion.
- **POST** `/public/api/v1/conversion` - Create Conversion.
- **GET** `/public/api/v1/conversion/{id}` - Get Conversion.
- ... and 5 more endpoints

### [Csv](docs/endpoints/csv/README.md) (7 endpoints)

- **DELETE** `/public/api/v1/csv/clicklog/clear` - Delete all clicklog files.
- **DELETE** `/public/api/v1/csv/conversions/clear` - Delete all conversion files.
- **GET** `/public/api/v1/csv/file/{filename}` - Download file by name.
- ... and 4 more endpoints

### [Domain](docs/endpoints/domain/README.md) (8 endpoints)

- **GET** `/public/api/v1/domain/{id}/clone` - Clone Domain.
- **POST** `/public/api/v1/domain` - Create Domain.
- **GET** `/public/api/v1/domain/{id}` - Get Domain.
- ... and 5 more endpoints

### [Group](docs/endpoints/group/README.md) (8 endpoints)

- **GET** `/public/api/v1/group/{id}/clone` - Clone Group.
- **POST** `/public/api/v1/group` - Create Group.
- **GET** `/public/api/v1/group/{id}` - Get Group.
- ... and 5 more endpoints

### [Identity](docs/endpoints/identity/README.md) (9 endpoints)

*Identity and access management*

- **POST** `/public/api/v1/identity/api_key/block/{id}` - Identity Block ApiKey
- **GET** `/public/api/v1/identity/api_key/{id}` - Identity Get ApiKey
- **PUT** `/public/api/v1/identity/api_key/refresh/{id}` - Identity Refresh ApiKey
- ... and 6 more endpoints

### [Info](docs/endpoints/info/README.md) (6 endpoints)

*Get basic information about resources*

- **GET** `/public/api/v1/info/affiliate_network` - Get traffic sources info.
- **GET** `/public/api/v1/info/campaign` - Get campaigns info.
- **GET** `/public/api/v1/info/landing` - Get landings info.
- ... and 3 more endpoints

### [Landing](docs/endpoints/landing/README.md) (8 endpoints)

*Manage landing pages and their configurations*

- **GET** `/public/api/v1/landing/{id}/clone` - Clone Landing.
- **POST** `/public/api/v1/landing` - Create Landing.
- **GET** `/public/api/v1/landing/{id}` - Get Landing.
- ... and 5 more endpoints

### [Offer](docs/endpoints/offer/README.md) (8 endpoints)

*Handle affiliate offers and payouts*

- **GET** `/public/api/v1/offer/{id}/clone` - Clone Offer.
- **POST** `/public/api/v1/offer` - Create Offer.
- **GET** `/public/api/v1/offer/{id}` - Get Offer.
- ... and 5 more endpoints

### [Report](docs/endpoints/report/README.md) (2 endpoints)

*Generate and manage custom reports*

- **GET** `/public/api/v1/report/{page}` - Get Report.
- **GET** `/public/api/v1/report/user/campaign` - Get user campaigns Report.

### [Report Filters](docs/endpoints/report_filters/README.md) (5 endpoints)

- **POST** `/public/api/v1/report/simple_filter/{subject}/{uuid}` - Create Simple filter.
- **PUT** `/public/api/v1/report/simple_filter/{uuid}` - Edit Simple filter.
- **DELETE** `/public/api/v1/report/simple_filter/{uuid}` - Delete Simple filter.
- ... and 2 more endpoints

### [Report Groupings](docs/endpoints/report_groupings/README.md) (8 endpoints)

- **GET** `/public/api/v1/report/affiliate_network/groupings` - Get Affiliate network Groupings for single aggregate.
- **GET** `/public/api/v1/report/campaign/groupings` - Get Campaign Groupings for single aggregate.
- **GET** `/public/api/v1/report/campaign/groupings/multiple` - Get Groupings for multiple aggregates.
- ... and 5 more endpoints

### [Report Mark](docs/endpoints/report_mark/README.md) (6 endpoints)

- **POST** `/public/api/v1/report/mark/campaign/{id}` - Set mark to token by campaign id.
- **DELETE** `/public/api/v1/report/mark/campaign/{id}` - Delete mark for token by campaign id.
- **POST** `/public/api/v1/report/mark/traffic_source/{id}` - Set mark to token by traffic source id.
- ... and 3 more endpoints

### [Report Presets](docs/endpoints/report_presets/README.md) (3 endpoints)

- **POST** `/public/api/v1/report/preset/{subject}/{uuid}` - Create preset.
- **DELETE** `/public/api/v1/report/preset/{uuid}` - Delete preset.
- **GET** `/public/api/v1/report/preset/{subject}` - Get presets by Subject.

### [Rotation](docs/endpoints/rotation/README.md) (11 endpoints)

- **PUT** `/public/api/v1/campaign/landing/pause` - Pause landing in campaign.
- **PUT** `/public/api/v1/campaign/offer/pause` - Pause offer in campaign.
- **PUT** `/public/api/v1/campaign/path/pause` - Pause path in campaign.
- ... and 8 more endpoints

### [Stats](docs/endpoints/stats/README.md) (6 endpoints)

*Retrieve performance statistics and analytics data*

- **GET** `/public/api/v1/stats/affiliate_network` - Get stats Affiliate Network.
- **GET** `/public/api/v1/stats/campaign` - Get stats Campaign.
- **GET** `/public/api/v1/stats/landing` - Get stats Landing.
- ... and 3 more endpoints

### [Traffic Source](docs/endpoints/traffic_source/README.md) (9 endpoints)

*Configure and manage traffic sources*

- **GET** `/public/api/v1/traffic_source/{id}/clone` - Clone Traffic Source.
- **POST** `/public/api/v1/traffic_source` - Create Traffic Source.
- **GET** `/public/api/v1/traffic_source/{id}` - Get Traffic Source.
- ... and 6 more endpoints

### [Trends](docs/endpoints/trends/README.md) (1 endpoints)

- **GET** `/public/api/v1/trends` - Get Trends.

### [User](docs/endpoints/user/README.md) (16 endpoints)

*User management and authentication*

- **PUT** `/public/api/v1/user/change_login` - Change User Login.
- **PUT** `/public/api/v1/user/change_password` - Change User Password.
- **POST** `/public/api/v1/user/create` - Create User
- ... and 13 more endpoints

### [User Access](docs/endpoints/user_access/README.md) (3 endpoints)

- **GET** `/public/api/v1/user/{adminId}/accessible-users` - Accessible Users of Admin.
- **POST** `/public/api/v1/user/{adminId}/accessible-users` - Set Accessible Users for Admin.
- **GET** `/public/api/v1/users/accessible` - Accessible Users.


## 🤖 AI Agent Features

This encyclopedia is specifically designed for AI agents with:

- ✅ **Complete endpoint documentation** with parameters, schemas, and examples
- ✅ **Ready-to-use code samples** in Python and cURL
- ✅ **JSON schemas** for request/response validation
- ✅ **AI-optimized guides** with best practices and common patterns
- ✅ **Error handling examples** for robust implementations
- ✅ **Workflow integration tips** for complex operations

## 📖 Documentation Structure

```
binom-api-encyclopedia/
├── docs/
│   ├── endpoints/          # Complete endpoint documentation
│   │   ├── campaign/       # Campaign management endpoints
│   │   ├── stats/          # Statistics and analytics
│   │   ├── report/         # Reporting endpoints
│   │   └── ...            # Other categories
│   ├── schemas/           # JSON schemas for validation
│   └── examples/          # Usage examples and tutorials
├── code-samples/          # Ready-to-use code samples
│   ├── python/           # Python implementations
│   └── curl/             # cURL examples
├── ai-guides/            # AI-specific guides and patterns
└── utils/                # Utilities and helper tools
```

## 🔧 Authentication

All API requests require Bearer token authentication:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     "https://pierdun.com/public/api/v1/info/campaign?datePreset=today&timezone=UTC"
```

## 📋 Required Parameters

Most endpoints require these parameters:
- `datePreset`: Time period (e.g., "last_7_days", "today", "yesterday")
- `timezone`: Timezone (e.g., "UTC")

## 🎯 Common Use Cases

### Campaign Management
```python
# Get campaign performance
campaigns = get_campaigns_with_stats("last_30_days")
top_performers = sorted(campaigns, key=lambda x: x.get('roi', 0), reverse=True)[:10]
```

### Landing Page Optimization
```python
# Analyze landing page performance
landing_stats = get_landing_stats(campaign_id, "last_7_days")
best_landing = max(landing_stats, key=lambda x: x.get('conversion_rate', 0))
```

### Automated Reporting
```python
# Generate daily performance report
daily_report = generate_performance_report("yesterday")
send_report_email(daily_report)
```

## 🔗 Links

- [Official Binom Documentation](https://docs.binom.org/)
- [API Documentation](https://pierdun.com/api/doc)
- [AI Agent Guide](ai-guides/AI_AGENT_GUIDE.md)

## 📊 Statistics

- **Total Endpoints**: 177
- **With Parameters**: 133
- **With Request Body**: 78
- **With Examples**: 177
- **Categories**: 24

## 📄 License

This documentation is created for educational and development purposes.

---

*Generated automatically from Binom API v2 specification*  
*Optimized for AI agents and automated workflows*
