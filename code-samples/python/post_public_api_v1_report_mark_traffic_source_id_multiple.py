#!/usr/bin/env python3
"""
Set mark to multiple tokens by traffic source id.
POST /public/api/v1/report/mark/traffic_source/{id}/multiple
"""

import requests
import os
import json

def main():
    """
    Set mark to multiple tokens by traffic source id.
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
            f"{BASE_URL}/public/api/v1/report/mark/traffic_source/123/multiple",
            headers=headers,
            params=params,
            json={
            "token": "click_id",
            "tokenValue": "accepted",
            "mark": "mints"
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
