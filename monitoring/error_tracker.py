"""
Error Tracking and Monitoring System for Binom API Encyclopedia
Tracks API errors, documentation issues, and system health
"""

import os
import json
import time
import logging
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class ErrorEvent:
    """Represents an error event in the system"""
    timestamp: str
    error_type: str
    severity: str  # critical, high, medium, low
    component: str  # api, documentation, validation, etc.
    message: str
    details: Dict[str, Any]
    stack_trace: Optional[str] = None
    user_impact: str = "unknown"  # high, medium, low, none
    resolution_status: str = "open"  # open, investigating, resolved
    
class ErrorTracker:
    """Comprehensive error tracking and monitoring system"""
    
    def __init__(self, log_dir: str = "monitoring/logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Error storage
        self.errors_file = self.log_dir / "errors.json"
        self.metrics_file = self.log_dir / "metrics.json"
        
        # Initialize error storage
        self.errors = self.load_errors()
        self.metrics = self.load_metrics()
        
    def setup_logging(self):
        """Setup structured logging"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # File handler
        file_handler = logging.FileHandler(self.log_dir / "system.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(log_format))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(logging.Formatter(log_format))
        
        # Setup logger
        self.logger = logging.getLogger("BinomAPITracker")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def load_errors(self) -> List[Dict]:
        """Load existing errors from storage"""
        if self.errors_file.exists():
            try:
                with open(self.errors_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Failed to load errors: {e}")
        return []
    
    def load_metrics(self) -> Dict:
        """Load existing metrics from storage"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Failed to load metrics: {e}")
        
        return {
            "total_errors": 0,
            "errors_by_type": {},
            "errors_by_component": {},
            "errors_by_severity": {},
            "daily_error_count": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def save_errors(self):
        """Save errors to storage"""
        try:
            with open(self.errors_file, 'w') as f:
                json.dump(self.errors, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save errors: {e}")
    
    def save_metrics(self):
        """Save metrics to storage"""
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save metrics: {e}")
    
    def track_error(self, error_type: str, component: str, message: str, 
                   severity: str = "medium", details: Dict = None, 
                   user_impact: str = "unknown") -> str:
        """Track a new error event"""
        
        error_event = ErrorEvent(
            timestamp=datetime.now().isoformat(),
            error_type=error_type,
            severity=severity,
            component=component,
            message=message,
            details=details or {},
            stack_trace=traceback.format_exc() if traceback.format_exc().strip() != "NoneType: None" else None,
            user_impact=user_impact
        )
        
        # Add to errors list
        error_dict = asdict(error_event)
        self.errors.append(error_dict)
        
        # Update metrics
        self.update_metrics(error_event)
        
        # Log the error
        log_level = {
            "critical": logging.CRITICAL,
            "high": logging.ERROR,
            "medium": logging.WARNING,
            "low": logging.INFO
        }.get(severity, logging.WARNING)
        
        self.logger.log(log_level, f"[{component}] {error_type}: {message}")
        
        # Save to storage
        self.save_errors()
        self.save_metrics()
        
        return error_event.timestamp
    
    def update_metrics(self, error_event: ErrorEvent):
        """Update error metrics"""
        self.metrics["total_errors"] += 1
        
        # Update by type
        if error_event.error_type not in self.metrics["errors_by_type"]:
            self.metrics["errors_by_type"][error_event.error_type] = 0
        self.metrics["errors_by_type"][error_event.error_type] += 1
        
        # Update by component
        if error_event.component not in self.metrics["errors_by_component"]:
            self.metrics["errors_by_component"][error_event.component] = 0
        self.metrics["errors_by_component"][error_event.component] += 1
        
        # Update by severity
        if error_event.severity not in self.metrics["errors_by_severity"]:
            self.metrics["errors_by_severity"][error_event.severity] = 0
        self.metrics["errors_by_severity"][error_event.severity] += 1
        
        # Update daily count
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.metrics["daily_error_count"]:
            self.metrics["daily_error_count"][today] = 0
        self.metrics["daily_error_count"][today] += 1
        
        self.metrics["last_updated"] = datetime.now().isoformat()
    
    def track_api_error(self, endpoint: str, status_code: int, error_message: str, 
                       response_time: float = None):
        """Track API-specific errors"""
        severity = "critical" if status_code >= 500 else "high" if status_code >= 400 else "medium"
        user_impact = "high" if status_code >= 500 else "medium"
        
        details = {
            "endpoint": endpoint,
            "status_code": status_code,
            "response_time": response_time
        }
        
        self.track_error(
            error_type="api_error",
            component="api",
            message=f"API error on {endpoint}: {error_message}",
            severity=severity,
            details=details,
            user_impact=user_impact
        )
    
    def track_documentation_error(self, file_path: str, error_type: str, message: str):
        """Track documentation-specific errors"""
        details = {
            "file_path": file_path,
            "doc_error_type": error_type
        }
        
        self.track_error(
            error_type="documentation_error",
            component="documentation",
            message=f"Documentation error in {file_path}: {message}",
            severity="medium",
            details=details,
            user_impact="low"
        )
    
    def track_validation_error(self, validation_type: str, message: str, data: Dict = None):
        """Track validation errors"""
        details = {
            "validation_type": validation_type,
            "validation_data": data
        }
        
        self.track_error(
            error_type="validation_error",
            component="validation",
            message=f"Validation error ({validation_type}): {message}",
            severity="medium",
            details=details,
            user_impact="medium"
        )
    
    def get_error_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get error summary for the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_errors = [
            error for error in self.errors
            if datetime.fromisoformat(error["timestamp"]) > cutoff_date
        ]
        
        summary = {
            "period_days": days,
            "total_errors": len(recent_errors),
            "errors_by_severity": {},
            "errors_by_component": {},
            "errors_by_type": {},
            "critical_errors": [],
            "error_rate_trend": self.calculate_error_trend(days),
            "top_error_types": self.get_top_error_types(recent_errors),
            "recommendations": self.generate_recommendations(recent_errors)
        }
        
        # Count by categories
        for error in recent_errors:
            # By severity
            severity = error["severity"]
            summary["errors_by_severity"][severity] = summary["errors_by_severity"].get(severity, 0) + 1
            
            # By component
            component = error["component"]
            summary["errors_by_component"][component] = summary["errors_by_component"].get(component, 0) + 1
            
            # By type
            error_type = error["error_type"]
            summary["errors_by_type"][error_type] = summary["errors_by_type"].get(error_type, 0) + 1
            
            # Collect critical errors
            if severity == "critical":
                summary["critical_errors"].append({
                    "timestamp": error["timestamp"],
                    "message": error["message"],
                    "component": error["component"]
                })
        
        return summary
    
    def calculate_error_trend(self, days: int) -> str:
        """Calculate error rate trend"""
        if days < 2:
            return "insufficient_data"
        
        mid_point = days // 2
        cutoff_date = datetime.now() - timedelta(days=days)
        mid_date = datetime.now() - timedelta(days=mid_point)
        
        first_half_errors = len([
            error for error in self.errors
            if cutoff_date < datetime.fromisoformat(error["timestamp"]) <= mid_date
        ])
        
        second_half_errors = len([
            error for error in self.errors
            if datetime.fromisoformat(error["timestamp"]) > mid_date
        ])
        
        if first_half_errors == 0 and second_half_errors == 0:
            return "stable"
        elif first_half_errors == 0:
            return "increasing"
        elif second_half_errors == 0:
            return "decreasing"
        else:
            ratio = second_half_errors / first_half_errors
            if ratio > 1.2:
                return "increasing"
            elif ratio < 0.8:
                return "decreasing"
            else:
                return "stable"
    
    def get_top_error_types(self, errors: List[Dict], limit: int = 5) -> List[Dict]:
        """Get top error types by frequency"""
        error_counts = {}
        for error in errors:
            error_type = error["error_type"]
            if error_type not in error_counts:
                error_counts[error_type] = {"count": 0, "latest": error["timestamp"]}
            error_counts[error_type]["count"] += 1
            if error["timestamp"] > error_counts[error_type]["latest"]:
                error_counts[error_type]["latest"] = error["timestamp"]
        
        sorted_errors = sorted(error_counts.items(), key=lambda x: x[1]["count"], reverse=True)
        
        return [
            {
                "error_type": error_type,
                "count": data["count"],
                "latest_occurrence": data["latest"]
            }
            for error_type, data in sorted_errors[:limit]
        ]
    
    def generate_recommendations(self, errors: List[Dict]) -> List[str]:
        """Generate recommendations based on error patterns"""
        recommendations = []
        
        if not errors:
            recommendations.append("✅ No errors detected in the specified period")
            return recommendations
        
        # Check for high error rates
        if len(errors) > 10:
            recommendations.append("🚨 High error rate detected - investigate root causes")
        
        # Check for critical errors
        critical_errors = [e for e in errors if e["severity"] == "critical"]
        if critical_errors:
            recommendations.append(f"🔴 {len(critical_errors)} critical errors require immediate attention")
        
        # Check for API errors
        api_errors = [e for e in errors if e["component"] == "api"]
        if len(api_errors) > 5:
            recommendations.append("🌐 Multiple API errors - check API connectivity and authentication")
        
        # Check for documentation errors
        doc_errors = [e for e in errors if e["component"] == "documentation"]
        if doc_errors:
            recommendations.append("📚 Documentation errors detected - review and update documentation")
        
        # Check for validation errors
        validation_errors = [e for e in errors if e["component"] == "validation"]
        if validation_errors:
            recommendations.append("✅ Validation errors detected - review data quality and validation rules")
        
        if not recommendations:
            recommendations.append("💡 Error levels are within acceptable ranges")
        
        return recommendations
    
    def generate_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive system health report"""
        summary_7d = self.get_error_summary(7)
        summary_24h = self.get_error_summary(1)
        
        # Calculate health score (0-100)
        health_score = 100
        
        # Deduct points for errors
        health_score -= min(summary_24h["total_errors"] * 5, 30)  # Max 30 points for 24h errors
        health_score -= min(summary_7d["total_errors"] * 2, 40)   # Max 40 points for 7d errors
        
        # Deduct extra points for critical errors
        critical_24h = len(summary_24h["critical_errors"])
        health_score -= critical_24h * 10
        
        health_score = max(0, health_score)
        
        # Determine health status
        if health_score >= 90:
            health_status = "excellent"
        elif health_score >= 75:
            health_status = "good"
        elif health_score >= 60:
            health_status = "fair"
        elif health_score >= 40:
            health_status = "poor"
        else:
            health_status = "critical"
        
        return {
            "timestamp": datetime.now().isoformat(),
            "health_score": health_score,
            "health_status": health_status,
            "summary_24h": summary_24h,
            "summary_7d": summary_7d,
            "total_tracked_errors": len(self.errors),
            "monitoring_active": True,
            "recommendations": summary_7d["recommendations"]
        }

def create_monitoring_dashboard():
    """Create a simple HTML dashboard for monitoring"""
    tracker = ErrorTracker()
    health_report = tracker.generate_health_report()
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Binom API Encyclopedia - Health Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .health-score {{ font-size: 2em; font-weight: bold; text-align: center; }}
        .excellent {{ color: #28a745; }}
        .good {{ color: #17a2b8; }}
        .fair {{ color: #ffc107; }}
        .poor {{ color: #fd7e14; }}
        .critical {{ color: #dc3545; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; background: #f8f9fa; border-radius: 4px; }}
        .recommendations {{ background: #e7f3ff; border-left: 4px solid #007bff; }}
        .error-list {{ max-height: 300px; overflow-y: auto; }}
        .timestamp {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏥 Binom API Encyclopedia - Health Dashboard</h1>
        
        <div class="card">
            <h2>System Health</h2>
            <div class="health-score {health_report['health_status']}">
                {health_report['health_score']}/100 ({health_report['health_status'].title()})
            </div>
            <p class="timestamp">Last updated: {health_report['timestamp']}</p>
        </div>
        
        <div class="card">
            <h2>📊 24-Hour Summary</h2>
            <div class="metric">Total Errors: {health_report['summary_24h']['total_errors']}</div>
            <div class="metric">Critical Errors: {len(health_report['summary_24h']['critical_errors'])}</div>
            <div class="metric">Trend: {health_report['summary_24h']['error_rate_trend']}</div>
        </div>
        
        <div class="card">
            <h2>📈 7-Day Summary</h2>
            <div class="metric">Total Errors: {health_report['summary_7d']['total_errors']}</div>
            <div class="metric">Critical Errors: {len(health_report['summary_7d']['critical_errors'])}</div>
            <div class="metric">Trend: {health_report['summary_7d']['error_rate_trend']}</div>
        </div>
        
        <div class="card recommendations">
            <h2>💡 Recommendations</h2>
            <ul>
                {"".join(f"<li>{rec}</li>" for rec in health_report['recommendations'])}
            </ul>
        </div>
        
        <div class="card">
            <h2>🔍 Recent Critical Errors</h2>
            <div class="error-list">
                {"".join(f"<div><strong>{error['timestamp']}</strong>: {error['message']} ({error['component']})</div>" for error in health_report['summary_7d']['critical_errors'][:10]) or "<p>No critical errors in the last 7 days ✅</p>"}
            </div>
        </div>
        
        <div class="card">
            <h2>📋 Top Error Types (7 days)</h2>
            {"".join(f"<div class='metric'>{error['error_type']}: {error['count']} occurrences</div>" for error in health_report['summary_7d']['top_error_types'][:5]) or "<p>No errors to display ✅</p>"}
        </div>
    </div>
    
    <script>
        // Auto-refresh every 5 minutes
        setTimeout(() => location.reload(), 300000);
    </script>
</body>
</html>
"""
    
    dashboard_path = Path("monitoring/dashboard.html")
    dashboard_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(dashboard_path, 'w') as f:
        f.write(html_content)
    
    return str(dashboard_path)

if __name__ == "__main__":
    # Initialize error tracker
    tracker = ErrorTracker()
    
    # Example usage - track some sample errors for demonstration
    tracker.track_api_error("/info/offer", 500, "Internal server error", 2.5)
    tracker.track_documentation_error("docs/endpoints/offer.md", "missing_example", "No response example provided")
    tracker.track_validation_error("schema_validation", "Invalid JSON schema", {"field": "datePreset"})
    
    # Generate health report
    health_report = tracker.generate_health_report()
    
    print("🏥 System Health Report")
    print("=" * 50)
    print(f"Health Score: {health_report['health_score']}/100 ({health_report['health_status'].title()})")
    print(f"24h Errors: {health_report['summary_24h']['total_errors']}")
    print(f"7d Errors: {health_report['summary_7d']['total_errors']}")
    
    # Create monitoring dashboard
    dashboard_path = create_monitoring_dashboard()
    print(f"\n📊 Dashboard created: {dashboard_path}")
    print("💡 Open the dashboard in your browser to view real-time health metrics")
