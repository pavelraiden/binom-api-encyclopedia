"""
Dependency Checker for API Endpoints
Validates endpoint dependencies and relationships
"""

import json
from typing import Dict, Tuple, List

class DependencyChecker:
    def __init__(self):
        self.dependencies = {
            # Critical dependencies between endpoints
            "campaign/create": {
                "required_endpoints": ["info/traffic_source"],
                "affects": ["campaign/update", "stats/campaign"]
            },
            "offer/create": {
                "required_endpoints": ["info/affiliate_network"],
                "affects": ["offer/update", "stats/offer"]
            },
            "landing/create": {
                "required_endpoints": [],
                "affects": ["landing/update", "stats/landing"]
            }
        }

    def check(self, endpoint: str) -> Tuple[bool, str]:
        """
        Check endpoint dependencies
        Returns: (dependencies_ok: bool, error_message: str)
        """
        try:
            # Normalize endpoint path
            endpoint = endpoint.lstrip('/')
            
            # Check if endpoint has dependencies
            if endpoint not in self.dependencies:
                return True, "No dependencies to check"
            
            required_endpoints = self.dependencies[endpoint].get("required_endpoints", [])
            
            # For now, assume all required endpoints are available
            # In a full implementation, we would test each required endpoint
            for required_ep in required_endpoints:
                # Simplified check - in reality we'd test the endpoint
                if not self._is_endpoint_available(required_ep):
                    return False, f"Required endpoint not available: {required_ep}"
            
            return True, "All dependencies satisfied"
            
        except Exception as e:
            return False, f"Dependency check error: {str(e)}"

    def _is_endpoint_available(self, endpoint: str) -> bool:
        """
        Check if an endpoint is available
        Simplified implementation - always returns True for now
        """
        # In a full implementation, this would test the actual endpoint
        return True

    def get_affected_endpoints(self, endpoint: str) -> List[str]:
        """Get list of endpoints affected by changes to this endpoint"""
        endpoint = endpoint.lstrip('/')
        if endpoint in self.dependencies:
            return self.dependencies[endpoint].get("affects", [])
        return []
