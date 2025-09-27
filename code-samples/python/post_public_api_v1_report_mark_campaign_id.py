#!/usr/bin/env python3
"""
Set mark to token by campaign id.
POST /public/api/v1/report/mark/campaign/{id}
"""

import requests
import os
import json

def main():
    """
    Set mark to token by campaign id.
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

    
    try:
        response = requests.post(
            f"{BASE_URL}/public/api/v1/report/mark/campaign/123",
            headers=headers,
            params=params,
            json={
            "name": "Test Campaign",
            "trafficSourceId": 1,
            "cost": 0.1,
            "currency": "USD"
}
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
