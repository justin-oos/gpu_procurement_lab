from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from utils.config import config
import os


def setup_database():
    client = bigquery.Client(project=config.PROJECT_ID)
    dataset_ref = bigquery.Dataset(f"{config.PROJECT_ID}.{config.DATASET_ID}")

    print(f"🧹 Teardown: Attempting to delete dataset {config.DATASET_ID}...")

    # 1. Force Delete the Dataset (Clean Slate)
    try:
        client.delete_dataset(
            dataset_ref,
            delete_contents=True,  # This wipes all tables inside
            not_found_ok=True,  # Don't crash if it doesn't exist yet
        )
        print(f"✅ Dataset {config.DATASET_ID} deleted (if it existed).")
    except Exception as e:
        print(f"⚠️ Warning during deletion: {e}")

    # 2. Create Fresh Dataset
    try:
        print(f"🛠️ Setup: Creating fresh dataset {config.DATASET_ID}...")
        dataset = client.create_dataset(dataset_ref, timeout=30)
        print(f"✅ Created dataset {config.DATASET_ID}.")
    except Exception as e:
        print(f"❌ Failed to create dataset: {e}")
        return

    # 3. Read and Execute SQL Files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sql_dir = os.path.join(base_dir, "sql")

    files = ["legacy_inv_main_v2.sql", "ref_catalog_dump.sql"]

    for filename in files:
        file_path = os.path.join(sql_dir, filename)
        print(f"Running {filename}...")

        with open(file_path, "r") as f:
            sql = f.read()

            # Split by semicolon to handle multiple statements
            statements = sql.split(";")

            for stmt in statements:
                if stmt.strip():
                    try:
                        # Dynamic injection of dataset ID
                        clean_stmt = stmt.replace(
                            "gpu_procurement_db", config.DATASET_ID
                        )

                        query_job = client.query(clean_stmt)
                        query_job.result()  # Wait for completion
                    except Exception as e:
                        print(f"❌ Error running statement in {filename}: {e}")

        print(f"✅ {filename} deployed successfully.")


if __name__ == "__main__":
    setup_database()
