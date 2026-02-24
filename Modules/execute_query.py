import requests
import time
import json
from dotenv import load_dotenv
import os
import snowflake.connector as sc
from Modules.set_up_logs import *

def execute_query(stage, schema, database, account, password, private_key, warehouse, user, query):

#############################
# This function executes any query in a snowflake schema
#############################

    logger = set_up_logger(execute_query.__name__)
    
    try: 
        private_key_file = private_key
        private_key_file_pwd = password
        account = account
        user = user
        warehouse = warehouse
        database = database
        schema = schema
    except Exception as e: 
        logger.error(f"Error loading env variables", exc_info=True)

    conn_params = {
        'account': account,
        'user': user,
        'authenticator': 'SNOWFLAKE_JWT',
        'private_key_file': private_key_file,
        'private_key_file_pwd': private_key_file_pwd,
        'warehouse': warehouse,
        'database': database,
        'schema': schema
    }

    logger.info(f"Starting Execute Query")
    print('Starting Execute Query')
    logger.info(f"Connecting to Snowflake")

    try:
        ctx = sc.connect(**conn_params)
        cursor = ctx.cursor()
        print("Snowflake connection SUCCESS")
    except Exception as e:
        logger.error("Connection Failed", exc_info=True)
        raise e  

    logger.info("Connected to Snowflake")

    try: 
    # Execute query and fetch data 
        cursor.execute(query)
    except Exception as e:
        logger.error("Connection Failed", exc_info=True)
        raise e  

    logger.info(f"Querry: {query} executed")