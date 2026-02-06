#Import Packages
import requests
import time
import json
from datetime import date, timedelta, datetime
import logging
import os

#Import Modules
from get_park_ids import *
from get_places import *
from get_observations import *
from taxon import *


# Set Up Variables
SLEEP_SECONDS = 5
DAYS_BACK = 1

#Run Pipeline
place_ids = fetch_park_id()
print(place_ids)
get_places(place_ids)
get_observations(place_ids, DAYS_BACK)
get_taxon()
