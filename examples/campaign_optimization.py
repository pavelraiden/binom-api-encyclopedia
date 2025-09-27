#!/usr/bin/env python3
"""
Real-world example: Complete Campaign Optimization Workflow
This example demonstrates a full campaign optimization cycle using the Binom API.
"""

import requests
import json
import time
from datetime import datetime, timedelta

class CampaignOptimizer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://pierdun.com/public/api/v1"
        self.headers = {"api-key": api_key}
    
    def get_campaign_performance(self, campaign_id, days=7):
        """Get campaign performance data for the last N days"""
        endpoint = "/stats/campaign"
        params = {
            "datePreset": f"last_{days}_days",
            "timezone": "UTC",
            "campaignId": campaign_id
        }
        
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting campaign stats: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            return None
    
    def analyze_landing_performance(self, campaign_data):
        """Analyze which landings are performing best"""
        if not campaign_data or 'data' not in campaign_data:
            return []
        
        landing_stats = {}
        
        for record in campaign_data['data']:
            landing_id = record.get('landingId')
            if not landing_id:
                continue
            
            if landing_id not in landing_stats:
                landing_stats[landing_id] = {
                    'clicks': 0,
                    'conversions': 0,
                    'revenue': 0,
                    'cost': 0
                }
            
            stats = landing_stats[landing_id]
            stats['clicks'] += record.get('clicks', 0)
            stats['conversions'] += record.get('conversions', 0)
            stats['revenue'] += record.get('revenue', 0)
            stats['cost'] += record.get('cost', 0)
        
        # Calculate ROI and conversion rates
        for landing_id, stats in landing_stats.items():
            if stats['clicks'] > 0:
                stats['conversion_rate'] = (stats['conversions'] / stats['clicks']) * 100
            else:
                stats['conversion_rate'] = 0
            
            if stats['cost'] > 0:
                stats['roi'] = ((stats['revenue'] - stats['cost']) / stats['cost']) * 100
            else:
                stats['roi'] = 0
        
        # Sort by ROI
        sorted_landings = sorted(
            landing_stats.items(),
            key=lambda x: x[1]['roi'],
            reverse=True
        )
        
        return sorted_landings
    
    def optimize_campaign_weights(self, campaign_id):
        """Optimize campaign landing weights based on performance"""
        print(f"Starting optimization for campaign {campaign_id}")
        
        # Step 1: Get current performance data
        performance_data = self.get_campaign_performance(campaign_id)
        if not performance_data:
            print("Failed to get performance data")
            return False
        
        # Step 2: Analyze landing performance
        landing_analysis = self.analyze_landing_performance(performance_data)
        if not landing_analysis:
            print("No landing data to analyze")
            return False
        
        print("Landing Performance Analysis:")
        print("-" * 50)
        for landing_id, stats in landing_analysis[:5]:  # Top 5
            print(f"Landing {landing_id}:")
            print(f"  ROI: {stats['roi']:.2f}%")
            print(f"  Conversion Rate: {stats['conversion_rate']:.2f}%")
            print(f"  Clicks: {stats['clicks']}")
            print(f"  Revenue: ${stats['revenue']:.2f}")
            print()
        
        # Step 3: Calculate new weights (this would normally update via API)
        total_roi = sum(stats['roi'] for _, stats in landing_analysis if stats['roi'] > 0)
        
        if total_roi > 0:
            print("Recommended Weight Distribution:")
            print("-" * 30)
            for landing_id, stats in landing_analysis:
                if stats['roi'] > 0:
                    weight = (stats['roi'] / total_roi) * 100
                    print(f"Landing {landing_id}: {weight:.1f}%")
        
        return True
    
    def run_full_optimization(self, campaign_id):
        """Run a complete optimization cycle"""
        print(f"🚀 Starting full optimization for campaign {campaign_id}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 60)
        
        success = self.optimize_campaign_weights(campaign_id)
        
        if success:
            print("✅ Optimization completed successfully")
        else:
            print("❌ Optimization failed")
        
        return success

# Example usage
if __name__ == "__main__":
    import os
    
    # Get API key from environment
    api_key = os.getenv("binomPublic")
    if not api_key:
        print("Please set the binomPublic environment variable")
        exit(1)
    
    # Initialize optimizer
    optimizer = CampaignOptimizer(api_key)
    
    # Run optimization for campaign ID 51 (example)
    campaign_id = 51
    optimizer.run_full_optimization(campaign_id)
