#Import Modules
from iNaturalist_Modules.get_park_ids import *
from iNaturalist_Modules.get_places import *
from iNaturalist_Modules.get_observations import *
from iNaturalist_Modules.taxon import *
from Modules.push_to_stage import *
from Modules.set_up_logs import *
from Modules.remove_local_data import *

# Set Up Variables
park_list = [
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
DAYS_BACK = 1
directory = "Data/"
stage = 'nature_stg'
#Run Pipeline
place_ids = fetch_park_id(park_list)
print(place_ids)
get_places(place_ids)
get_observations(place_ids, DAYS_BACK)
get_taxon()
push_to_stage(directory, stage) 
remove_local_data(directory)

