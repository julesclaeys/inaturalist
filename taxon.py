import requests
import time
import json
from dotenv import load_dotenv
import os
import snowflake.connector as sc
import pandas as pd
from datetime import date, timedelta, datetime
import logging
from set_up_logs import *
import csv

def get_taxon():

#############################
# This function gathers information from snowflake to run additional API queries, 
# fetching data about species. It will check if the taxon_IDs
# are already in the Snowflake reference table to then fetch only required ones.
#############################

    logger = set_up_logger(get_taxon.__name__)
    
    try: 
        load_dotenv()
        private_key_file = os.getenv('PRIVATE_KEY_FILE')
        private_key_file_pwd = os.getenv("PRIVATE_KEY_PASSWORD")
    except Exception as e: 
        logger.error(f"Error loading env variables", exc_info=True)

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

    logger.info(f"Starting Get Taxon")
    print('Starting Get')
    logger.info(f"Connecting to Snowflake")

    try: 
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
    except Exception as e: 
        logger.error(f"Connection Failed", exc_info=True)

    logger.info("Connected to Snowflake")

    # Execute query and fetch data into Pandas
    cursor.execute(query)

    rows = cursor.fetchall()
    taxa_ids = [str(row[0]) for row in rows if row[0] is not None]

    logger.info(f"Found {len(taxa_ids)} taxa to fetch")

    #Inner function to run in batch 
    def chunk_list(lst, chunk_size):
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]

    #API Settings
    BASE_URL = "https://api.inaturalist.org/v1/taxa"
    BATCH_SIZE = 20
    SLEEP_BETWEEN_BATCHES = 10
    REQUEST_TIMEOUT = 30

    #Setting Output file Name
    ts = int(time.time())
    output_file = f"data/inaturalist_taxa_{ts}.json"

   #Loop through and get data
    try: 
        with open(output_file, "w", encoding="utf-8") as f:
            for batch_num, batch in enumerate(chunk_list(taxa_ids, BATCH_SIZE), start=1):
                logger.info(f"Processing batch {batch_num} ({len(batch)} taxa)")

                for taxon_id in batch:
                    try:
                        url = f"{BASE_URL}/{taxon_id}"
                        response = requests.get(url, timeout=REQUEST_TIMEOUT)
                        response.raise_for_status()

                        payload = response.json()
                        payload["snowflake_taxon_id"] = taxon_id

                        f.write(json.dumps(payload) + "\n")

                    except requests.exceptions.RequestException as e:
                        logger.error(f"Failed taxon_id {taxon_id}: {e}")

                logger.info(f"Sleeping {SLEEP_BETWEEN_BATCHES}s...")
                time.sleep(SLEEP_BETWEEN_BATCHES)

    except Exception as e: 
        logger.error(f"Failed to generate {output_file}")
    
    return print(f'Taxons Fetched')


# abs_path = os.path.abspath(output_file)

# cursor.execute(f"""
#     PUT file://{abs_path}
#     @NATURE_STG
#     AUTO_COMPRESS = TRUE
#     OVERWRITE = TRUE
# """)

# cursor.close()
# ctx.close()