"""
Enhanced API Tester with Quality Metrics
Tests comprehensive set of endpoints and measures quality
"""

import os
import requests
import json
import time
from typing import Dict, List, Tuple
from datetime import datetime

class EnhancedAPITester:
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
        
        # Comprehensive endpoint list for testing
        self.test_endpoints = [
            # Info endpoints
            "info/offer",
            "info/traffic_source", 
            "info/campaign",
            "info/landing",
            "info/rotation",
            "info/affiliate_network",
            
            # Stats endpoints
            "stats/offer",
            "stats/traffic_source",
            "stats/campaign", 
            "stats/landing",
            "stats/rotation",
            "stats/affiliate_network",
            
            # Utility endpoints
            "clicklog/columns",
            "conversions/columns",
            "country/list",
            "currency/list",
            "date_preset/list",
            
            # Additional endpoints
            "conversions/filters",
            "conversions/statuses/one",
            "conversions/statuses/two"
        ]

    def comprehensive_test(self) -> Dict:
        """Run comprehensive test of all endpoints"""
        print("🧪 Running Comprehensive API Test...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_endpoints": len(self.test_endpoints),
            "successful_endpoints": 0,
            "failed_endpoints": 0,
            "endpoint_results": {},
            "quality_metrics": {},
            "performance_metrics": {}
        }
        
        start_time = time.time()
        
        for endpoint in self.test_endpoints:
            print(f"  Testing {endpoint}...")
            
            endpoint_start = time.time()
            success, error, response_data = self._test_endpoint_detailed(endpoint)
            endpoint_duration = time.time() - endpoint_start
            
            results["endpoint_results"][endpoint] = {
                "success": success,
                "error": error,
                "response_time": endpoint_duration,
                "response_size": len(str(response_data)) if response_data else 0,
                "has_data": bool(response_data)
            }
            
            if success:
                results["successful_endpoints"] += 1
                print(f"    ✅ PASS ({endpoint_duration:.2f}s)")
            else:
                results["failed_endpoints"] += 1
                print(f"    ❌ FAIL: {error}")
        
        total_duration = time.time() - start_time
        
        # Calculate quality metrics
        results["quality_metrics"] = self._calculate_quality_metrics(results)
        results["performance_metrics"] = {
            "total_test_time": total_duration,
            "average_response_time": sum(r["response_time"] for r in results["endpoint_results"].values()) / len(results["endpoint_results"]),
            "endpoints_per_second": len(self.test_endpoints) / total_duration
        }
        
        return results

    def _test_endpoint_detailed(self, endpoint: str) -> Tuple[bool, str, any]:
        """Test endpoint with detailed response capture"""
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            params = self.default_params.copy() if 'stats' in endpoint else {}
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    return True, "Success", response_data
                except json.JSONDecodeError:
                    return True, "Success (non-JSON)", response.text
            else:
                return False, f"HTTP {response.status_code}: {response.text[:100]}", None
                
        except Exception as e:
            return False, f"Exception: {str(e)}", None

    def _calculate_quality_metrics(self, results: Dict) -> Dict:
        """Calculate quality metrics for 10/10 assessment"""
        total = results["total_endpoints"]
        successful = results["successful_endpoints"]
        
        # Core metrics
        success_rate = successful / total if total > 0 else 0
        coverage_score = min(1.0, total / 20)  # Target: 20+ endpoints
        
        # Response quality metrics
        endpoints_with_data = sum(1 for r in results["endpoint_results"].values() 
                                if r["success"] and r["has_data"])
        data_quality_score = endpoints_with_data / successful if successful > 0 else 0
        
        # Performance metrics
        avg_response_time = results.get("performance_metrics", {}).get("average_response_time", 0)
        performance_score = max(0, min(1.0, (5.0 - avg_response_time) / 5.0))  # Target: <5s
        
        # Overall quality score (weighted)
        overall_score = (
            success_rate * 0.4 +           # 40% - API reliability
            coverage_score * 0.3 +         # 30% - Endpoint coverage  
            data_quality_score * 0.2 +     # 20% - Data quality
            performance_score * 0.1        # 10% - Performance
        )
        
        return {
            "success_rate": success_rate,
            "coverage_score": coverage_score,
            "data_quality_score": data_quality_score,
            "performance_score": performance_score,
            "overall_quality_score": overall_score,
            "quality_rating": f"{overall_score * 10:.1f}/10",
            "endpoints_with_data": endpoints_with_data,
            "total_successful": successful
        }

    def generate_quality_report(self, results: Dict) -> str:
        """Generate human-readable quality report"""
        metrics = results["quality_metrics"]
        
        report = f"""
🎯 API Quality Assessment Report
================================

📊 Overall Quality: {metrics['quality_rating']}

📈 Detailed Metrics:
- Success Rate: {metrics['success_rate']:.1%} ({results['successful_endpoints']}/{results['total_endpoints']})
- Coverage Score: {metrics['coverage_score']:.1%} (Target: 20+ endpoints)
- Data Quality: {metrics['data_quality_score']:.1%} ({metrics['endpoints_with_data']} endpoints with data)
- Performance: {metrics['performance_score']:.1%} (Avg: {results['performance_metrics']['average_response_time']:.2f}s)

⚡ Performance Metrics:
- Total Test Time: {results['performance_metrics']['total_test_time']:.2f}s
- Average Response Time: {results['performance_metrics']['average_response_time']:.2f}s
- Endpoints/Second: {results['performance_metrics']['endpoints_per_second']:.1f}

🎯 10/10 Requirements:
- ✅ Success Rate: {'✅ PASS' if metrics['success_rate'] >= 0.9 else '❌ FAIL'} (≥90%)
- ✅ Coverage: {'✅ PASS' if metrics['coverage_score'] >= 1.0 else '❌ FAIL'} (≥20 endpoints)
- ✅ Data Quality: {'✅ PASS' if metrics['data_quality_score'] >= 0.8 else '❌ FAIL'} (≥80%)
- ✅ Performance: {'✅ PASS' if metrics['performance_score'] >= 0.6 else '❌ FAIL'} (<5s avg)

🏆 Overall Assessment: {'🎉 READY FOR 10/10' if metrics['overall_quality_score'] >= 0.9 else '🔧 NEEDS IMPROVEMENT'}
"""
        return report

if __name__ == "__main__":
    tester = EnhancedAPITester()
    results = tester.comprehensive_test()
    
    # Save results
    with open("/home/ubuntu/api_quality_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Generate and save report
    report = tester.generate_quality_report(results)
    with open("/home/ubuntu/api_quality_report.md", "w") as f:
        f.write(report)
    
    print("\n" + "="*60)
    print(report)
    print("="*60)
