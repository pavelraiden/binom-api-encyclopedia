#!/usr/bin/env python3
"""
This script fetches real API responses for all documented endpoints and saves them as JSON files.
It reads the correct endpoint paths from the encyclopedia.json file.
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
    """Returns a list of all endpoint paths from encyclopedia.json."""
    encyclopedia_path = Path("/home/ubuntu/binom-api-encyclopedia/encyclopedia.json")
    with open(encyclopedia_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return list(data["endpoints"].keys())

def fetch_and_save_examples():
    """Fetches real API responses and saves them to files."""
    endpoints = get_endpoints_from_encyclopedia()
    output_dir = Path("/home/ubuntu/binom-api-encyclopedia/docs/examples/responses")
    output_dir.mkdir(exist_ok=True)

    print(f"--- Starting to fetch {len(endpoints)} API examples ---")

    for endpoint in endpoints:
        # Skip dynamic endpoints for now
        if "{" in endpoint:
            print(f"SKIPPING dynamic endpoint: {endpoint}")
            continue

        params = STATS_PARAMS if "stats" in endpoint else {}

        try:
            # Only perform GET requests for this automated script
            response = requests.get(BASE_URL + endpoint, headers=HEADERS, params=params)
            
            if response.status_code == 200:
                # Save the response
                output_filename = endpoint.replace("/", "_").strip("_") + ".json"
                output_path = output_dir / output_filename
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(response.json(), f, indent=4, ensure_ascii=False)
                print(f"✅ SUCCESS: Saved example for {endpoint} to {output_path}")
            else:
                print(f"❌ FAILED for {endpoint}: Status {response.status_code} - {response.text[:100]}...")

        except requests.exceptions.RequestException as e:
            print(f"❌ FAILED for {endpoint}: Request failed with exception: {e}")

    print("\n--- Finished fetching API examples ---")
if __name__ == "__main__":
    if not API_KEY:
        print("CRITICAL ERROR: `binomPublic` environment variable not set.")
    else:
        fetch_and_save_examples()

