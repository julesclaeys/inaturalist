import requests
import time
import json
from dotenv import load_dotenv
import os
import snowflake.connector as sc
import pandas as pd
from datetime import date, timedelta, datetime
import logging

import csv

def push_to_stage(directory):

    # Set up Try block for Logging

    # Set Up Logging
    logger = logging.getLogger("push_to_stage")
    logger.setLevel(logging.DEBUG)  # Capture everything, handlers decide what to save

    #Set Up Logger Format
    log_format = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    ) # Configure logging

    #Set up Log file Name
    ts = int(time.time())
    output_file = f"push_to_stage_log_{ts}.log"

    #Set up Different Paths for different Levels of Logging (Info)
    info_dir = 'logs/push_to_stage/INFO'
    os.makedirs(info_dir, exist_ok=True)
    info_log = logging.FileHandler("logs/push_to_stage/INFO/" + output_file, encoding="utf-8")
    logger.addHandler(info_log)
    info_log.setLevel(logging.INFO)
    info_log.setFormatter(log_format)
    info_log.addFilter(lambda record: record.levelno == logging.INFO)

    #Set up Different Paths for different Levels of Logging (Warning)
    warning_dir = 'logs/push_to_stage/WARNING'
    os.makedirs(warning_dir, exist_ok=True)
    Warning_log = logging.FileHandler("logs/push_to_stage/WARNING/" + output_file, encoding="utf-8")
    logger.addHandler(Warning_log)
    Warning_log.setLevel(logging.WARNING)
    Warning_log.setFormatter(log_format)
    Warning_log.addFilter(lambda record: record.levelno == logging.WARNING)

    #Set up Different Paths for different Levels of Logging (ERROR)
    error_dir = 'logs/push_to_stage/ERROR'
    os.makedirs(error_dir, exist_ok=True)
    error_log = logging.FileHandler("logs/push_to_stage/ERROR/" + output_file, encoding="utf-8")
    logger.addHandler(error_log)
    error_log.setLevel(logging.ERROR)
    error_log.setFormatter(log_format)
    error_log.addFilter(lambda record: record.levelno == logging.ERROR)

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
        PUT file://{directory}
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

