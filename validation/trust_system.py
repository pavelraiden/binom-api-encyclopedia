"""
Trust System for AI Agents
Manages agent reputation and auto-approval permissions
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class SimpleTrustSystem:
    def __init__(self, trust_file_path: str = None):
        self.trust_file_path = trust_file_path or "/home/ubuntu/binom-api-encyclopedia/validation/agent_trust.json"
        self.trust_data = self._load_trust_data()
        
        # Trust thresholds
        self.auto_approve_threshold = 0.85
        self.trusted_threshold = 0.75
        self.new_agent_threshold = 0.5

    def _load_trust_data(self) -> Dict:
        """Load trust data from file or create new"""
        if os.path.exists(self.trust_file_path):
            try:
                with open(self.trust_file_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        return {
            "agents": {},
            "global_stats": {
                "total_contributions": 0,
                "successful_contributions": 0,
                "failed_contributions": 0
            }
        }

    def is_trusted(self, agent_id: str) -> bool:
        """Check if agent is trusted for auto-approval"""
        stats = self.get_agent_stats(agent_id)
        return stats["trust_score"] >= self.auto_approve_threshold

    def get_agent_stats(self, agent_id: str) -> Dict:
        """Get agent statistics"""
        if agent_id not in self.trust_data["agents"]:
            self.trust_data["agents"][agent_id] = {
                "successful_contributions": 0,
                "failed_contributions": 0,
                "total_contributions": 0,
                "trust_score": 0.5,  # Start with neutral trust
                "level": "new",
                "last_contribution": None,
                "created_at": datetime.now().isoformat()
            }
        
        return self.trust_data["agents"][agent_id]
