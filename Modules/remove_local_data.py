#Import Packages
import os
from dotenv import load_dotenv
import snowflake.connector as sc

#Import Modules
from Modules.set_up_logs import *

def remove_local_data(directory, stage, schema, database, account, password, private_key, warehouse, user):

#############################
# This function cleans the data folder to not store data for too long.
# It uses snowflake to ensure we only delete files which have been uploaded to the stage correctly.
# Some formatting is required hence the changes within the for loop. 
#############################

#Setting up Logger

    logger = set_up_logger(remove_local_data.__name__)

#Starting connection to snowflake

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
