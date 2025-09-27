
import os
import requests

# Get the API key from environment variables
API_KEY = os.getenv('binomPublic')
BASE_URL = "https://pierdun.com/public/api/v1"

# --- Headers for testing ---
HEADERS_API_KEY = {
    "api-key": API_KEY,
    "Content-Type": "application/json"
}

HEADERS_BEARER = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# --- Endpoints to test ---
ENDPOINTS_TO_TEST = [
    "/info/offer",
    "/info/campaign",
    "/stats/campaign"
]

# --- Required parameters for stats endpoints ---
STATS_PARAMS = {
    "datePreset": "last_7_days",
    "timezone": "UTC"
}

def run_auth_test():
    """Tests both api-key and Bearer token authentication methods."""
    print("--- Starting Binom API Authentication Test ---")

    for endpoint in ENDPOINTS_TO_TEST:
        print(f"\n--- Testing Endpoint: {endpoint} ---")
        
        params = STATS_PARAMS if 'stats' in endpoint else {}

        # Test 1: api-key header
        try:
            response_api_key = requests.get(BASE_URL + endpoint, headers=HEADERS_API_KEY, params=params)
            print(f"1.  `api-key` header: Status Code = {response_api_key.status_code}")
            if response_api_key.status_code == 200:
                print("    ✅ SUCCESS: Received data.")
            else:
                print(f"    ❌ FAILED: Response: {response_api_key.text[:100]}...")
        except requests.exceptions.RequestException as e:
            print(f"    ❌ FAILED: Request with `api-key` header failed with exception: {e}")

        # Test 2: Bearer token header
        try:
            response_bearer = requests.get(BASE_URL + endpoint, headers=HEADERS_BEARER, params=params)
            print(f"2.  `Bearer` token:   Status Code = {response_bearer.status_code}")
            if response_bearer.status_code == 200:
                print("    ✅ SUCCESS: Received data.")
            else:
                print(f"    ❌ FAILED: Response: {response_bearer.text[:100]}...")
        except requests.exceptions.RequestException as e:
            print(f"    ❌ FAILED: Request with `Bearer` token failed with exception: {e}")

    print("\n--- Authentication Test Finished ---")

if __name__ == "__main__":
    if not API_KEY:
        print("CRITICAL ERROR: `binomPublic` environment variable not set.")
    else:
        run_auth_test()

