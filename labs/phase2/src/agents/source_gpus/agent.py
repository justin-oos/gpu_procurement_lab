# Copyright 2025 Google LLC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import logging
from dotenv import load_dotenv
import google.auth.transport.requests
import google.oauth2.id_token
from google.adk.agents import Agent, SequentialAgent, ParallelAgent
from google.adk.tools.tool_context import ToolContext

from tools.file_system import FileSystemTools
from utils.config import config
from agents.inventory.agent import inventory_agent
from agents.legal.agent import legal_agent
from agents.logistics.agent import logistics_agent


load_dotenv()


fs_tools = FileSystemTools(root_dir="./workspace")


source_gpus_parallel_agent = ParallelAgent(
        name="source_gpus_parallel_agent",
        description=(
            "Runs multiple source GPU sub-agents in parallel."
        ),
        sub_agents=[inventory_agent, legal_agent, logistics_agent],
    )

def source_gpus_merge_results(tool_context: ToolContext):
    """Return the aggregate sub-agent information."""
    return "Success"

source_gpus_merge_agent = Agent(
    name="source_gpus_merge_agent",
    model=config.MODEL_NAME,
    instruction="""
Your Goal: Append uncovered finding from DATA INPUTS into a CSV 'procurement_tracker.csv'.

SYSTEM OF RECORD:
You have access to a local file system. You MUST maintain a file named 'procurement_tracker.csv'.
You MUST append the data as lines to this file.

Format for CSV:
timestamp, source, quantity, status, notes

STRATEGY (FOLLOW THIS EXACTLY):
1. Initialize the 'procurement_tracker.csv' with a header if it doesn't exist (use write_file).
2. Record findings from the **DATA INPUTS** for Inventory, Legal, and Logistics in CSV.

CRITICAL TERMINATION RULES:
- Record all findings in CSV.
- If an agent cannot provide specific information, accept their response and move on.
- Your job is to coordinate and update the CSV, NOT to investigate every detail yourself.

DATA INPUTS:

    *   **Inventory Agent Results:**
        {inventory_agent_result}

    *   **Legal Agent Results:**
        {legal_agent_result}

    *   **Logistics Agent Results:**
        {logistics_agent_result}
""",
    tools=[
        # File System Capabilities (The "Pivot")
        fs_tools.read_file,
        fs_tools.write_file,
        fs_tools.append_to_log,
        fs_tools.list_files,
    ]
)

source_gpus_agent = SequentialAgent(
    name="source_gpus_agent",
    description=(
        "Runs multiple source GPU sub-agents in sequence."
    ),
    sub_agents=[source_gpus_parallel_agent, source_gpus_merge_agent],
)
