#!/usr/bin/env python3
"""
Generate two-factor secrets for current user, when two-factor authentication is disabled
PUT /public/api/v1/user/2fa/secret/generate
"""

import requests
import os
import json

def main():
    """
    Generate two-factor secrets for current user, when two-factor authentication is disabled
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
        response = requests.put(
            f"{BASE_URL}/public/api/v1/user/2fa/secret/generate",
            headers=headers,
            params=params,
            json={
            "name": "Example Resource"
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
