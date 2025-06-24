#!/usr/bin/env python3
"""
MIND System Watchdog
Überwacht die Systemgesundheit und sendet Alerts
"""

import os
import json
from datetime import datetime, timedelta

def check_system_health():
    """Prüft MIND-System Gesundheit"""
    
    issues = []
    
    # SKK Output prüfen
    skk_files = len([f for f in os.listdir("SKK_OUT") if f.endswith('.yaml')])
    if skk_files > 50:
        issues.append(f"SKK Queue overflow: {skk_files} files")
    
    # Semnet Registry prüfen
    try:
        with open("MIND/semnet/registry/last_rebuild.json", 'r') as f:
            last_rebuild = json.load(f)
        
        rebuild_time = datetime.fromisoformat(last_rebuild['timestamp'])
        if datetime.now() - rebuild_time > timedelta(days=2):
            issues.append("Semnet rebuild overdue")
            
    except FileNotFoundError:
        issues.append("Semnet registry missing")
    
    # Thoughts Activity prüfen
    thoughts_dir = "MIND/thoughts/daily"
    if os.path.exists(thoughts_dir):
        recent_thoughts = [f for f in os.listdir(thoughts_dir) 
                          if datetime.fromtimestamp(os.path.getctime(f)) > 
                          datetime.now() - timedelta(days=7)]
        
        if len(recent_thoughts) == 0:
            issues.append("No recent thoughts activity")
    
    if issues:
        print("⚠️ MIND System Issues:")
        for issue in issues:
            print(f"  • {issue}")
        
        # Hier könnte Slack/Discord Notification stehen
        
    else:
        print("✅ MIND System: All systems operational")

if __name__ == "__main__":
    check_system_health()
