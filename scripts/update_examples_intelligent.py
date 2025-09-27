#!/usr/bin/env python3
"""
This script intelligently fetches real API responses for all documented endpoints.
It reads the request_schema from encyclopedia.json to generate valid dummy data for POST/PUT requests.
"""

import os
import json
from pathlib import Path
import requests
import random
import string

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
    """Returns a dictionary of endpoints with their details from encyclopedia.json."""
    encyclopedia_path = Path("/home/ubuntu/binom-api-encyclopedia/encyclopedia.json")
    with open(encyclopedia_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["endpoints"]

def generate_value_from_schema(schema):
    """Generates a dummy value based on a JSON schema property."""
    if not isinstance(schema, dict):
        return None
    
    schema_type = schema.get("type")
    if schema_type == "string":
        return ''.join(random.choices(string.ascii_lowercase, k=10))
    elif schema_type == "integer":
        return random.randint(1, 100)
    elif schema_type == "number":
        return round(random.uniform(1.0, 100.0), 2)
    elif schema_type == "boolean":
        return random.choice([True, False])
    elif schema_type == "array":
        return []
    elif schema_type == "object":
        return {}
    return None

def generate_dummy_data_from_schema(schema):
    """Generates dummy data for POST/PUT requests based on the request_schema."""
    if not schema or "properties" not in schema:
        return {}
    
    data = {}
    for key, prop_schema in schema["properties"].items():
        data[key] = generate_value_from_schema(prop_schema)
    return data

def fetch_and_save_examples():
    """Fetches real API responses and saves them to files."""
    endpoints_details = get_endpoints_from_encyclopedia()
    output_dir = Path("/home/ubuntu/binom-api-encyclopedia/docs/examples/responses")
    output_dir.mkdir(exist_ok=True)

    print(f"--- Starting to fetch {len(endpoints_details)} API examples (Intelligent) ---")

    for endpoint, details in endpoints_details.items():
        method = details.get("method", "GET")
        
        if "{" in endpoint:
            print(f"SKIPPING dynamic endpoint: {endpoint}")
            continue

        params = STATS_PARAMS if "stats" in endpoint else {}
        url = BASE_URL + endpoint

        try:
            response = None
            if method == "GET":
                response = requests.get(url, headers=HEADERS, params=params)
            elif method in ["POST", "PUT"]:
                request_schema = details.get("request_schema", {})
                dummy_data = generate_dummy_data_from_schema(request_schema)
                if method == "POST":
                    response = requests.post(url, headers=HEADERS, json=dummy_data, params=params)
                else: # PUT
                    response = requests.put(url, headers=HEADERS, json=dummy_data, params=params)
            else: # For DELETE and other methods
                response = requests.request(method, url, headers=HEADERS, params=params)

            if response is not None:
                if response.status_code in [200, 201, 204]:
                    output_filename = endpoint.replace("/", "_").strip("_") + ".json"
                    output_path = output_dir / output_filename
                    if response.content:
                        try:
                            with open(output_path, "w", encoding="utf-8") as f:
                                json.dump(response.json(), f, indent=4, ensure_ascii=False)
                            print(f"✅ SUCCESS ({method}): Saved example for {endpoint} to {output_path}")
                        except json.JSONDecodeError:
                             print(f"✅ SUCCESS ({method}): Received non-JSON response for {endpoint}")
                    else:
                        print(f"✅ SUCCESS ({method}): Received empty response for {endpoint}")
                else:
                    print(f"❌ FAILED ({method}) for {endpoint}: Status {response.status_code} - {response.text[:100]}...")

        except requests.exceptions.RequestException as e:
            print(f"❌ FAILED ({method}) for {endpoint}: Request failed with exception: {e}")

    print("\n--- Finished fetching API examples (Intelligent) ---")

if __name__ == "__main__":
    if not API_KEY:
        print("CRITICAL ERROR: `binomPublic` environment variable not set.")
    else:
        fetch_and_save_examples()

