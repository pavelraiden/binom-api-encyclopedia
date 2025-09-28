"""
Comprehensive Media Buying Workflows for Binom API
Real-world examples of how to use the API for media buying operations
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class Campaign:
    """Campaign data structure"""
    id: int
    name: str
    traffic_source: str
    cost: float
    status: str
    clicks: int = 0
    leads: int = 0
    revenue: float = 0.0
    roi: float = 0.0

class BinomMediaBuyingAPI:
    """Media buying operations using Binom API"""
    
    def __init__(self):
        self.api_key = os.getenv('binomPublic')
        self.base_url = "https://pierdun.com/public/api/v1"
        self.headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if not self.api_key:
            raise ValueError("Binom API key not found in environment variable 'binomPublic'")
    
    def make_request(self, endpoint: str, params: Dict = None, method: str = "GET") -> Dict:
        """Make API request with error handling"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        default_params = {
            "datePreset": "today",
            "timezone": "UTC"
        }
        
        if params:
            default_params.update(params)
        
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=default_params, timeout=30)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=default_params, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API request failed: {e}")
            return {}
    
    def get_campaigns(self, limit: int = 50) -> List[Campaign]:
        """Get all campaigns with performance data"""
        print("📊 Fetching campaigns...")
        
        # Get campaign info
        campaigns_data = self.make_request("info/campaign", {"limit": limit})
        
        # Get campaign stats
        stats_data = self.make_request("stats/campaign", {"limit": limit})
        
        campaigns = []
        
        for campaign_info in campaigns_data:
            # Find matching stats
            campaign_stats = next(
                (stats for stats in stats_data if stats.get("id") == campaign_info.get("id")),
                {}
            )
            
            # Safe type conversion for numeric fields
            def safe_float(value, default=0.0):
                try:
                    return float(value) if value is not None else default
                except (ValueError, TypeError):
                    return default
            
            def safe_int(value, default=0):
                try:
                    return int(value) if value is not None else default
                except (ValueError, TypeError):
                    return default
            
            campaign = Campaign(
                id=safe_int(campaign_info.get("id"), 0),
                name=str(campaign_info.get("name", "Unknown")),
                traffic_source=str(campaign_info.get("traffic_source", "Unknown")),
                cost=safe_float(campaign_info.get("current_cpc"), 0.0),
                status="active" if not campaign_info.get("is_deleted", False) else "deleted",
                clicks=safe_int(campaign_stats.get("clicks"), 0),
                leads=safe_int(campaign_stats.get("leads"), 0),
                revenue=safe_float(campaign_stats.get("revenue"), 0.0),
                roi=safe_float(campaign_stats.get("roi"), 0.0)
            )
            
            campaigns.append(campaign)
        
        print(f"✅ Found {len(campaigns)} campaigns")
        return campaigns
    
    def get_traffic_sources(self) -> List[Dict]:
        """Get all traffic sources with cost data"""
        print("🚦 Fetching traffic sources...")
        
        traffic_sources = self.make_request("info/traffic_source")
        
        print(f"✅ Found {len(traffic_sources)} traffic sources")
        return traffic_sources
    
    def get_offers(self) -> List[Dict]:
        """Get all offers with performance data"""
        print("🎯 Fetching offers...")
        
        offers = self.make_request("info/offer")
        
        print(f"✅ Found {len(offers)} offers")
        return offers

