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

    @staticmethod
    def check_network(port: int = None) -> dict:
        """Inspect port mappings and active socket servers using ss / netstat"""
        try:
            if sys.platform.startswith("win"):
                return {
                    "status": "success",
                    "output": f"Mock networking. Active ports on 127.0.0.1: [80, 443, 3000, 5432, 8501]. Requested Port {port or 'None'} check: OK",
                    "is_blocked": False
                }
                
            # Use ss or netstat
            cmd = ["ss", "-tulpn"]
            res = subprocess.run(cmd, capture_output=True, text=True)
            output = res.stdout or res.stderr
            
            is_blocked = False
            if port:
                port_pattern = f":{port} "
                is_blocked = port_pattern in output
                
            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "output": output,
                "port_checked": port,
                "is_blocked": is_blocked
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    @staticmethod
    def check_processes(cpu_threshold: float = 80.0) -> dict:
        """Identify resource-hogging system processes"""
        try:
            if sys.platform.startswith("win"):
                return {
                    "status": "success",
                    "output": "Mock Process: svchost.exe (CPU: 2%), streamlit.exe (CPU: 5%)",
                    "hogs": []
                }
            
            cmd = ["ps", "aux", "--sort=-%cpu"]
            res = subprocess.run(cmd, capture_output=True, text=True)
            output = res.stdout
            
            hogs = []
            lines = output.splitlines()
            for line in lines[1:6]:  # Top 5 CPU processes
                parts = line.split()
                if len(parts) >= 11:
                    cpu_val = float(parts[2])
                    if cpu_val >= cpu_threshold:
                        hogs.append({"pid": parts[1], "user": parts[0], "cpu": cpu_val, "comm": " ".join(parts[10:])})
                        
            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "output": "\n".join(lines[:10]),
                "hogs": hogs
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    @staticmethod
    def check_logs(search_query: str = "error", lines_count: int = 50) -> dict:
        """Search through system journal logs for specific error occurrences"""
        try:
            if sys.platform.startswith("win"):
                return {
                    "status": "success",
                    "output": f"Mock Log Search for '{search_query}':\n[2026-06-02 08:30:11] ERROR: connection pool exhausted\n[2026-06-02 08:31:02] WARN: slow query detected",
                    "matches_found": 2
                }
                
            cmd = ["journalctl", f"-n", str(lines_count)]
            res = subprocess.run(cmd, capture_output=True, text=True)
            output = res.stdout or res.stderr
            
            matches = []
            for line in output.splitlines():
                if re.search(search_query, line, re.IGNORECASE):
                    matches.append(line)
                    
            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "output": "\n".join(matches[:15]),
                "matches_found": len(matches)
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}