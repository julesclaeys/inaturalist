import requests
import time
import json
from datetime import date, timedelta, datetime
import logging
import os

def fetch_park_id():
    # Set up Try block for Logging
    try: 
        # Set Up Logging
        logger = logging.getLogger("get_park_ids")
        logger.setLevel(logging.DEBUG)  # Capture everything, handlers decide what to save

        #Set Up Logger Format
        log_format = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        ) # Configure logging

        #Set up Log file Name
        ts = int(time.time())
        output_file = f"get_park_ids_log_{ts}.log"

        #Set up Different Paths for different Levels of Logging (Info)
        info_dir = 'logs/get_park_ids/INFO'
        os.makedirs(info_dir, exist_ok=True)
        info_log = logging.FileHandler("logs/get_park_ids/INFO/" + output_file, encoding="utf-8")
        logger.addHandler(info_log)
        info_log.setLevel(logging.INFO)
        info_log.setFormatter(log_format)
        info_log.addFilter(lambda record: record.levelno == logging.INFO)

        #Set up Different Paths for different Levels of Logging (Warning)
        warning_dir = 'logs/get_park_ids/WARNING'
        os.makedirs(warning_dir, exist_ok=True)
        Warning_log = logging.FileHandler("logs/get_park_ids/WARNING/" + output_file, encoding="utf-8")
        logger.addHandler(Warning_log)
        Warning_log.setLevel(logging.WARNING)
        Warning_log.setFormatter(log_format)
        Warning_log.addFilter(lambda record: record.levelno == logging.WARNING)

            #Set up Different Paths for different Levels of Logging (ERROR)
        error_dir = 'logs/get_park_ids/ERROR'
        os.makedirs(error_dir, exist_ok=True)
        error_log = logging.FileHandler("logs/get_park_ids/ERROR/" + output_file, encoding="utf-8")
        logger.addHandler(error_log)
        error_log.setLevel(logging.ERROR)
        error_log.setFormatter(log_format)
        error_log.addFilter(lambda record: record.levelno == logging.ERROR)
    except Exception as e:
        logger.error("Error creating logger", exc_info=True)

    try: 
        logger.info("Starting fetch_park_ids()")
        AUTOCOMPLETE_URL = "https://api.inaturalist.org/v1/places/autocomplete/" #API URL Query to obtain IDs for all our locations of interest
        # -----------------------------
        # NATIONAL PARK NAMES
        # ----------------------------- (Chat GPT Generated List, with additional locations for my own interest, not all work but that is part of the code)
        national_parks = [
            "Acadia National Park",
            "American Samoa National Park",
            "Arches National Park",
            "Badlands National Park",
            "Big Bend National Park",
            "Biscayne National Park",
            "Black Canyon of the Gunnison National Park",
            "Bryce Canyon National Park",
            "Canyonlands National Park",
            "Capitol Reef National Park",
            "Carlsbad Caverns National Park",
            "Channel Islands National Park",
            "Congaree National Park",
            "Crater Lake National Park",
            "Cuyahoga Valley National Park",
            "Death Valley National Park",
            "Denali National Park & Preserve",
            "Dry Tortugas National Park",
            "Everglades National Park",
            "Gates of the Arctic National Park & Preserve",
            "Gateway Arch National Park",
            "Glacier Bay National Park & Preserve",
            "Glacier National Park",
            "Grand Canyon National Park",
            "Grand Teton National Park",
            "Great Basin National Park",
            "Great Sand Dunes National Park & Preserve",
            "Great Smoky Mountains National Park",
            "Guadalupe Mountains National Park",
            "Haleakalā National Park",
            "Hawaiʻi Volcanoes National Park",
            "Hot Springs National Park",
            "Indiana Dunes National Park",
            "Isle Royale National Park",
            "Joshua Tree National Park",
            "Katmai National Park & Preserve",
            "Kenai Fjords National Park",
            "Kings Canyon National Park",
            "Kobuk Valley National Park",
            "Lake Clark National Park & Preserve",
            "Lassen Volcanic National Park",
            "Mammoth Cave National Park",
            "Mesa Verde National Park",
            "Mount Rainier National Park",
            "New River Gorge National Park & Preserve",
            "North Cascades National Park",
            "Olympic National Park",
            "Petrified Forest National Park",
            "Pinnacles National Park",
            "Redwood National Park",
            "Rocky Mountain National Park",
            "Saguaro National Park",
            "Sequoia National Park",
            "Shenandoah National Park",
            "Theodore Roosevelt National Park",
            "Virgin Islands National Park",
            "Voyageurs National Park",
            "White Sands National Park",
            "Wind Cave National Park",
            "Wrangell–St. Elias National Park & Preserve",
            "Yellowstone National Park",
            "Yosemite National Park",
            "Zion National Park",
            "Monterey Bay",
            "Monument Valley",
            "Niagara Falls"


        ]

        place_ids = [] #Set Variables
        park_place_map = {}
    except Exception as e: 
        logger.error("Error creating Park list", exc_info=True)

    try: 
        test = int('ab')
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
    print(place_ids)
    return place_ids

print(fetch_park_id())