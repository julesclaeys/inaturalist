-- SILVER -> Places Dimension Table 
CREATE OR REPLACE TABLE S_PLACES as
SELECT DISTINCT
    VARIANT_COL:place_id::string as Place_ID -- Obtaining the ID Field
  , SPLIT_PART(VARIANT_COL:name::string, ',', 1) as Place_Name -- Name can be different from the original prompt given in Python
  , SPLIT_PART(VARIANT_COL:name::string, ',', 2) as Country 
  , SPLIT_PART(VARIANT_COL:name::string, ',', 3) as State -- if USA
  ,  ,TO_GEOGRAPHY(VARIANT_COL:geometry_geojson::variant) as Coordinates --Using to_geography we create a polygon for mapping.  
  ,VARIANT_COL:place_type::string as Place_type_ID -- Place type ID can represent national parks or city for example
  , SPLIT_PART(VARIANT_COL:location::string, ',', 1) as Latitude -- Coordinates of centre point of the park
  , SPLIT_PART(VARIANT_COL:location::string, ',', 2) as Longitude
FROM
  "TIL_DATA_ENGINEERING"."JC_NATURE"."B_PLACES_DETAILS" ; 


-- SILVER -> Taxonomy Dimension Table 
CREATE OR REPLACE TABLE S_Taxon as
SELECT DISTINCT 
VARIANT_COL:taxon:id::string as Taxon_ID 
,VARIANT_COL:taxon:name::string as Taxon_Name -- Scientific Name
, INITCAP(VARIANT_COL:taxon:preferred_common_name::string) as Common_name -- If exists, common name
, VARIANT_COL:taxon:iconic_taxon_name::string as Recognisable_Name -- If not there's a recognisable name but can loose some details
, VARIANT_COL:taxon:rank_level::int as Rank_Level 
, VARIANT_COL:taxon:rank::string as Rank -- Taxonomy Rank
, VARIANT_COL:taxon:ancestor_ids[1]::int as Kingdom_ID -- Next few IDs are used to fetch taxon information in the get_taxon script
, VARIANT_COL:taxon:ancestor_ids[2]::int as Phylum_ID
, VARIANT_COL:taxon:ancestor_ids[3]::int as Class_ID
, VARIANT_COL:taxon:ancestor_ids[4]::int as Order_ID
, VARIANT_COL:taxon:ancestor_ids[5]::int as Family_ID
, VARIANT_COL:taxon:ancestor_ids[6]::int as Genus_ID
FROM TIL_DATA_ENGINEERING.JC_NATURE.B_OBSERVATIONS
WHERE VARIANT_COL:taxon:name::string IS NOT NULL -- remove unidentified observations as they currently break the logic 
;

-- Silver -> Taxonomy reference table (result of get_Taxon())
CREATE OR REPLACE TABLE S_REFERENCE_TAXONOMY AS 

  SELECT DISTINCT 
  variant_col:results[0].id::varchar as Taxon_ID
, variant_col:results[0].name::varchar as Scientific_Name -- Different naming conventions 
, variant_col:results[0].preferred_common_name::varchar as Common_Name
, variant_col:results[0].iconic_taxon_name::varchar as Iconic_Name
, variant_col:results[0].rank::varchar as Rank -- Taxonomic Rank
, REGEXP_REPLACE( VARIANT_COL:results[0]:wikipedia_summary::varchar, '<[^>]+>', ''  )  as Summary -- Wikipedia Summary 
, VARIANT_COL:results[0]:wikipedia_url::varchar as Wikipedia_URL -- URL To species Wikipedia
, variant_col:results[0].extinct::boolean as IsExtinct -- Is the species extinct 
, variant_col:results[0].conservation_statuses::varchar as Conservation_Statuses -- Conservation Status of the species
, variant_col:results[0].children[0].id::varchar as Child_ID 
, variant_col:results[0].children[0].name::varchar as Child_Name
, variant_col:results[0].children[0].rank::varchar as Child_Rank  
, variant_col:results[0].ancestors[ARRAY_SIZE(variant_col:results[0].ancestors)-1].id::varchar as Ancestor_ID -- First Ancestor Details
, variant_col:results[0].ancestors[ARRAY_SIZE(variant_col:results[0].ancestors)-1].name::varchar as Ancestor_Name 
, variant_col:results[0].ancestors[ARRAY_SIZE(variant_col:results[0].ancestors)-1].rank::varchar as Ancestor_Rank 
  
  FROM
  "TIL_DATA_ENGINEERING"."JC_NATURE"."B_TAXON_LIST";

 
-- SILVER -> Location Dimension Table, Location unlike places details is directly where the observation occured
CREATE OR REPLACE TABLE S_Location as

SELECT DISTINCT 
VARIANT_COL:source_place_id::string as Location_ID
, VARIANT_COL:place_guess::string as Location_Guess -- This is a free input text field
, VARIANT_COL:place_ids::array as Place_ids -- These are other levels of place IDs, could be used in another API Query
, MIN(VARIANT_COL:geojson:coordinates[1]::double) as Latitude -- Coordinates, some places are a few meters off so using min to keep just one coordinate
, MIN(VARIANT_COL:geojson:coordinates[0]::double) as Longitude
FROM TIL_DATA_ENGINEERING.JC_NATURE.B_OBSERVATIONS
GROUP BY 1,2,3
;


-- SILVER -> User Dimension Table 
CREATE OR REPLACE TABLE S_USER as
SELECT DISTINCT 
VARIANT_COL:user:id::string as user_ID -- user id
, VARIANT_COL:user:login::string as login 
, VARIANT_COL:user:name::string as name -- name of the user
, VARIANT_COL:user:orcid::string as orcid -- orcid for researchers 
, VARIANT_COL:user:created_at::datetime as created_at 
, VARIANT_COL:user:suspended::boolean as is_suspended --careul you cannot name a field suspended
FROM TIL_DATA_ENGINEERING.JC_NATURE.B_OBSERVATIONS;

-- Silver -> Observation Facts Table
CREATE OR REPLACE TABLE S_Observations as
SELECT  DISTINCT
VARIANT_COL:id::string as Observation_ID -- Unique ID for each observation
, VARIANT_COL:user:id::string as user_ID -- All IDs are present in other tables we created
, VARIANT_COL:source_place_id::string as Location_ID
, VARIANT_COL:taxon:id::string as Taxon_ID
, VARIANT_COL:place_ids::array as Place_ids
, VARIANT_COL:taxon:native::boolean as is_native
, VARIANT_COL:taxon:endemic::boolean as is_endemic
, VARIANT_COL:taxon:introduced::boolean as was_introduced -- Was the species introduced to this area
, VARIANT_COL:description::string as description -- Description of the user for the observation
, VARIANT_COL:created_at::datetime as published_timestamp
, VARIANT_COL:time_observed_at::datetime as observation_timestamp
, VARIANT_COL:identification_disagreements_count::int as identification_disagreements_count
, VARIANT_COL:observation_photos:url::string as photo_url --URL for the observation made
, VARIANT_COL:project_ids::array as project_ID 
, VARIANT_COL:quality_grade::string as quality -- Quality of the observation
, VARIANT_COL:taxon:complete_species_count::int as complete_species_count
, VARIANT_COL:taxon:extinct::boolean as is_extinct
, VARIANT_COL:taxon:conservation_status:status_name::string as conservation_status
, VARIANT_COL:taxon:threatened::boolean as is_threatened 

FROM TIL_DATA_ENGINEERING.JC_NATURE.B_OBSERVATIONS;