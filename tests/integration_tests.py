"""
Comprehensive Integration Tests for Binom API Encyclopedia
Tests real API endpoints to ensure documentation accuracy and API reliability.
"""

import os
import json
import time
import requests
import pytest
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class BinomAPITester:
    """Integration tester for Binom API with comprehensive validation"""
    
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
            "limit": 10,
            "offset": 0
        }
        
        # Test results storage
        self.test_results = []
        self.failed_endpoints = []
        self.performance_metrics = {}
        
    def validate_response(self, response: requests.Response, endpoint: str) -> Dict[str, Any]:
        """Validate API response and return detailed results"""
        start_time = time.time()
        
        result = {
            "endpoint": endpoint,
            "status_code": response.status_code,
            "response_time": time.time() - start_time,
            "success": False,
            "error": None,
            "data_quality": {},
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Check status code
            if response.status_code == 200:
                # Try to parse JSON
                data = response.json()
                result["success"] = True
                result["data_size"] = len(str(data))
                
                # Data quality checks
                if isinstance(data, list):
                    result["data_quality"]["record_count"] = len(data)
                    result["data_quality"]["is_array"] = True
                    
                    if data:  # Non-empty array
                        first_record = data[0]
                        result["data_quality"]["has_id"] = "id" in first_record
                        result["data_quality"]["has_name"] = "name" in first_record
                        result["data_quality"]["field_count"] = len(first_record.keys())
                        result["data_quality"]["fields"] = list(first_record.keys())
                
                elif isinstance(data, dict):
                    result["data_quality"]["is_object"] = True
                    result["data_quality"]["field_count"] = len(data.keys())
                    result["data_quality"]["fields"] = list(data.keys())
                
            else:
                result["error"] = f"HTTP {response.status_code}: {response.text[:200]}"
                
        except json.JSONDecodeError:
            result["error"] = "Invalid JSON response"
        except Exception as e:
            result["error"] = f"Validation error: {str(e)}"
            
        return result
    
    def test_endpoint(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Test a single endpoint with comprehensive validation"""
        test_params = {**self.default_params}
        if params:
            test_params.update(params)
            
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            start_time = time.time()
            response = requests.get(url, headers=self.headers, params=test_params, timeout=30)
            end_time = time.time()
            
            result = self.validate_response(response, endpoint)
            result["response_time"] = end_time - start_time
            
            # Store performance metrics
            self.performance_metrics[endpoint] = result["response_time"]
            
            return result
            
        except requests.exceptions.Timeout:
            return {
                "endpoint": endpoint,
                "success": False,
                "error": "Request timeout (30s)",
                "response_time": 30.0,
                "timestamp": datetime.now().isoformat()
            }
        except requests.exceptions.RequestException as e:
            return {
                "endpoint": endpoint,
                "success": False,
                "error": f"Request error: {str(e)}",
                "response_time": 0,
                "timestamp": datetime.now().isoformat()
            }
    
    def test_core_endpoints(self) -> List[Dict[str, Any]]:
        """Test core API endpoints that should always work"""
        core_endpoints = [
            "info/offer",
            "info/traffic_source", 
            "info/campaign",
            "info/landing",
            "info/rotation",
            "info/affiliate_network",
            "stats/offer",
            "stats/traffic_source",
            "stats/campaign"
        ]
        
        results = []
        print("🧪 Testing core endpoints...")
        
        for endpoint in core_endpoints:
            print(f"   Testing: {endpoint}")
            result = self.test_endpoint(endpoint)
            results.append(result)
            
            if not result["success"]:
                self.failed_endpoints.append(endpoint)
                print(f"   ❌ FAILED: {result.get('error', 'Unknown error')}")
            else:
                print(f"   ✅ SUCCESS: {result['response_time']:.2f}s")
        
        return results
    
    def test_authentication(self) -> Dict[str, Any]:
        """Test authentication with various scenarios"""
        print("🔐 Testing authentication...")
        
        # Test with correct auth
        correct_result = self.test_endpoint("info/offer", {"limit": 1})
        
        # Test with wrong auth format
        wrong_headers = {**self.headers}
        wrong_headers["Authorization"] = f"Bearer {self.api_key}"
        del wrong_headers["api-key"]  # Remove correct header
        
        try:
            response = requests.get(
                f"{self.base_url}/info/offer",
                headers=wrong_headers,
                params={"datePreset": "today", "timezone": "UTC", "limit": 1},
                timeout=10
            )
            wrong_auth_result = {
                "status_code": response.status_code,
                "expected_failure": response.status_code in [401, 403]
            }
        except Exception as e:
            wrong_auth_result = {"error": str(e), "expected_failure": True}
        
        return {
            "correct_auth": correct_result["success"],
            "wrong_auth_properly_rejected": wrong_auth_result.get("expected_failure", False),
            "auth_test_passed": correct_result["success"] and wrong_auth_result.get("expected_failure", False)
        }
    
    def test_required_parameters(self) -> Dict[str, Any]:
        """Test that required parameters are enforced"""
        print("📋 Testing required parameters...")
        
        # Test without datePreset
        no_date_result = self.test_endpoint("info/offer", {"timezone": "UTC", "limit": 1})
        
        # Test without timezone  
        no_timezone_result = self.test_endpoint("info/offer", {"datePreset": "today", "limit": 1})
        
        # Test with both required params
        both_params_result = self.test_endpoint("info/offer", {"datePreset": "today", "timezone": "UTC", "limit": 1})
        
        return {
            "no_date_preset_rejected": not no_date_result["success"],
            "no_timezone_rejected": not no_timezone_result["success"], 
            "both_params_accepted": both_params_result["success"],
            "parameter_validation_working": (
                not no_date_result["success"] and 
                not no_timezone_result["success"] and 
                both_params_result["success"]
            )
        }
    
    def test_data_consistency(self) -> Dict[str, Any]:
        """Test data consistency across related endpoints"""
        print("🔄 Testing data consistency...")
        
        # Get offers from info and stats endpoints
        info_offers = self.test_endpoint("info/offer", {"limit": 5})
        stats_offers = self.test_endpoint("stats/offer", {"limit": 5})
        
        consistency_result = {
            "info_endpoint_working": info_offers["success"],
            "stats_endpoint_working": stats_offers["success"],
            "both_endpoints_working": info_offers["success"] and stats_offers["success"]
        }
        
        # If both work, check for data consistency
        if consistency_result["both_endpoints_working"]:
            try:
                info_data = requests.get(
                    f"{self.base_url}/info/offer",
                    headers=self.headers,
                    params={**self.default_params, "limit": 5}
                ).json()
                
                stats_data = requests.get(
                    f"{self.base_url}/stats/offer", 
                    headers=self.headers,
                    params={**self.default_params, "limit": 5}
                ).json()
                
                consistency_result["info_record_count"] = len(info_data) if isinstance(info_data, list) else 0
                consistency_result["stats_record_count"] = len(stats_data) if isinstance(stats_data, list) else 0
                consistency_result["data_available"] = consistency_result["info_record_count"] > 0
                
            except Exception as e:
                consistency_result["consistency_check_error"] = str(e)
        
        return consistency_result
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        
        # Run all tests
        print("🚀 Starting comprehensive API integration tests...")
        print("=" * 60)
        
        # Core endpoint tests
        core_results = self.test_core_endpoints()
        
        # Authentication tests
        auth_results = self.test_authentication()
        
        # Parameter validation tests
        param_results = self.test_required_parameters()
        
        # Data consistency tests
        consistency_results = self.test_data_consistency()
        
        # Calculate overall metrics
        total_tests = len(core_results)
        successful_tests = sum(1 for r in core_results if r["success"])
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        
        avg_response_time = sum(self.performance_metrics.values()) / len(self.performance_metrics) if self.performance_metrics else 0
        
        # Generate report
        report = {
            "test_summary": {
                "timestamp": datetime.now().isoformat(),
                "total_endpoints_tested": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": total_tests - successful_tests,
                "success_rate_percent": round(success_rate, 2),
                "average_response_time_seconds": round(avg_response_time, 3),
                "failed_endpoints": self.failed_endpoints
            },
            "authentication_tests": auth_results,
            "parameter_validation_tests": param_results,
            "data_consistency_tests": consistency_results,
            "detailed_results": core_results,
            "performance_metrics": self.performance_metrics,
            "quality_score": self._calculate_quality_score(
                success_rate, avg_response_time, auth_results, param_results, consistency_results
            )
        }
        
        return report
    
    def _calculate_quality_score(self, success_rate: float, avg_response_time: float, 
                               auth_results: Dict, param_results: Dict, consistency_results: Dict) -> Dict[str, Any]:
        """Calculate overall API quality score"""
        
        # Base score from success rate (0-40 points)
        success_score = (success_rate / 100) * 40
        
        # Performance score (0-20 points) - better performance = higher score
        if avg_response_time <= 0.5:
            performance_score = 20
        elif avg_response_time <= 1.0:
            performance_score = 15
        elif avg_response_time <= 2.0:
            performance_score = 10
        else:
            performance_score = 5
        
        # Security score (0-20 points)
        security_score = 20 if auth_results.get("auth_test_passed", False) else 0
        
        # Validation score (0-10 points)
        validation_score = 10 if param_results.get("parameter_validation_working", False) else 0
        
        # Consistency score (0-10 points)
        consistency_score = 10 if consistency_results.get("both_endpoints_working", False) else 0
        
        total_score = success_score + performance_score + security_score + validation_score + consistency_score
        
        return {
            "total_score": round(total_score, 1),
            "max_score": 100,
            "grade": self._get_grade(total_score),
            "breakdown": {
                "success_rate": round(success_score, 1),
                "performance": round(performance_score, 1),
                "security": round(security_score, 1),
                "validation": round(validation_score, 1),
                "consistency": round(consistency_score, 1)
            }
        }
    
    def _get_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        else:
            return "F"

def run_integration_tests():
    """Main function to run all integration tests"""
    
    # Check if API key is available
    if not os.getenv('binomPublic'):
        print("❌ Error: binomPublic environment variable not found")
        print("Please set your Binom API key in the environment")
        return False
    
    # Initialize tester
    tester = BinomAPITester()
    
    # Generate comprehensive report
    report = tester.generate_report()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 INTEGRATION TEST RESULTS")
    print("=" * 60)
    
    summary = report["test_summary"]
    print(f"✅ Success Rate: {summary['success_rate_percent']}%")
    print(f"⏱️  Average Response Time: {summary['average_response_time_seconds']}s")
    print(f"🎯 Quality Score: {report['quality_score']['total_score']}/100 ({report['quality_score']['grade']})")
    
    if summary['failed_endpoints']:
        print(f"❌ Failed Endpoints: {', '.join(summary['failed_endpoints'])}")
    
    # Save detailed report
    report_filename = f"integration_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed report saved: {report_filename}")
    
    # Return success if quality score is acceptable
    return report['quality_score']['total_score'] >= 70

if __name__ == "__main__":
    success = run_integration_tests()
    exit(0 if success else 1)
