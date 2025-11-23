from google.adk import Agent
from google.adk.tools import AgentTool

# Import the sub-agents
from agents.inventory.agent import inventory_agent
from agents.legal.agent import legal_agent
from agents.logistics.agent import logistics_agent

# Import the new File System Tools
from tools.file_system import FileSystemTools
from utils.gdrive_integration import ReportGenerator

# Initialize tools
fs_tools = FileSystemTools(root_dir="./workspace")
reporter = ReportGenerator()

COMMANDER_SYSTEM_PROMPT = """
You are the Incident Commander for a Critical Supply Chain Crisis.
You DO NOT execute tasks yourself. You DELEGATE to your sub-agents.

Your Goal: Find 500 H100 GPUs immediately.

SYSTEM OF RECORD:
You have access to a local file system. You MUST maintain a file named 'procurement_tracker.csv'.
Every time you find valid units or confirm a purchase, you MUST append a line to this file.

Format for CSV:
timestamp, source, quantity, status, notes

STRATEGY:
1. Initialize the 'procurement_tracker.csv' with a header if it doesn't exist (use write_file).
2. Ask Inventory Agent to search. If 300 units found -> Append to CSV (Source: Internal, Status: Pending Legal).
3. Ask Legal Agent to validate. If valid -> Update CSV (actually, append a new line confirming release).
4. Ask Logistics Agent for spot purchase. -> Append to CSV (Source: Spot Market, Status: Ordered).
5. Finally, read the CSV content to generate your Executive Report and upload it to GDrive.
"""

commander_agent = Agent(
    name="commander_agent",
    model="gemini-3-pro-preview",
    instruction=COMMANDER_SYSTEM_PROMPT,
    tools=[
        # Sub-Agents
        AgentTool(inventory_agent),
        AgentTool(legal_agent),
        AgentTool(logistics_agent),
        # File System Capabilities (The "Pivot")
        fs_tools.read_file,
        fs_tools.write_file,
        fs_tools.append_to_log,
        fs_tools.list_files,
        # Reporting
        reporter.upload_report,
    ],
)
