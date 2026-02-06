import requests
import time
import json
from datetime import date, timedelta, datetime
import logging
import os
from dotenv import load_dotenv
import pandas as pd
import csv

def get_places(place_ids):
    # Set up Try block for Logging
    try: 
        # Set Up Logging
        logger = logging.getLogger("get_places")
        logger.setLevel(logging.DEBUG)  # Capture everything, handlers decide what to save

        #Set Up Logger Format
        log_format = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        ) # Configure logging

        #Set up Log file Name
        ts = int(time.time())
        output_file = f"get_places_log_{ts}.log"

        #Set up Different Paths for different Levels of Logging (Info)
        info_dir = 'logs/get_places/INFO'
        os.makedirs(info_dir, exist_ok=True)
        info_log = logging.FileHandler("logs/get_places/INFO/" + output_file, encoding="utf-8")
        logger.addHandler(info_log)
        info_log.setLevel(logging.INFO)
        info_log.setFormatter(log_format)
        info_log.addFilter(lambda record: record.levelno == logging.INFO)

        #Set up Different Paths for different Levels of Logging (Warning)
        warning_dir = 'logs/get_places/WARNING'
        os.makedirs(warning_dir, exist_ok=True)
        Warning_log = logging.FileHandler("logs/get_places/WARNING/" + output_file, encoding="utf-8")
        logger.addHandler(Warning_log)
        Warning_log.setLevel(logging.WARNING)
        Warning_log.setFormatter(log_format)
        Warning_log.addFilter(lambda record: record.levelno == logging.WARNING)

            #Set up Different Paths for different Levels of Logging (ERROR)
        error_dir = 'logs/get_places/ERROR'
        os.makedirs(error_dir, exist_ok=True)
        error_log = logging.FileHandler("logs/get_places/ERROR/" + output_file, encoding="utf-8")
        logger.addHandler(error_log)
        error_log.setLevel(logging.ERROR)
        error_log.setFormatter(log_format)
        error_log.addFilter(lambda record: record.levelno == logging.ERROR)
    except Exception as e:
        logger.error("Error creating logger", exc_info=True)
     
    
    logger.info("Starting get_places()")

    try: 
        #Setting Up Variables
        place_details = []
        PLACES_URL = "https://api.inaturalist.org/v1/places"

        #Looping Through Parks list
        for place_id in place_ids:
            try: 
                response = requests.get(f"{PLACES_URL}/{place_id}")
                response.raise_for_status()
                results = response.json().get("results", [])
            except Exception as e:
                logger.warning("Failed to fetch place_id=%s", place_id, exc_info=True)
                continue
                
            if not results:
                continue

            place = results[0]

            place_details.append({ #Makes a nice formatting for the json
                "place_id": place["id"],
                "name": place["display_name"],
                "place_type": place.get("place_type"),
                "admin_level": place.get("admin_level"),
                "ancestor_place_ids": place.get("ancestor_place_ids", []),
                "bbox_area": place.get("bbox_area"),
                "location": place.get("location"),                 
                "geometry_geojson": place.get("geometry_geojson"),    
                "bounding_box_geojson": place.get("bounding_box_geojson")
            })

            logger.info(F"place found")
            time.sleep(0.5)
    except Exception as e:
        logger.error("Error pulling data", exc_info=True)
 
    logger.info("Creating place_details.json")
    try:
        with open("Data/place_details.json", "w") as f:
            json.dump(place_details, f, indent=2)
    except Exception as e:
        logger.error("Error creating json file", exc_info=True)



