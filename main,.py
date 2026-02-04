import requests
import time
import json
from datetime import date, timedelta

# -----------------------------
# CONFIG
# -----------------------------
AUTOCOMPLETE_URL = "https://api.inaturalist.org/v1/places/autocomplete"
PLACES_URL = "https://api.inaturalist.org/v1/places"
OBSERVATIONS_URL = "https://api.inaturalist.org/v1/observations"

SLEEP_SECONDS = 5
DAYS_BACK =4
# -----------------------------
# NATIONAL PARK NAMES
# -----------------------------
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
    "Niagara Falls",


]

# -----------------------------
# STEP 1: RESOLVE PLACE IDS
# -----------------------------
place_ids = []
park_place_map = {}

print("\n🔍 Resolving park place IDs...\n")

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

        print(f"✔ {park} → {place_id}")

    else:
        print(f"✘ No match found for {park}")
        park_place_map[park] = None

    time.sleep(0.1)

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
