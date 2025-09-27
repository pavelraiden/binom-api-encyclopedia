#!/usr/bin/env python3
"""
Get Rotation list filtered.
GET /public/api/v1/rotation/list/filtered
"""

import requests
import os
import json

def main():
    """
    Get Rotation list filtered.
    """
    
    API_KEY = os.getenv('binomPublic')
    if not API_KEY:
        print("❌ Error: binomPublic environment variable not set")
        return None
    
    BASE_URL = "https://pierdun.com/public/api/v1"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Parameters
    params = {}
    params["datePreset"] = "last_7_days"  # Time period filter (e.g., 'last_7_days', 'today', 'yesterday')
    params["timezone"] = "UTC"  # Timezone for date calculations (e.g., 'UTC')
    # params["limit"] = "VALUE"  # Maximum number of records to return (max 1000) (optional)
    # params["offset"] = "VALUE"  # Number of records to skip for pagination (optional)
    # params["sortColumn"] = "VALUE"  # Column to sort by (optional)
    # params["sortType"] = "VALUE"  # Sort direction (optional)

    
    try:
        response = requests.get(
            f"{BASE_URL}/public/api/v1/rotation/list/filtered",
            headers=headers,
            params=params
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            print("✅ Success!")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return data
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

if __name__ == "__main__":
    result = main()
