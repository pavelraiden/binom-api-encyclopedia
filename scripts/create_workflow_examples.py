"""
This script demonstrates a real-world API workflow by creating a complete campaign setup.
It now uses the correct payload structure for each resource.
"""

import os
import json
import requests
import time
from pathlib import Path

API_KEY = os.getenv("binomPublic")
BASE_URL = "https://pierdun.com/public/api/v1"
HEADERS = {
    "api-key": API_KEY,
    "Content-Type": "application/json"
}

def create_resource(endpoint, payload, resource_name):
    """Generic function to create a resource and return its ID."""
    try:
        response = requests.post(BASE_URL + endpoint, headers=HEADERS, json=payload)
        if response.status_code in [200, 201]:
            response_data = response.json()
            resource_id = response_data.get("id")
            if resource_id:
                print(f"✅ SUCCESS: Created {resource_name} with ID: {resource_id}")
                return resource_id
            else:
                print(f"❌ FAILED: Could not find 'id' in response for {resource_name}. Full response: {response.json()}")
                return None
        else:
            print(f"❌ FAILED to create {resource_name}: Status {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED to create {resource_name} with exception: {e}")
        return None

def run_workflow():
    print("--- Starting Real-World API Workflow (Corrected Payloads) ---")
    timestamp = int(time.time())

    # 1. Create Traffic Source (flat structure)
    ts_name = f"Workflow TS {timestamp}"
    ts_payload = {"name": ts_name, "postback_url": "http://test.com", "s2sMode": "FIRST"}
    traffic_source_id = create_resource("/traffic_source", ts_payload, ts_name)
    if not traffic_source_id:
        return

    # 2. Create Offer (nested structure)
    offer_name = f"Workflow Offer {timestamp}"
    offer_payload = {"offer": {"name": offer_name, "url": "http://offer.com"}}
    offer_id = create_resource("/offer", offer_payload, offer_name)
    if not offer_id:
        return

    # 3. Create Landing Page (nested structure)
    landing_name = f"Workflow Landing {timestamp}"
    landing_payload = {"landing": {"name": landing_name, "url": "http://landing.com"}}
    landing_id = create_resource("/landing", landing_payload, landing_name)
    if not landing_id:
        return

    # 4. Create Campaign (flat structure)
    campaign_name = f"Workflow Campaign {timestamp}"
    campaign_payload = {
        "name": campaign_name,
        "traffic_source_id": traffic_source_id,
        "paths": [
            {
                "landings": [{"id": landing_id, "share": 100}],
                "offers": [{"id": offer_id, "share": 100}],
                "share": 100
            }
        ]
    }
    campaign_id = create_resource("/campaign", campaign_payload, campaign_name)
    if not campaign_id:
        return

    # 5. Verify Campaign Creation
    print(f"\n--- Verifying creation of Campaign ID: {campaign_id} ---")
    try:
        response = requests.get(f"{BASE_URL}/campaign/{campaign_id}", headers=HEADERS)
        if response.status_code == 200:
            print("✅ SUCCESS: Campaign details fetched successfully.")
            output_path = Path("/home/ubuntu/binom-api-encyclopedia/docs/examples/responses/workflow_created_campaign.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(response.json(), f, indent=4, ensure_ascii=False)
            print(f"Saved campaign example to {output_path}")
        else:
            print(f"❌ FAILED to verify campaign: Status {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED to verify campaign with exception: {e}")

    print("\n--- Real-World API Workflow Finished ---")

if __name__ == "__main__":
    if not API_KEY:
        print("CRITICAL ERROR: `binomPublic` environment variable not set.")
    else:
        run_workflow()

