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

    @staticmethod
    def check_services(service_name: str = None) -> dict:
        """Diagnose systemd services, detecting failed loops or config issues"""
        try:
            if sys.platform.startswith("win"):
                return {
                    "status": "success",
                    "output": f"Mock Windows Service '{service_name or 'All'}' status: Active/Running (0 errors)",
                    "failed_units": []
                }
            
            if service_name:
                cmd = ["systemctl", "status", service_name]
            else:
                cmd = ["systemctl", "--failed"]
                
            res = subprocess.run(cmd, capture_output=True, text=True)
            output = res.stdout or res.stderr
            
            failed_units = []
            if not service_name:
                # Parse failed services list
                for line in output.splitlines():
                    if "●" in line or "failed" in line:
                        parts = line.split()
                        if len(parts) > 1:
                            failed_units.append(parts[1])
                            
            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "output": output,
                "failed_units": failed_units
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}