from dotenv import load_dotenv
import os
import snowflake.connector as sc
import logging
from .set_up_logs import *

def push_to_stage(directory, stage, schema, database, account, password, private_key, warehouse, user):

#############################
# This function pushes all files in a directory into my snowflake Stage 
# This function will not work on your own stage! Just an example of what you could do. 
# If you want to set a similar one up, you will need a service account,
# A Key pair authentification method, and to give the service account read and write permissions
# on your stage. Before pushing the data, the script will check that the stage mentioned exists.
#############################

#Setting up logger
    logger = set_up_logger(push_to_stage.__name__)

#Obtain snowflake Parameters
    try: 
        load_dotenv()
        private_key_file = private_key
        private_key_file_pwd = password
        account = account
        user = user
        warehouse = warehouse
        database = database
        schema = schema
    except Exception as e: 
        logger.error(f"Error loading env variables", exc_info=True)

#Set up connection
    try: 

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
        logger.info(f"Starting Push_to_Stage")
        logger.info(f"Connecting to Snowflake")


#Connect to snowflake
        ctx = sc.connect(**conn_params)
        cursor = ctx.cursor()

    except Exception as e: 
        logger.error(f"Error connecting to Sonwflake")
    
    logger.info(f"Connection Successful, pushing to Stage")

#Check Stage Exists

    cursor.execute(f"SHOW STAGES LIKE '{stage}'")
    if cursor.fetchone() is not None:
#Push files from directory to stage
        try: 
            cursor.execute(f"""
            PUT file://{directory}/*
            @{stage}
            AUTO_COMPRESS = TRUE
            OVERWRITE = TRUE
            """)
            cursor.close()
            ctx.close()
        
        except Exception:
            logger.error("Failed to Push to Stage", exc_info=True)
            raise
    else: 
        logger.error(f"Stage {stage} does not exist")

    return print(f'Pushed {directory} to stage')

