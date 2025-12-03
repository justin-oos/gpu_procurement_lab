# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.cloud import bigquery
from typing import List, Dict, Any, Optional
from utils.config import config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseTools:
    def __init__(self):
        self.client = bigquery.Client(project=config.PROJECT_ID)

    def run_query(self, sql_query: str) -> List[Dict[str, Any]]:
        """Executes a standard SQL query."""

        # --- ADDED VISIBILITY ---
        print(f"\n[🛠️ DB TOOL] Executing SQL:\n    {sql_query}")
        # ------------------------

        try:
            query_job = self.client.query(sql_query)
            results = [dict(row) for row in query_job.result()]

            # --- ADDED VISIBILITY ---
            print(f"[✅ DB TOOL] Success. Rows returned: {len(results)}")
            # ------------------------

            return results
        except Exception as e:
            # --- ADDED VISIBILITY ---
            print(f"[❌ DB TOOL] Error: {str(e)}")
            # ------------------------
            logger.error(f"Query failed: {e}")
            return [{"error": str(e)}]

    def explore_schema(self, table_name: str) -> Dict[str, Any]:
        """Returns the schema and a sample of 5 rows."""

        # --- ADDED VISIBILITY ---
        print(f"\n[🛠️ DB TOOL] Exploring Schema for: {table_name}")
        # ------------------------

        clean_table = table_name.replace(";", "").replace("--", "")
        # Handle cases where LLM might pass the full ID or just the name
        if "." in clean_table:
            full_table_id = clean_table
        else:
            full_table_id = f"{config.PROJECT_ID}.{config.DATASET_ID}.{clean_table}"

        try:
            table = self.client.get_table(full_table_id)
            schema_info = [
                f"{field.name} ({field.field_type})" for field in table.schema
            ]

            sample_query = f"SELECT * FROM `{full_table_id}` LIMIT 5"
            sample_rows = self.run_query(sample_query)

            return {
                "table_name": clean_table,
                "fully_qualified_id": full_table_id,  # Helping the agent learn the right name
                "schema_fields": schema_info,
                "sample_rows": sample_rows,
                "note": f"IMPORTANT: When writing SQL, use this table name: `{full_table_id}`",
            }
        except Exception as e:
            print(f"[❌ DB TOOL] Schema Error: {str(e)}")
            return {"error": f"Could not explore schema: {str(e)}"}
