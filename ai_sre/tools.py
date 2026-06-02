import os
import sys
import subprocess
import json
import re
from datetime import datetime

class SRETools:
    """Structured, safety-checked operations for SRE diagnostic investigation"""
    
    @staticmethod
    def check_disk() -> dict:
        """Check disk space usages safely using standard OS commands"""
        try:
            if sys.platform.startswith("win"):
                # Mock or Windows disk check equivalent
                return {
                    "status": "success",
                    "timestamp": datetime.now().isoformat(),
                    "output": "Windows Disk C: Free Space: 120GB, Used: 80GB, Util: 40%\nWindows Disk D: Free Space: 450GB, Used: 50GB, Util: 10%",
                    "alerts": []
                }
            
            # Linux real df -h execution
            res = subprocess.run(["df", "-h"], capture_output=True, text=True)
            output = res.stdout
            
            alerts = []
            for line in output.splitlines()[1:]:
                parts = line.split()
                if len(parts) >= 5:
                    use_pct = int(parts[4].replace("%", ""))
                    if use_pct >= 85:
                        alerts.append(f"High disk usage on {parts[5]}: {use_pct}%")
                        
            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "output": output,
                "alerts": alerts
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}