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