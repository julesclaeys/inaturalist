#Import Packages
import requests
import time
import json
from datetime import date, timedelta, datetime
import logging
import os
from dotenv import load_dotenv
import snowflake.connector as sc


#Import Modules
from get_park_ids import *
from get_places import *
from get_observations import *
from taxon import *
from push_to_stage import *
from set_up_logs import *

def remove_local_data(directory):

#############################
# This function cleans the data folder to not store data for too long.
# It uses snowflake to ensure we only delete files which have been uploaded to the stage correctly.
# Some formatting is required hence the changes within the for loop. 
#############################

#Setting up Logger

    logger = set_up_logger(remove_local_data.__name__)

#Starting connection to snowflake

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

    logger.info(f"Starting remove local data")
    print('Starting remove local data')
    logger.info(f"Connecting to Snowflake")

#Setting up Query to fetch staged files list

    try:
        ctx = sc.connect(**conn_params)
        cursor = ctx.cursor()


        query = """
                LIST @Nature_STG
                """
        cursor.execute(query)
        rows = cursor.fetchall()

    except Exception as e: 
        logger.error(f"Connection Failed", exc_info=True)

    logger.info("Connected to Snowflake, stage data fetched")

#Loop through and check which files are to be deleted.
    try: 
    
        for filename in os.listdir(directory):
            logger.info(f"Looping through files, {filename}")
            for row in rows: 
                placeholder = "nature_stg/" + filename + ".gz"
                if placeholder == row[0]:
                    logger.info(f"deleting {filename}")

                    os.remove(os.path.join(directory, filename))
    except Exception as e:
        logger.error(f"Error Deleting files")


    print('Files Deleted')   