class MediaBuyingWorkflows:
    """Collection of media buying workflow examples"""
    
    def __init__(self):
        self.api = BinomMediaBuyingAPI()
    
    def workflow_1_daily_performance_check(self) -> Dict[str, Any]:
        """
        Workflow 1: Daily Performance Check
        Check campaign performance and identify issues
        """
        print("\n🔍 WORKFLOW 1: Daily Performance Check")
        print("=" * 50)
        
        # Get campaigns
        campaigns = self.api.get_campaigns()
        
        # Analyze performance
        analysis = {
            "total_campaigns": len(campaigns),
            "active_campaigns": len([c for c in campaigns if c.status == "active"]),
            "high_performers": [],
            "underperformers": [],
            "zero_traffic": [],
            "negative_roi": [],
            "recommendations": []
        }
        
        for campaign in campaigns:
            if campaign.status != "active":
                continue
                
            # High performers (ROI > 50%)
            if campaign.roi > 50:
                analysis["high_performers"].append({
                    "name": campaign.name,
                    "roi": campaign.roi,
                    "revenue": campaign.revenue,
                    "clicks": campaign.clicks
                })
            
            # Underperformers (ROI < 10%)
            elif campaign.roi < 10 and campaign.clicks > 100:
                analysis["underperformers"].append({
                    "name": campaign.name,
                    "roi": campaign.roi,
                    "clicks": campaign.clicks,
                    "cost": campaign.cost
                })
            
            # Zero traffic
            if campaign.clicks == 0:
                analysis["zero_traffic"].append({
                    "name": campaign.name,
                    "cost": campaign.cost
                })
            
            # Negative ROI
            if campaign.roi < 0:
                analysis["negative_roi"].append({
                    "name": campaign.name,
                    "roi": campaign.roi,
                    "revenue": campaign.revenue
                })
        
        # Generate recommendations
        if analysis["high_performers"]:
            analysis["recommendations"].append(f"🚀 Scale up {len(analysis['high_performers'])} high-performing campaigns")
        
        if analysis["underperformers"]:
            analysis["recommendations"].append(f"⚠️ Optimize or pause {len(analysis['underperformers'])} underperforming campaigns")
        
        if analysis["zero_traffic"]:
            analysis["recommendations"].append(f"🔍 Investigate {len(analysis['zero_traffic'])} campaigns with zero traffic")
        
        if analysis["negative_roi"]:
            analysis["recommendations"].append(f"🛑 Immediately review {len(analysis['negative_roi'])} campaigns with negative ROI")
        
        # Print summary
        print(f"📊 Total Campaigns: {analysis['total_campaigns']}")
        print(f"✅ Active: {analysis['active_campaigns']}")
        print(f"🚀 High Performers: {len(analysis['high_performers'])}")
        print(f"⚠️ Underperformers: {len(analysis['underperformers'])}")
        print(f"🔍 Zero Traffic: {len(analysis['zero_traffic'])}")
        print(f"🛑 Negative ROI: {len(analysis['negative_roi'])}")
        
        print("\n💡 Recommendations:")
        for rec in analysis["recommendations"]:
            print(f"   {rec}")
        
        return analysis
    
    def workflow_2_traffic_source_analysis(self) -> Dict[str, Any]:
        """
        Workflow 2: Traffic Source Analysis
        Analyze traffic source performance and costs
        """
        print("\n📈 WORKFLOW 2: Traffic Source Analysis")
        print("=" * 50)
        
        # Get traffic sources and stats
        traffic_sources = self.api.get_traffic_sources()
        traffic_stats = self.api.make_request("stats/traffic_source")
        
        analysis = {
            "total_sources": len(traffic_sources),
            "source_performance": [],
            "cost_analysis": {},
            "recommendations": []
        }
        
        # Safe type conversion helper functions
        def safe_float(value, default=0.0):
            try:
                return float(value) if value is not None else default
            except (ValueError, TypeError):
                return default
        
        def safe_int(value, default=0):
            try:
                return int(value) if value is not None else default
            except (ValueError, TypeError):
                return default
        
        # Analyze each traffic source
        for source in traffic_sources:
            source_id = source.get("id")
            source_name = str(source.get("name", "Unknown"))
            
            # Find matching stats
            stats = next(
                (s for s in traffic_stats if s.get("id") == source_id),
                {}
            )
            
            performance = {
                "name": source_name,
                "clicks": safe_int(stats.get("clicks"), 0),
                "leads": safe_int(stats.get("leads"), 0),
                "revenue": safe_float(stats.get("revenue"), 0.0),
                "cost": safe_float(stats.get("cost"), 0.0),
                "roi": safe_float(stats.get("roi"), 0.0),
                "cpc": safe_float(stats.get("cpc"), 0.0),
                "cr": safe_float(stats.get("cr"), 0.0)  # conversion rate
            }
            
            analysis["source_performance"].append(performance)
        
        # Sort by ROI
        analysis["source_performance"].sort(key=lambda x: x["roi"], reverse=True)
        
        # Cost analysis
        total_cost = sum(s["cost"] for s in analysis["source_performance"])
        total_revenue = sum(s["revenue"] for s in analysis["source_performance"])
        
        analysis["cost_analysis"] = {
            "total_cost": total_cost,
            "total_revenue": total_revenue,
            "overall_roi": ((total_revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0,
            "average_cpc": sum(s["cpc"] for s in analysis["source_performance"]) / len(analysis["source_performance"]) if analysis["source_performance"] else 0
        }
        
        # Generate recommendations
        top_performers = [s for s in analysis["source_performance"] if s["roi"] > 30]
        poor_performers = [s for s in analysis["source_performance"] if s["roi"] < 0 and s["cost"] > 100]
        
        if top_performers:
            analysis["recommendations"].append(f"🎯 Increase budget for {len(top_performers)} top-performing sources")
        
        if poor_performers:
            analysis["recommendations"].append(f"🔴 Review or pause {len(poor_performers)} poor-performing sources")
        
        # Print results
        print(f"📊 Total Traffic Sources: {analysis['total_sources']}")
        print(f"💰 Total Cost: ${analysis['cost_analysis']['total_cost']:.2f}")
        print(f"💵 Total Revenue: ${analysis['cost_analysis']['total_revenue']:.2f}")
        print(f"📈 Overall ROI: {analysis['cost_analysis']['overall_roi']:.1f}%")
        
        print(f"\n🏆 Top 3 Performing Sources:")
        for i, source in enumerate(analysis["source_performance"][:3], 1):
            print(f"   {i}. {source['name']}: {source['roi']:.1f}% ROI, ${source['revenue']:.2f} revenue")
        
        print("\n💡 Recommendations:")
        for rec in analysis["recommendations"]:
            print(f"   {rec}")
        
        return analysis
    
    def workflow_3_offer_optimization(self) -> Dict[str, Any]:
        """
        Workflow 3: Offer Optimization
        Analyze offer performance and suggest optimizations
        """
        print("\n🎯 WORKFLOW 3: Offer Optimization")
        print("=" * 50)
        
        # Get offers and stats
        offers = self.api.get_offers()
        offer_stats = self.api.make_request("stats/offer")
        
        analysis = {
            "total_offers": len(offers),
            "offer_performance": [],
            "optimization_opportunities": [],
            "recommendations": []
        }
        
        # Safe type conversion helper functions
        def safe_float(value, default=0.0):
            try:
                return float(value) if value is not None else default
            except (ValueError, TypeError):
                return default
        
        def safe_int(value, default=0):
            try:
                return int(value) if value is not None else default
            except (ValueError, TypeError):
                return default
        
        # Analyze each offer
        for offer in offers:
            offer_id = offer.get("id")
            offer_name = str(offer.get("name", "Unknown"))
            
            # Find matching stats
            stats = next(
                (s for s in offer_stats if s.get("id") == offer_id),
                {}
            )
            
            performance = {
                "name": offer_name,
                "country": str(offer.get("country", "Unknown")),
                "clicks": safe_int(stats.get("clicks"), 0),
                "leads": safe_int(stats.get("leads"), 0),
                "revenue": safe_float(stats.get("revenue"), 0.0),
                "cost": safe_float(stats.get("cost"), 0.0),
                "roi": safe_float(stats.get("roi"), 0.0),
                "cr": safe_float(stats.get("cr"), 0.0),
                "epc": safe_float(stats.get("epc"), 0.0)  # earnings per click
            }
            
            analysis["offer_performance"].append(performance)
            
            # Identify optimization opportunities
            if performance["clicks"] > 1000 and performance["cr"] < 1.0:
                analysis["optimization_opportunities"].append({
                    "offer": offer_name,
                    "issue": "Low conversion rate",
                    "suggestion": "Test different landing pages or traffic quality"
                })
            
            if performance["epc"] < 0.1 and performance["clicks"] > 500:
                analysis["optimization_opportunities"].append({
                    "offer": offer_name,
                    "issue": "Low EPC",
                    "suggestion": "Negotiate better payout or find alternative offers"
                })
        
        # Sort by EPC
        analysis["offer_performance"].sort(key=lambda x: x["epc"], reverse=True)
        
        # Generate recommendations
        high_volume_low_cr = [o for o in analysis["offer_performance"] if o["clicks"] > 1000 and o["cr"] < 1.0]
        profitable_offers = [o for o in analysis["offer_performance"] if o["roi"] > 20]
        
        if profitable_offers:
            analysis["recommendations"].append(f"💰 Scale traffic to {len(profitable_offers)} profitable offers")
        
        if high_volume_low_cr:
            analysis["recommendations"].append(f"🔧 Optimize conversion for {len(high_volume_low_cr)} high-traffic offers")
        
        # Print results
        print(f"📊 Total Offers: {analysis['total_offers']}")
        print(f"🔧 Optimization Opportunities: {len(analysis['optimization_opportunities'])}")
        
        print(f"\n🏆 Top 3 Offers by EPC:")
        for i, offer in enumerate(analysis["offer_performance"][:3], 1):
            print(f"   {i}. {offer['name']}: ${offer['epc']:.3f} EPC, {offer['cr']:.1f}% CR")
        
        print(f"\n🔧 Optimization Opportunities:")
        for opp in analysis["optimization_opportunities"][:5]:
            print(f"   • {opp['offer']}: {opp['issue']} - {opp['suggestion']}")
        
        print("\n💡 Recommendations:")
        for rec in analysis["recommendations"]:
            print(f"   {rec}")
        
        return analysis
    
    def workflow_4_budget_allocation(self) -> Dict[str, Any]:
        """
        Workflow 4: Smart Budget Allocation
        Suggest optimal budget distribution based on performance
        """
        print("\n💰 WORKFLOW 4: Smart Budget Allocation")
        print("=" * 50)
        
        # Get campaign performance data
        campaigns = self.api.get_campaigns()
        
        # Calculate current budget distribution
        total_cost = sum(c.cost * c.clicks for c in campaigns if c.status == "active")
        total_revenue = sum(c.revenue for c in campaigns if c.status == "active")
        
        analysis = {
            "current_budget": total_cost,
            "current_revenue": total_revenue,
            "current_roi": ((total_revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0,
            "budget_recommendations": [],
            "reallocation_plan": []
        }
        
        # Categorize campaigns by performance
        high_performers = [c for c in campaigns if c.status == "active" and c.roi > 30]
        medium_performers = [c for c in campaigns if c.status == "active" and 10 <= c.roi <= 30]
        low_performers = [c for c in campaigns if c.status == "active" and c.roi < 10]
        
        # Calculate recommended budget allocation
        total_recommended_budget = total_cost
        
        for campaign in high_performers:
            current_spend = campaign.cost * campaign.clicks
            recommended_increase = min(current_spend * 0.5, 1000)  # Increase by 50% or $1000 max
            
            analysis["reallocation_plan"].append({
                "campaign": campaign.name,
                "action": "increase",
                "current_budget": current_spend,
                "recommended_budget": current_spend + recommended_increase,
                "reason": f"High ROI ({campaign.roi:.1f}%)"
            })
        
        for campaign in low_performers:
            current_spend = campaign.cost * campaign.clicks
            if current_spend > 100:  # Only recommend reduction for campaigns spending >$100
                recommended_decrease = current_spend * 0.3  # Decrease by 30%
                
                analysis["reallocation_plan"].append({
                    "campaign": campaign.name,
                    "action": "decrease",
                    "current_budget": current_spend,
                    "recommended_budget": current_spend - recommended_decrease,
                    "reason": f"Low ROI ({campaign.roi:.1f}%)"
                })
        
        # Generate budget recommendations
        if high_performers:
            analysis["budget_recommendations"].append(f"📈 Increase budget for {len(high_performers)} high-performing campaigns")
        
        if low_performers:
            analysis["budget_recommendations"].append(f"📉 Reduce budget for {len(low_performers)} low-performing campaigns")
        
        if medium_performers:
            analysis["budget_recommendations"].append(f"🔄 Monitor and test {len(medium_performers)} medium-performing campaigns")
        
        # Print results
        print(f"💰 Current Total Budget: ${total_cost:.2f}")
        print(f"💵 Current Revenue: ${total_revenue:.2f}")
        print(f"📊 Current ROI: {analysis['current_roi']:.1f}%")
        
        print(f"\n📊 Campaign Distribution:")
        print(f"   🚀 High Performers (ROI >30%): {len(high_performers)}")
        print(f"   🔄 Medium Performers (ROI 10-30%): {len(medium_performers)}")
        print(f"   📉 Low Performers (ROI <10%): {len(low_performers)}")
        
        print(f"\n💡 Budget Reallocation Plan:")
        for plan in analysis["reallocation_plan"][:5]:
            action_emoji = "📈" if plan["action"] == "increase" else "📉"
            print(f"   {action_emoji} {plan['campaign']}: ${plan['current_budget']:.0f} → ${plan['recommended_budget']:.0f} ({plan['reason']})")
        
        print("\n🎯 Recommendations:")
        for rec in analysis["budget_recommendations"]:
            print(f"   {rec}")
        
        return analysis
    
    def run_all_workflows(self) -> Dict[str, Any]:
        """Run all media buying workflows and generate comprehensive report"""
        print("🚀 RUNNING ALL MEDIA BUYING WORKFLOWS")
        print("=" * 60)
        
        results = {}
        
        try:
            results["daily_performance"] = self.workflow_1_daily_performance_check()
            results["traffic_analysis"] = self.workflow_2_traffic_source_analysis()
            results["offer_optimization"] = self.workflow_3_offer_optimization()
            results["budget_allocation"] = self.workflow_4_budget_allocation()
            
            # Generate overall summary
            results["summary"] = {
                "timestamp": datetime.now().isoformat(),
                "workflows_completed": 4,
                "total_campaigns_analyzed": results["daily_performance"]["total_campaigns"],
                "total_traffic_sources": results["traffic_analysis"]["total_sources"],
                "total_offers": results["offer_optimization"]["total_offers"],
                "overall_roi": results["budget_allocation"]["current_roi"],
                "key_insights": [
                    f"Found {len(results['daily_performance']['high_performers'])} high-performing campaigns",
                    f"Identified {len(results['offer_optimization']['optimization_opportunities'])} optimization opportunities",
                    f"Budget reallocation could improve ROI by optimizing {len(results['budget_allocation']['reallocation_plan'])} campaigns"
                ]
            }
            
            print("\n" + "=" * 60)
            print("📊 WORKFLOW SUMMARY")
            print("=" * 60)
            print(f"✅ Workflows Completed: {results['summary']['workflows_completed']}")
            print(f"📊 Campaigns Analyzed: {results['summary']['total_campaigns_analyzed']}")
            print(f"🚦 Traffic Sources: {results['summary']['total_traffic_sources']}")
            print(f"🎯 Offers: {results['summary']['total_offers']}")
            print(f"💰 Overall ROI: {results['summary']['overall_roi']:.1f}%")
            
            print("\n🔍 Key Insights:")
            for insight in results["summary"]["key_insights"]:
                print(f"   • {insight}")
            
        except Exception as e:
            print(f"❌ Error running workflows: {e}")
            results["error"] = str(e)
        
        return results

def save_workflow_results(results: Dict[str, Any]):
    """Save workflow results to JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"workflow_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {filename}")
    return filename

if __name__ == "__main__":
    print("🎯 Binom API Media Buying Workflows")
    print("Real-world examples for media buyers")
    print("=" * 60)
    
    try:
        # Initialize workflows
        workflows = MediaBuyingWorkflows()
        
        # Run all workflows
        results = workflows.run_all_workflows()
        
        # Save results
        save_workflow_results(results)
        
        print("\n✅ All workflows completed successfully!")
        print("💡 Use these examples as templates for your own media buying automation")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure your Binom API key is set in the 'binomPublic' environment variable")
