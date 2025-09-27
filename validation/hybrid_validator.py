"""
Hybrid Validator for Binom API Encyclopedia Contributions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_tester import APITester
from trust_system import SimpleTrustSystem
from dependency_checker import DependencyChecker

class HybridValidator:
    def __init__(self):
        self.api_tester = APITester()
        self.trust_system = SimpleTrustSystem()
        self.dependency_checker = DependencyChecker()

    def validate_contribution(self, contribution, agent_id):
        """Validates a contribution from an AI agent."""
        validation_results = {
            "passed": False,
            "errors": []
        }

        # 1. Basic Syntax and Schema Validation (To be implemented)
        # ...

        # 2. API Endpoint Testing
        api_test_passed, api_error = self.api_tester.test_endpoint(contribution["endpoint"])
        if not api_test_passed:
            validation_results["errors"].append(f"API Test Failed: {api_error}")
            return validation_results

        # 3. Dependency Check
        dependencies_ok, dep_error = self.dependency_checker.check(contribution["endpoint"])
        if not dependencies_ok:
            validation_results["errors"].append(f"Dependency Check Failed: {dep_error}")
            return validation_results

        # 4. Agent Trust Score
        if not self.trust_system.is_trusted(agent_id):
            validation_results["errors"].append("Agent not trusted for auto-approval.")
            # Even if not trusted, the contribution can be valid but needs manual review
            # For now, we fail validation for non-trusted agents
            return validation_results

        validation_results["passed"] = True
        return validation_results
