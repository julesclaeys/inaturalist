#Import Packages
import requests
import time
import json
from datetime import date, timedelta, datetime
import logging
import os

from Modules.set_up_logs import *

def fetch_park_id(national_parks):
    logger = set_up_logger(fetch_park_id.__name__)


    try: 
        logger.info("Starting fetch_park_ids()")
        AUTOCOMPLETE_URL = "https://api.inaturalist.org/v1/places/autocomplete/" #API URL Query to obtain IDs for all our locations of interest
    except Exception as e: 
        logger.error("Error creating Park list", exc_info=True)

    place_ids = [] #Set Variables
    park_place_map = {}

    try: 
        for park in national_parks:
            response = requests.get(AUTOCOMPLETE_URL, params={"q": park})
            response.raise_for_status()
            results = response.json().get("results", [])
            if results:
                best = results[0]
                place_id = best["id"]

                place_ids.append(place_id)
                park_place_map[park] = {
                    "place_id": place_id,
                    "display_name": best["display_name"]
                }

                logger.info("Park Found, " + park + ':' + str(place_id))

            else:
                logger.warning("Park Not Found, " + park )
                park_place_map[park] = None

            time.sleep(0.1)
    except Exception as e: 
        logger.error("Error fetching Park data %s", exc_info=True)
    logger.info('Finished running fetch_park_id')
    logger.info(place_ids)
    print(F'finished get_park_ids')
    return place_ids
