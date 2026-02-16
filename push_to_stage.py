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

def push_to_stage(directory):

#############################
# This function pushes all files in a directory into my snowflake Stage 
# This function will not work on your own stage! Just an example of what you could do. 
# If you want to set a similar one up, you will need a service account,
# A Key pair authentification method, and to give the service account read and write permissions
# on your stage
#############################

    logger = set_up_logger(push_to_stage.__name__)


    try: 
        load_dotenv()
        private_key_file = os.getenv('PRIVATE_KEY_FILE')
        private_key_file_pwd = os.getenv("PRIVATE_KEY_PASSWORD")
    except Exception as e: 
        logger.error(f"Error loading env variables", exc_info=True)


    try: 

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


        logger.info(f"Starting Push_to_Stage")
        logger.info(f"Connecting to Snowflake")



        ctx = sc.connect(**conn_params)
        cursor = ctx.cursor()

    except Exception as e: 
        logger.error(f"Error connecting to Sonwflake")
    
    logger.info(f"Connection Successful, pushing to Stage")


    try: 
        cursor.execute(f"""
        PUT file://{directory}/*
        @NATURE_STG
        AUTO_COMPRESS = TRUE
        OVERWRITE = TRUE
        """)
        cursor.close()
        ctx.close()
    
    except Exception:
        logger.error("Failed to Push to Stage", exc_info=True)
        raise

    return print(f'Pushed {directory} to stage')

