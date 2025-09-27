#!/usr/bin/env python3
"""
This script fetches real API responses for all documented endpoints and saves them as JSON files.
It reads the correct endpoint paths and methods from the encyclopedia.json file and provides dummy data for POST/PUT requests.
"""

import os
import json
from pathlib import Path
import requests

API_KEY = os.getenv("binomPublic")
BASE_URL = "https://pierdun.com/public/api/v1"
HEADERS = {
    "api-key": API_KEY,
    "Content-Type": "application/json"
}

STATS_PARAMS = {
    "datePreset": "last_7_days",
    "timezone": "UTC"
}

def get_endpoints_from_encyclopedia():
    """Returns a dictionary of endpoints with their methods from encyclopedia.json."""
    encyclopedia_path = Path("/home/ubuntu/binom-api-encyclopedia/encyclopedia.json")
    with open(encyclopedia_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {endpoint: details['method'] for endpoint, details in data["endpoints"].items()}

def generate_dummy_data(endpoint):
    """Generates dummy data for POST/PUT requests based on the endpoint."""
    if "campaign" in endpoint:
        return {"name": "Test Campaign", "trafficSourceId": 1}
    if "offer" in endpoint:
        return {"name": "Test Offer"}
    if "landing" in endpoint:
        return {"name": "Test Landing"}
    return {}

def fetch_and_save_examples():
    """Fetches real API responses and saves them to files."""
    endpoints = get_endpoints_from_encyclopedia()
    output_dir = Path("/home/ubuntu/binom-api-encyclopedia/docs/examples/responses")
    output_dir.mkdir(exist_ok=True)

    print(f"--- Starting to fetch {len(endpoints)} API examples (Advanced) ---")

    for endpoint, method in endpoints.items():
        if "{" in endpoint:
            print(f"SKIPPING dynamic endpoint: {endpoint}")
            continue

        params = STATS_PARAMS if "stats" in endpoint else {}
        url = BASE_URL + endpoint

        try:
            response = None
            if method == "GET":
                response = requests.get(url, headers=HEADERS, params=params)
            elif method == "POST":
                dummy_data = generate_dummy_data(endpoint)
                response = requests.post(url, headers=HEADERS, json=dummy_data, params=params)
            elif method == "PUT":
                dummy_data = generate_dummy_data(endpoint)
                response = requests.put(url, headers=HEADERS, json=dummy_data, params=params)
            else: # For DELETE and other methods, we don't expect a body
                response = requests.request(method, url, headers=HEADERS, params=params)

            if response is not None:
                if response.status_code in [200, 201, 204]:
                    output_filename = endpoint.replace("/", "_").strip("_") + ".json"
                    output_path = output_dir / output_filename
                    if response.content:
                        with open(output_path, "w", encoding="utf-8") as f:
                            json.dump(response.json(), f, indent=4, ensure_ascii=False)
                        print(f"✅ SUCCESS ({method}): Saved example for {endpoint} to {output_path}")
                    else:
                        print(f"✅ SUCCESS ({method}): Received empty response for {endpoint}")
                else:
                    print(f"❌ FAILED ({method}) for {endpoint}: Status {response.status_code} - {response.text[:100]}...")

        except requests.exceptions.RequestException as e:
            print(f"❌ FAILED ({method}) for {endpoint}: Request failed with exception: {e}")

    print("\n--- Finished fetching API examples (Advanced) ---")

if __name__ == "__main__":
    if not API_KEY:
        print("CRITICAL ERROR: `binomPublic` environment variable not set.")
    else:
        fetch_and_save_examples()

