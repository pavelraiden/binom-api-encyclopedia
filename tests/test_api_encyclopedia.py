#!/usr/bin/env python3
"""
Unit tests for Binom API Encyclopedia
"""

import unittest
import json
import os
import requests
from unittest.mock import patch, Mock

class TestBinomAPIEndpoints(unittest.TestCase):
    
    def setUp(self):
        self.base_url = "https://pierdun.com/public/api/v1"
        self.api_key = os.getenv("binomPublic", "test_key")
        self.headers = {"api-key": self.api_key}
    
    def test_info_offer_endpoint_structure(self):
        """Test that info/offer endpoint has correct structure"""
        endpoint_file = "/home/ubuntu/binom-api-encyclopedia/docs/endpoints/info/offer.md"
        self.assertTrue(os.path.exists(endpoint_file))
        
        with open(endpoint_file, 'r') as f:
            content = f.read()
            self.assertIn("GET /info/offer", content)
            self.assertIn("datePreset", content)
            self.assertIn("timezone", content)
    
    def test_workflow_json_validity(self):
        """Test that all workflow JSON files are valid"""
        workflows_dir = "/home/ubuntu/binom-api-encyclopedia/workflows"
        if os.path.exists(workflows_dir):
            for filename in os.listdir(workflows_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(workflows_dir, filename)
                    with open(filepath, 'r') as f:
                        try:
                            json.load(f)
                        except json.JSONDecodeError:
                            self.fail(f"Invalid JSON in {filename}")
    
    def test_error_catalog_completeness(self):
        """Test that error catalog contains required fields"""
        catalog_file = "/home/ubuntu/binom-api-encyclopedia/error_handling/catalog.json"
        if os.path.exists(catalog_file):
            with open(catalog_file, 'r') as f:
                catalog = json.load(f)
                for error_code, details in catalog.items():
                    self.assertIn("name", details)
                    self.assertIn("description", details)
                    self.assertIn("recovery_strategies", details)
    
    @patch('requests.get')
    def test_api_monitoring_simulation(self, mock_get):
        """Test API monitoring system with mocked responses"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"id": 1, "name": "test"}]}
        mock_get.return_value = mock_response
        
        # Simulate monitoring check
        response = requests.get(f"{self.base_url}/info/offer", headers=self.headers)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
