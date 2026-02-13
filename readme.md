# 🌵 iNaturalist Python Tools

This is a Python Project utilising the iNaturalist API and going through biodiversity observations in National Parks and additional Locations to publish them to a Snowflake Server. You can utilise some of the Python Scripts and edit them to retrieve data from your favorite locations! 

---

## 🦆 Contents 

- [About iNaturalist API](#-about-inaturalist-api)  
- [Installation](#-installation)  
- [Usage](#-usage)  
  - [1. main.py](#1-mainpy)  
  - [2. get_park_ids.py](#2-get_park_idspy)  
  - [3. get_places.py](#3-get_placespy)  
  - [4. taxon.py](#4-taxonpy)  
  - [5. push_to_stage.py](#5-push_to_stage)  
- [Repository Structure](#-repository-structure)  
- [Contributing](#-contributing)  
- [License](#-license)  
- [References](#-references)

---

## 🦊 About iNaturalist API

[iNaturalist](https://www.inaturalist.org/) is a global community where users can record observations of plants, animals, fungi, and other organisms. The iNaturalist API provides access to this data, enabling developers and researchers to:

- Query species observations
- Retrieve geographic locations and places
- Access taxonomic information
- Analyze biodiversity data for research or conservation projects

This repository provides Python scripts and utilities to simplify these interactions with the API.

Here's a link to the API documentation: https://www.inaturalist.org/pages/api+reference

---

## 🐼 Installation

1. **Clone the repository**

    git clone https://github.com/julesclaeys/inaturalist.git  
    cd inaturalist  

2. **Create and activate a virtual environment**

    python3 -m venv venv  
    venv\Scripts\activate      # Windows  

3. **Install dependencies**
    All the required packages should be in the requirements.txt file!
   
    pip install -r requirements.txt 

These steps should allow you to use the scripts on your machine. Any script connecting to snowflake (Taxon.py, push_to_stage.py) require you to put your own snowflake account details. 

## 🐘 Usage

Each script serves a specific purpose when working with iNaturalist data: 

---

### 🐒 main.py

This is how I use the different functions. Only parameters to input at the Sleep_seconds which will decide how long to wait in between API calls in order to not overload the API with requests. Days_Back decides how many days, in addition to today, the script will search data for. 0 Means just today and is the default value. Removing the get_taxon() and push_to_stage() will allow a user to run the script without Snowflake. 

---

### 🐯 get_park_ids.py

This function takes a list of strings, these are the locations we want to obtain the IDs for. This will use the API's Get places autocomplete function to find the IDs related to each of the places. If the API does not find a location for the string, they will be sent into the logs into the warning folder. If it cannot find your location, it is worth trying different spellings, certain characters are not recognised. 

Example result from the logs:  

Channel Islands National Park:3157
Park Not Found, Indiana Dunes National Park.

The function outputs a list of IDs. 

---

### 🐩 get_observations.py

Fetch observation data from iNaturalist based on taxon, place, and date filters.

    python get_observations.py --taxon_id 12345 --place_id 67890 --start_date 2025-01-01 --end_date 2025-02-01

**What it does:**

- Queries the iNaturalist observations endpoint  
- Filters observations by taxonomic ID  
- Filters by geographic place or park  
- Optionally filters by date range  
- Returns structured observation data (JSON or CSV)

---

### 🌺 get_park_ids.py

Retrieve park identifiers for use in observation filtering.

    python get_park_ids.py

**What it does:**

- Queries iNaturalist places  
- Filters places categorized as parks  
- Outputs park names and corresponding place IDs  

---

### taxon.py

Utilities for taxonomic lookups and hierarchy exploration.

    python taxon.py --name "Panthera leo"

**What it does:**

- Resolves scientific or common names to taxon IDs  
- Retrieves parent and child taxa  
- Supports integration with observation queries  

---


**What it does:**

- Demonstrates how to combine taxon, place, and observation queries  
- Acts as a starting point for custom workflows  
- Can be extended for batch downloads or data pipelines
