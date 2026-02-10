# 🌵 iNaturalist Python Tools

Python utilities for interacting with the **iNaturalist API** and processing biodiversity observation data. This repository allows you to fetch species observations, retrieve geographic places or parks, and work with taxonomic information.

---

## 🦆 Contents 

- [About iNaturalist API](#-about-inaturalist-api)  
- [Installation](#-installation)  
- [Usage](#-usage)  
  - [1. get_observations.py](#1-get_observationspy)  
  - [2. get_park_ids.py](#2-get_park_idspy)  
  - [3. get_places.py](#3-get_placespy)  
  - [4. taxon.py](#4-taxonpy)  
  - [5. main,.py](#5-mainpy)  
- [Repository Structure](#-repository-structure)  
- [Contributing](#-contributing)  
- [License](#-license)  
- [References](#-references)

---

## 🦊 About iNaturalist API

[iNaturalist](https://www.inaturalist.org/) is a global citizen-science platform where users can record observations of plants, animals, fungi, and other organisms. The iNaturalist API provides programmatic access to this data, enabling developers and researchers to:

- Query species observations
- Retrieve geographic locations and places
- Access taxonomic information
- Analyze biodiversity data for research or conservation projects

This repository provides Python scripts and utilities to simplify these interactions with the API.

---

## 🐼 Installation

1. **Clone the repository**

    git clone https://github.com/julesclaeys/inaturalist.git  
    cd inaturalist  

2. **Create and activate a virtual environment**

    python3 -m venv venv  
    source venv/bin/activate   # macOS / Linux  
    venv\Scripts\activate      # Windows  

3. **Install dependencies**

    pip install -r requirements.txt 


## 🐘 Usage

Each script serves a specific purpose when working with iNaturalist data.

---

### get_observations.py

Fetch observation data from iNaturalist based on taxon, place, and date filters.

    python get_observations.py --taxon_id 12345 --place_id 67890 --start_date 2025-01-01 --end_date 2025-02-01

**What it does:**

- Queries the iNaturalist observations endpoint  
- Filters observations by taxonomic ID  
- Filters by geographic place or park  
- Optionally filters by date range  
- Returns structured observation data (JSON or CSV)

---

### get_park_ids.py

Retrieve park identifiers for use in observation filtering.

    python get_park_ids.py

**What it does:**

- Queries iNaturalist places  
- Filters places categorized as parks  
- Outputs park names and corresponding place IDs  

---

### get_places.py

Search for geographic places in the iNaturalist database.

    python get_places.py --query "Yellowstone"

**What it does:**

- Searches for cities, regions, or parks  
- Returns place IDs, names, and bounding coordinates  
- Useful for discovering place IDs for other scripts  

---

### taxon.py

Utilities for taxonomic lookups and hierarchy exploration.

    python taxon.py --name "Panthera leo"

**What it does:**

- Resolves scientific or common names to taxon IDs  
- Retrieves parent and child taxa  
- Supports integration with observation queries  

---

### main,.py

Example integration and entrypoint script.

    python main,.py

**What it does:**

- Demonstrates how to combine taxon, place, and observation queries  
- Acts as a starting point for custom workflows  
- Can be extended for batch downloads or data pipelines