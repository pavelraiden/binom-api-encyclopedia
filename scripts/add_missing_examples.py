#!/usr/bin/env python3
"""
This script adds boilerplate Python and cURL code examples to endpoint
documentation files that are missing them.
"""

import os
import re
import json
from pathlib import Path

ENCYCLOPEDIA_PATH = Path("/home/ubuntu/binom-api-encyclopedia/encyclopedia.json")
ENDPOINTS_DOCS_PATH = Path("/home/ubuntu/binom-api-encyclopedia/docs/endpoints")

def get_endpoint_details():
    """Loads endpoint details (method) from the encyclopedia."""
    with open(ENCYCLOPEDIA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {endpoint: details.get("method", "GET") for endpoint, details in data["endpoints"].items()}

def generate_python_example(endpoint, method):
    """Generates a boilerplate Python code example."""
    data_param = ""
    if method in ["POST", "PUT"]:
        data_param = ", json={}" # Basic dummy data

    return f"""```python
import os
import requests

API_KEY = os.getenv('binomPublic')
BASE_URL = "https://pierdun.com/public/api/v1"
HEADERS = {{
    "api-key": API_KEY,
    "Content-Type": "application/json"
}}

# Define parameters and data if required by the endpoint
params = {{}}
data = {{}}

response = requests.request(
    "{method}",
    BASE_URL + "{endpoint}",
    headers=HEADERS,
    params=params,
    json=data
)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {{response.status_code}} - {{response.text}}")
```"""

def generate_curl_example(endpoint, method):
    """Generates a boilerplate cURL code example."""
    data_param = ""
    if method in ["POST", "PUT"]:
       data_param = "--data-raw '{}'"
    return f"""```curl
curl --request {method} \
  --url https://pierdun.com/public/api/v1{endpoint} \
  --header 'api-key: YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  {data_param}
```"""

def add_missing_examples():
    """Adds missing code examples to markdown files."""
    endpoint_details = get_endpoint_details()
    md_files = list(ENDPOINTS_DOCS_PATH.rglob("*.md"))
    files_updated = 0

    print(f"--- Scanning {len(md_files)} files for missing examples ---\n")

    # Regex to find any code block
    code_block_regex = re.compile(r"```(python|curl)", re.DOTALL)

    # Create a mapping from file path to endpoint path
    file_to_endpoint = {}
    for endpoint in endpoint_details.keys():
        # Construct a file path from the endpoint path
        file_path_str = str(ENDPOINTS_DOCS_PATH) + endpoint + ".md"
        file_to_endpoint[Path(file_path_str)] = endpoint

    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        if not code_block_regex.search(content):
            # Find the corresponding endpoint path
            endpoint_path = None
            # This is a bit fragile, depends on directory structure matching the API path
            try:
                endpoint_path = "/" + "/".join(md_file.relative_to(ENDPOINTS_DOCS_PATH).with_suffix('').parts)
            except ValueError:
                print(f"Could not determine endpoint for {md_file}, skipping.")
                continue

            if endpoint_path in endpoint_details:
                method = endpoint_details[endpoint_path]
                print(f"  - Adding examples to {md_file.name} for endpoint {endpoint_path} ({method})")

                python_example = generate_python_example(endpoint_path, method)
                curl_example = generate_curl_example(endpoint_path, method)

                # Append the new examples to the file
                with md_file.open("a", encoding="utf-8") as f:
                    f.write("\n\n### Python Example\n")
                    f.write(python_example)
                    f.write("\n\n### cURL Example\n")
                    f.write(curl_example)
                
                files_updated += 1
            else:
                print(f"  - WARNING: No endpoint details found for {md_file.name} (Path: {endpoint_path})")

    print(f"\n--- Finished adding examples. {files_updated} files were updated. ---")

if __name__ == "__main__":
    add_missing_examples()

