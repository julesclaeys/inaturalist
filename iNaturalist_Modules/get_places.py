#Import Packages
import requests
import time
import json

from Modules.set_up_logs import *

def get_places(place_ids):

#############################
# This function uses a list of place IDs from inaturalist
# and searched for details regarding the place including exact coordinates
#############################
   

    logger = set_up_logger(get_places.__name__)
    
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
    print(f'finished get_places')


