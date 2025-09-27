# GET /info/offer

## Description
Retrieves information about all offers in the system.

## Endpoint
```
GET /info/offer
```

## Authentication
```
Headers:
  api-key: {your_api_key}
```

## Required Parameters
- `datePreset` (string): Time period for data retrieval
  - Possible values: `today`, `yesterday`, `last_7_days`, `last_30_days`, `this_month`, `last_month`, etc.
- `timezone` (string): Timezone for date calculations
  - Example: `UTC`, `America/New_York`, `Europe/London`

## Optional Parameters
- `limit` (integer): Maximum number of records to return (default: 100)
- `offset` (integer): Number of records to skip (default: 0)
- `status` (string): Filter by offer status
  - Possible values: `active`, `paused`, `deleted`

## Example Request
```bash
curl -X GET "https://pierdun.com/public/api/v1/info/offer" \
  -H "api-key: your_api_key_here" \
  -G \
  -d "datePreset=last_7_days" \
  -d "timezone=UTC" \
  -d "limit=50"
```

## Example Response
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "Example Offer",
      "url": "https://example.com/offer",
      "status": "active",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-15T12:30:00Z",
      "payout": 10.50,
      "currency": "USD"
    }
  ],
  "pagination": {
    "total": 25,
    "limit": 50,
    "offset": 0
  }
}
```

## Error Responses
- `400 Bad Request`: Missing required parameters (datePreset, timezone)
- `401 Unauthorized`: Invalid or missing API key
- `500 Internal Server Error`: Server error

## AI Agent Notes
- This endpoint has **high stability** (>90% success rate)
- Safe for automated use in workflows
- Always include both `datePreset` and `timezone` parameters
- Use for offer discovery and validation workflows
