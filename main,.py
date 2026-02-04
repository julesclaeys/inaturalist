import requests
import time
import json
from datetime import date, timedelta, datetime
import logging
import os

#Import Functions
from get_park_ids import *


# -----------------------------
# CONFIG
# -----------------------------
#AUTOCOMPLETE_URL = "https://api.inaturalist.org/v1/places/autocomplete"
PLACES_URL = "https://api.inaturalist.org/v1/places"
OBSERVATIONS_URL = "https://api.inaturalist.org/v1/observations"

SLEEP_SECONDS = 5
DAYS_BACK =4

place_ids = fetch_park_id()

# -----------------------------
# STEP 2: FETCH PLACE DETAILS
# -----------------------------
print("\n📍 Fetching place details...\n")

place_details = []

for place_id in place_ids:
    response = requests.get(f"{PLACES_URL}/{place_id}")
    response.raise_for_status()
    results = response.json().get("results", [])

    if not results:
        continue

    place = results[0]

    place_details.append({
        "place_id": place["id"],
        "name": place["display_name"],
        "place_type": place.get("place_type"),
        "admin_level": place.get("admin_level"),
        "ancestor_place_ids": place.get("ancestor_place_ids", []),
        "bbox_area": place.get("bbox_area"),
        "location": place.get("location"),                     # "lat,lon"
        "geometry_geojson": place.get("geometry_geojson"),     # full polygon
        "bounding_box_geojson": place.get("bounding_box_geojson")
    })

    print(f"✔ {place['display_name']}")
    time.sleep(0.5)

with open("place_details.json", "w") as f:
    json.dump(place_details, f, indent=2)

print("\n💾 Saved place_details.json")

# -----------------------------
# STEP 3: FETCH OBSERVATIONS (1 FILE PER DAY)
# -----------------------------
print("\n🦋 Fetching observations...\n")

today = date.today()
start_date = today - timedelta(days=DAYS_BACK)
current_date = start_date

while current_date <= today:
    date_str = current_date.strftime("%Y-%m-%d")
    daily_observations = []

    print(f"\n📅 {date_str}")

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

        print(f"  ✔ place_id {place_id}: {len(results)} obs")
        time.sleep(5)

    file_name = f"observations_{date_str}.json"
    with open(file_name, "w") as f:
        json.dump(daily_observations, f, indent=2)

    print(f"💾 Saved {file_name} ({len(daily_observations)} records)")
    current_date += timedelta(days=1)

print("\n✅ Pipeline complete.")
