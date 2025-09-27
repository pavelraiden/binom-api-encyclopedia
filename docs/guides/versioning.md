# API Versioning Strategy

## Version Format

Binom API follows **Semantic Versioning** (SemVer):

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Breaking changes that require code updates
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

## Current Version

- **API Version**: 2.0.0
- **Documentation Version**: 3.0.0
- **Last Updated**: 2025-09-26

## Version History

### v2.0.0 (Current)
- Complete API redesign
- New authentication method (api-key header)
- Enhanced error handling
- Custom metrics support

### v1.x.x (Deprecated)
- Legacy API version
- **End of Life**: 2025-12-31
- **Migration Required**: Yes

## Breaking Changes Policy

### Notification Timeline

1. **6 months notice** for breaking changes
2. **3 months notice** for deprecations
3. **1 month notice** for security updates

### Communication Channels

- Email notifications to registered developers
- API response headers with deprecation warnings
- Documentation updates with migration guides

## Deprecation Process

### Phase 1: Announcement (6 months)
```http
HTTP/1.1 200 OK
Deprecation: true
Sunset: Fri, 31 Dec 2025 23:59:59 GMT
Link: <https://docs.binom.org/migration>; rel="successor-version"
```

### Phase 2: Warning Period (3 months)
```http
HTTP/1.1 200 OK
Warning: 299 - "This API version will be deprecated on 2025-12-31"
```

### Phase 3: End of Life
- API returns `410 Gone` status
- Redirect to migration documentation

## Version Detection

### Request Headers
```http
GET /api/v2/campaigns
Accept: application/json
API-Version: 2.0.0
```

### Response Headers
```http
HTTP/1.1 200 OK
API-Version: 2.0.0
API-Supported-Versions: 2.0.0, 2.1.0
```

## Migration Guidelines

### From v1.x to v2.0

**Authentication Changes:**
```python
# v1.x (deprecated)
headers = {"Authorization": f"Bearer {token}"}

# v2.0 (current)
headers = {"api-key": api_key}
```

**Endpoint Changes:**
```python
# v1.x
GET /api/v1/campaign/stats

# v2.0
GET /api/v2/stats/campaign
```

### Migration Checklist

- [ ] Update authentication method
- [ ] Update endpoint URLs
- [ ] Update request/response schemas
- [ ] Test all integrations
- [ ] Update error handling
- [ ] Verify custom metrics compatibility

## Version Support Matrix

| Version | Status | Support Until | Breaking Changes |
|---------|--------|---------------|------------------|
| 2.1.x | Planned | TBD | No |
| 2.0.x | Current | 2026-12-31 | No |
| 1.x.x | Deprecated | 2025-12-31 | Yes |

## Best Practices

### For Developers

1. **Pin API Versions**: Always specify version in requests
2. **Monitor Deprecation Headers**: Check response headers regularly
3. **Test Early**: Use beta versions for testing
4. **Subscribe to Updates**: Join developer mailing list

### Version-Safe Code

```python
class BinomAPIClient:
    def __init__(self, api_key, version="2.0.0"):
        self.api_key = api_key
        self.version = version
        self.base_url = f"https://pierdun.com/public/api/v{version.split('.')[0]}"
    
    def make_request(self, endpoint, **kwargs):
        headers = {
            "api-key": self.api_key,
            "API-Version": self.version,
            "Content-Type": "application/json"
        }
        
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers, **kwargs)
        
        # Check for deprecation warnings
        if 'Deprecation' in response.headers:
            warnings.warn(f"API endpoint {endpoint} is deprecated")
        
        return response
```

## Future Roadmap

### v2.1.0 (Planned Q1 2026)
- Enhanced filtering options
- Bulk operations support
- WebSocket real-time updates

### v3.0.0 (Planned Q3 2026)
- GraphQL support
- Enhanced security features
- Performance improvements

## Support and Migration Help

- **Documentation**: https://docs.binom.org/migration
- **Support Email**: api-support@binom.org
- **Migration Tools**: Available in developer dashboard
- **Community Forum**: https://community.binom.org
