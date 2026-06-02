import json
from ai_sre.config import Config
from ai_sre.tools import SRETools

# Define tool schemas for agent interaction
TOOL_SCHEMAS = [
    {
        "name": "check_disk",
        "description": "Inspect filesystem storage space, free partitions, and locate disk alerts."
    },
    {
        "name": "check_services",
        "description": "Check systemd service status or retrieve details of active/failed units.",
        "parameters": {
            "type": "object",
            "properties": {
                "service_name": {"type": "string", "description": "The name of the service to check"}
            }
        }
    },
    {
        "name": "check_network",
        "description": "View port listeners or check if a specific TCP port is blocked/open.",
        "parameters": {
            "type": "object",
            "properties": {
                "port": {"type": "integer", "description": "Specific port number to check"}
            }
        }
    },
    {
        "name": "check_processes",
        "description": "Inspect top resource-consuming OS processes.",
        "parameters": {
            "type": "object",
            "properties": {
                "cpu_threshold": {"type": "number", "description": "Min CPU % threshold to trigger warning"}
            }
        }
    },
    {
        "name": "check_logs",
        "description": "Retrieve and filter recent system journalctl logs for diagnostics.",
        "parameters": {
            "type": "object",
            "properties": {
                "search_query": {"type": "string", "description": "Search text filters like 'error', 'failed'"},
                "lines_count": {"type": "integer", "description": "Number of log lines to retrieve"}
            }
        }
    }
]

class SREAgent:
    """LLM Reasoning SRE Agent that acts as a secure diagnostics troubleshooter"""
    
    def __init__(self, mode: str = "mock"):
        self.mode = mode
        self.history = []
        
    def execute_tool(self, name: str, params: dict = None) -> dict:
        """Execute the structured tools based on agent decisions"""
        params = params or {}
        if name == "check_disk":
            return SRETools.check_disk()
        elif name == "check_services":
            return SRETools.check_services(params.get("service_name"))
        elif name == "check_network":
            return SRETools.check_network(params.get("port"))
        elif name == "check_processes":
            return SRETools.check_processes(params.get("cpu_threshold", 80.0))
        elif name == "check_logs":
            return SRETools.check_logs(params.get("search_query", "error"), params.get("lines_count", 50))
        return {"status": "error", "error": f"Tool '{name}' not found"}

    def system_prompt(self) -> str:
        return (
            "You are an expert Linux SRE & DevOps Incident Response Troubleshooting Agent. "
            "Your objective is to diagnose system issues, explain the root cause, and provide a safe bash fix script.\n"
            "You have access to safe, structured diagnostic tools (check_disk, check_services, check_network, check_processes, check_logs).\n"
            "Analyze issues step-by-step. Do not make up command executions. Use the tools provided."
        )