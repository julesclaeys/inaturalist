#Import Packages
import requests
import time
import json
from datetime import date, timedelta, datetime
import logging
import os
from set_up_logs import *

def get_observations(place_ids, DAYS_BACK):

#############################
# This function fetches all observation data from the inaturalist api 
# for specific places and a certain amount of days from today
#############################
   
    logger = set_up_logger(get_observations.__name__)
     
    #Start of the actual function
    logger.info(f"Starting get_observations()")

    #Setting up Variables for the run
    OBSERVATIONS_URL = "https://api.inaturalist.org/v1/observations"
    SLEEP_SECONDS = 5
    today = date.today()
    start_date = today - timedelta(days=DAYS_BACK)
    current_date = start_date

    #Start a While loop to go through each date separately
    while current_date <= today:
        date_str = current_date.strftime("%Y-%m-%d")
        daily_observations = []
#Set up parameters 
        logger.info(f"Starting {date_str}")
        try: 
            for place_id in place_ids:
                params = {
                    "place_id": place_id,
                    "d1": date_str,
                    "d2": date_str,
                    "per_page": 200
                }
#Make API Call
                response = requests.get(OBSERVATIONS_URL, params=params)
                response.raise_for_status()

                results = response.json().get("results", [])

                for obs in results:
                        obs["source_place_id"] = place_id
                        obs["extracted_date"] = date_str
                        daily_observations.append(obs)
#Log success or not for different places
                if len(results) > 0:
                    logger.info(f"Place_id {place_id}: {len(results)} on {date_str} obs")
                else: 
                    logger.warning(f"No observation found for Place_id {place_id} on {date_str}")
                time.sleep(5)

        except Exception as e: 
            logger.error(f"Error Could not find Observation", exc_info=True) 

        try: 
#Save json to file 
            file_name = f"Data/observations_{date_str}.json"
            with open(file_name, "w") as f:
                json.dump(daily_observations, f, indent=2)

        except Exception as e: 
            logger.error(f"Error Could not save Observations", exc_info=True) 

        logger.info(f"Saved {file_name} ({len(daily_observations)} records)")
        current_date += timedelta(days=1)

    logger.info(f"Get Observations Complete")
    return print('Get Observations Done')

