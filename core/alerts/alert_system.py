from typing import List, Dict, Any, Callable
import json
from datetime import datetime
import asyncio
from collections import defaultdict

class AlertSystem:
    def __init__(self):
        """
        Initialize the alert system
        """
        self.alert_rules = []
        self.alert_handlers = []
        self.alert_history = defaultdict(list)
        
    def add_rule(self, rule: Dict[str, Any]):
        """
        Add a new alert rule
        
        Args:
            rule: Dictionary containing rule configuration
                {
                    "name": str,
                    "type": str,
                    "conditions": List[Dict],
                    "severity": str,
                    "cooldown": int (minutes)
                }
        """
        self.alert_rules.append(rule)
        
    def add_alert_handler(self, handler: Callable):
        """
        Add a new alert handler function
        
        Args:
            handler: Callable that processes alerts
        """
        self.alert_handlers.append(handler)
        
    async def process_content(self, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process content and generate alerts based on rules
        
        Args:
            content: Dictionary containing analyzed content
            
        Returns:
            List of generated alerts
        """
        generated_alerts = []
        
        for rule in self.alert_rules:
            if await self._check_rule_conditions(rule, content):
                alert = self._create_alert(rule, content)
                
                # Check cooldown
                if self._check_cooldown(rule, alert):
                    generated_alerts.append(alert)
                    self.alert_history[rule["name"]].append(alert)
                    
                    # Notify handlers
                    await self._notify_handlers(alert)
        
        return generated_alerts
    
    async def _check_rule_conditions(self, rule: Dict[str, Any], 
                                   content: Dict[str, Any]) -> bool:
        """
        Check if content matches rule conditions
        """
        for condition in rule["conditions"]:
            condition_type = condition["type"]
            
            if condition_type == "keyword":
                if not any(kw in content.get("keywords", []) 
                          for kw in condition["keywords"]):
                    return False
                    
            elif condition_type == "pattern":
                if not any(p["pattern_name"] == condition["pattern_name"] 
                          for p in content.get("pattern_matches", [])):
                    return False
                    
            elif condition_type == "sentiment":
                sentiment = content.get("sentiment", {}).get("label")
                if sentiment != condition["sentiment"]:
                    return False
        
        return True
    
    def _create_alert(self, rule: Dict[str, Any], 
                     content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an alert object from a triggered rule
        """
        return {
            "rule_name": rule["name"],
            "severity": rule["severity"],
            "timestamp": datetime.utcnow().isoformat(),
            "content_summary": content.get("summary", ""),
            "matched_conditions": rule["conditions"]
        }
    
    def _check_cooldown(self, rule: Dict[str, Any], 
                       alert: Dict[str, Any]) -> bool:
        """
        Check if enough time has passed since the last alert of this type
        """
        if not self.alert_history[rule["name"]]:
            return True
            
        last_alert = self.alert_history[rule["name"]][-1]
        last_time = datetime.fromisoformat(last_alert["timestamp"])
        current_time = datetime.fromisoformat(alert["timestamp"])
        
        cooldown_minutes = rule.get("cooldown", 0)
        time_diff = (current_time - last_time).total_seconds() / 60
        
        return time_diff >= cooldown_minutes
    
    async def _notify_handlers(self, alert: Dict[str, Any]):
        """
        Notify all registered handlers about the alert
        """
        for handler in self.alert_handlers:
            try:
                await handler(alert)
            except Exception as e:
                print(f"Error in alert handler: {str(e)}")
