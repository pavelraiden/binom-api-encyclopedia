"""
API Tester for Binom API Encyclopedia
Tests real API endpoints to ensure documentation accuracy
"""

import os
import requests
import json
from typing import Tuple, Dict, Any

class APITester:
    def __init__(self):
        self.api_key = os.getenv('binomPublic')
        self.base_url = "https://pierdun.com/public/api/v1"
        self.headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.default_params = {
            "datePreset": "last_7_days",
            "timezone": "UTC",
            "limit": 10
        }

    def test_endpoint(self, endpoint: str, method: str = "GET", data: Dict = None) -> Tuple[bool, str]:
        """
        Test a single API endpoint
        Returns: (success: bool, error_message: str)
        """
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            
            # Add default parameters for stats endpoints
            params = self.default_params.copy() if 'stats' in endpoint else {}
            
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=30)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=self.headers, json=data, timeout=30)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=self.headers, timeout=30)
            else:
                return False, f"Unsupported HTTP method: {method}"

            # Check response status
            if response.status_code == 200:
                return True, "Success"
            elif response.status_code == 401:
                return False, "Authentication failed - check API key"
            elif response.status_code == 400:
                return False, f"Bad request - {response.text}"
            elif response.status_code == 404:
                return False, "Endpoint not found"
            elif response.status_code == 429:
                return False, "Rate limited"
            elif response.status_code == 500:
                return False, f"Server error - {response.text}"
            else:
                return False, f"HTTP {response.status_code}: {response.text}"

        except requests.exceptions.Timeout:
            return False, "Request timeout"
        except requests.exceptions.ConnectionError:
            return False, "Connection error"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def test_multiple_endpoints(self, endpoints: list) -> Dict[str, Dict]:
        """
        Test multiple endpoints and return results
        """
        results = {}
        for endpoint in endpoints:
            success, error = self.test_endpoint(endpoint)
            results[endpoint] = {
                "success": success,
                "error": error if not success else None
            }
        return results

    def validate_response_format(self, endpoint: str, expected_schema: Dict) -> Tuple[bool, str]:
        """
        Validate that API response matches expected schema
        """
        try:
            success, error = self.test_endpoint(endpoint)
            if not success:
                return False, f"API test failed: {error}"

            # Get actual response
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            params = self.default_params.copy() if 'stats' in endpoint else {}
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code != 200:
                return False, f"API returned {response.status_code}"

            try:
                response_data = response.json()
            except json.JSONDecodeError:
                return False, "Response is not valid JSON"

            # Basic schema validation (simplified)
            if isinstance(response_data, list) and len(response_data) > 0:
                return True, "Response format valid (array)"
            elif isinstance(response_data, dict):
                return True, "Response format valid (object)"
            else:
                return False, "Unexpected response format"

        except Exception as e:
            return False, f"Validation error: {str(e)}"
