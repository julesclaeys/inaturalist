import requests
import time
import json
from datetime import date, timedelta
from dotenv import load_dotenv
import os
import snowflake.connector as sc
import pandas as pd

import csv


private_key_file = os.getenv("PRIVATE_KEY_FILE")
private_key_file_pwd = os.getenv("PRIVATE_KEY_PASSWORD")


conn_params = {
    'account': 'ad21223.eu-west-1',
    'user': 'SVC_SNOWFLAKE_PYTHON_JC',
    'authenticator': 'SNOWFLAKE_JWT',
    'private_key_file': private_key_file,
    'private_key_file_pwd': private_key_file_pwd,
    'warehouse': 'dataschool_wh',
    'database': 'til_data_engineering',
    'schema': 'jc_nature'
}

ctx = sc.connect(**conn_params)
cursor = ctx.cursor()

query = """
WITH UNPIVOT_CTE AS (
    SELECT DISTINCT *
    FROM S_TAXON
    UNPIVOT(
        IDs FOR Taxonomy_Level IN (
            Kingdom_ID,
            Phylum_ID,
            Class_ID,
            ORDER_ID,
            FAMILY_ID,
            GENUS_ID
        )
    )
),
PIVOT AS (
    SELECT DISTINCT IDs::VARCHAR AS IDs FROM UNPIVOT_CTE
    UNION ALL
    SELECT DISTINCT Taxon_ID::VARCHAR FROM S_TAXON
)
SELECT IDs
FROM PIVOT
WHERE IDs NOT IN (
    SELECT Taxon_ID FROM S_REFERENCE_TAXONOMY
)
"""

# Execute + fetch into Pandas
cursor.execute(query)

rows = cursor.fetchall()
taxa_ids = [str(row[0]) for row in rows if row[0] is not None]

print(f"Found {len(taxa_ids)} taxa to fetch")

# -------------------------
# Helper: batching
# -------------------------
def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

# -------------------------
# iNaturalist API settings
# -------------------------
BASE_URL = "https://api.inaturalist.org/v1/taxa"
BATCH_SIZE = 20
SLEEP_BETWEEN_BATCHES = 10
REQUEST_TIMEOUT = 30

ts = int(time.time())
output_file = f"inaturalist_taxa_{ts}.json"

# -------------------------
# Fetch taxa + write JSONL
# -------------------------
with open(output_file, "w", encoding="utf-8") as f:
    for batch_num, batch in enumerate(chunk_list(taxa_ids, BATCH_SIZE), start=1):
        print(f"Processing batch {batch_num} ({len(batch)} taxa)")

        for taxon_id in batch:
            try:
                url = f"{BASE_URL}/{taxon_id}"
                response = requests.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()

                payload = response.json()
                payload["snowflake_taxon_id"] = taxon_id

                f.write(json.dumps(payload) + "\n")

            except requests.exceptions.RequestException as e:
                print(f"Failed taxon_id {taxon_id}: {e}")

        print(f"Sleeping {SLEEP_BETWEEN_BATCHES}s...")
        time.sleep(SLEEP_BETWEEN_BATCHES)

# -------------------------
# Upload to Snowflake stage
# -------------------------
abs_path = os.path.abspath(output_file)

cursor.execute(f"""
    PUT file://{abs_path}
    @NATURE_STG
    AUTO_COMPRESS = TRUE
    OVERWRITE = TRUE
""")

cursor.close()
ctx.close()