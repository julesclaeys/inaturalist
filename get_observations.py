#Import Packages
import requests
import time
import json
from datetime import date, timedelta, datetime
import logging
import os


def get_observations(place_ids, DAYS_BACK):
    # Set up Try block for Logging
    try: 
        # Set Up Logging
        logger = logging.getLogger("get_observations")
        logger.setLevel(logging.DEBUG)  # Capture everything, handlers decide what to save

        #Set Up Logger Format
        log_format = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        ) # Configure logging

        #Set up Log file Name
        ts = int(time.time())
        output_file = f"get_observations_log_{ts}.log"

        #Set up Different Paths for different Levels of Logging (Info)
        info_dir = 'logs/get_observations/INFO'
        os.makedirs(info_dir, exist_ok=True)
        info_log = logging.FileHandler("logs/get_observations/INFO/" + output_file, encoding="utf-8")
        logger.addHandler(info_log)
        info_log.setLevel(logging.INFO)
        info_log.setFormatter(log_format)
        info_log.addFilter(lambda record: record.levelno == logging.INFO)

        #Set up Different Paths for different Levels of Logging (Warning)
        warning_dir = 'logs/get_observations/WARNING'
        os.makedirs(warning_dir, exist_ok=True)
        Warning_log = logging.FileHandler("logs/get_observations/WARNING/" + output_file, encoding="utf-8")
        logger.addHandler(Warning_log)
        Warning_log.setLevel(logging.WARNING)
        Warning_log.setFormatter(log_format)
        Warning_log.addFilter(lambda record: record.levelno == logging.WARNING)

            #Set up Different Paths for different Levels of Logging (ERROR)
        error_dir = 'logs/get_observations/ERROR'
        os.makedirs(error_dir, exist_ok=True)
        error_log = logging.FileHandler("logs/get_observations/ERROR/" + output_file, encoding="utf-8")
        logger.addHandler(error_log)
        error_log.setLevel(logging.ERROR)
        error_log.setFormatter(log_format)
        error_log.addFilter(lambda record: record.levelno == logging.ERROR)
    except Exception as e:
        logger.error(f"Error creating logger", exc_info=True)
     
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

        logger.info(f"Starting {date_str}")
        try: 
            for place_id in place_ids:
                params = {
                    "place_id": place_id,
                    "d1": date_str,
                    "d2": date_str,
                    "per_page": 200
                }

                response = requests.get(OBSERVATIONS_URL, params=params)
                response.raise_for_status()

                results = response.json().get("results", [])

                for obs in results:
                        obs["source_place_id"] = place_id
                        obs["extracted_date"] = date_str
                        daily_observations.append(obs)

                if len(results) > 0:
                    logger.info(f"Place_id {place_id}: {len(results)} on {date_str} obs")
                else: 
                    logger.warning(f"No observation found for Place_id {place_id} on {date_str}")
                time.sleep(5)

        except Exception as e: 
            logger.error(f"Error Could not find Observation", exc_info=True) 

        try: 

            file_name = f"Data/observations_{date_str}.json"
            with open(file_name, "w") as f:
                json.dump(daily_observations, f, indent=2)

        except Exception as e: 
            logger.error(f"Error Could not save Observations", exc_info=True) 

        logger.info(f"Saved {file_name} ({len(daily_observations)} records)")
        current_date += timedelta(days=1)

    logger.info(f"Get Observations Complete")
    return print('Get Observations Done')

