
-- BRONZE -> Copy into

-- Creating a file format for Json files, making sure to strip the outer array. 
CREATE FILE FORMAT IF NOT EXISTS nature_json_format
TYPE = JSON
STRIP_OUTER_ARRAY = TRUE;

-- Copying the observations data from stage to Bronze Observation Table
COPY INTO B_OBSERVATIONS
FROM @NATURE_STG
FILE_FORMAT = (FORMAT_NAME = nature_json_format)
PATTERN = '.*observations.*\.json.*'
ON_ERROR = 'CONTINUE';

-- Copying the taxon data from stage to Bronze Taxon Table
COPY INTO B_TAXON_LIST
FROM @NATURE_STG
FILE_FORMAT = (FORMAT_NAME = nature_json_format)
PATTERN = '.*taxa.*\.json.*'
ON_ERROR = 'CONTINUE';

-- For the places details, we don't want to insert new data but refresh the data instead, so we can truncate the table and refresh it. 
TRUNCATE TABLE B_PLACES_DETAILS;

-- Copying the places data from stage to Bronze places details Table
COPY INTO B_PLACES_DETAILS
FROM @NATURE_STG
FILE_FORMAT = (FORMAT_NAME = nature_json_format)
PATTERN = '.*place.*\.json.*'
ON_ERROR = 'CONTINUE';