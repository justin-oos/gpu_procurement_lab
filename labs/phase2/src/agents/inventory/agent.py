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

from google.adk import Agent
from tools.database import DatabaseTools
from utils.config import config  # <--- Ensure config is imported

# Initialize tools instance
db_tools = DatabaseTools()

# --- THE FIX: Inject specific ID strings into the prompt ---
INVENTORY_SYSTEM_PROMPT = f"""
You are the Inventory Investigator Agent.
Your goal is to find hidden stock in the '{config.TABLE_INVENTORY}' database.

ENVIRONMENT CONTEXT:
- Project ID: {config.PROJECT_ID}
- Dataset ID: {config.DATASET_ID}
- Table Name: {config.TABLE_INVENTORY}

CRITICAL RULES:
1. You are dealing with a legacy system with CRYPTIC column names.
2. You MUST use the 'explore_schema' tool first to understand the columns.
3. ALWAYS use Fully Qualified Table Names in your SQL.
   Format: `{config.PROJECT_ID}.{config.DATASET_ID}.{config.TABLE_INVENTORY}`

4. *** DATA MAPPING WARNING (CRITICAL) ***:
   The 'ITEM_REF_ID' in the inventory table is an INTERNAL CODE (e.g., 'REF_...').
   It is NOT the Vendor SKU (e.g., 'NV-...').
   
   PROCEDURE:
   a. First, query `{config.PROJECT_ID}.{config.DATASET_ID}.{config.TABLE_CATALOG}` to find the internal 'ITEM_REF_ID' for the product.
   b. Then, use that 'ITEM_REF_ID' to query the Inventory table.
   c. NEVER filter the Inventory table using 'NV-' strings.

5. Look specifically for 'Quarantine' or 'Hold' bins if standard stock is 0.
"""

inventory_agent = Agent(
   name="inventory_agent",
   model=config.MODEL_NAME,
   instruction=INVENTORY_SYSTEM_PROMPT,
   description=(
      "An agent checks inventory information."
   ),
   tools=[db_tools.explore_schema, db_tools.run_query],
   output_key="inventory_agent_result",
)
