CREATE OR REPLACE VIEW G_OBSERVATIONS AS

SELECT DISTINCT   
o.observation_id -- Our Unique Row ID
, p.coordinates as Polygon -- Shapes for Tableau, represents the Park. 
, p.place_id -- Park ID
, p.place_name -- Park Name
, p.country -- Country, not well populated, sometimes region, usually 2 letters
, p.state 
, p.coordinates
, t.taxon_name -- scientific name
, t.Common_name -- free input field
, t.recognisable_name -- Free input field, can be at a higher taxon level
, o.is_threatened 
, k.scientific_name as Kingdom_Name
, phy.common_name as Phylum_Common_name
, phy.scientific_name as Phylum_Name
, k.common_name as Kingdom_Common_name
, c.scientific_name as Class_Name
, c.common_name as Class_Common_name
, ord.scientific_name as Order_Name
, ord.common_name as Order_Common_name
, f.scientific_name as Family_Name
, f.common_name as Family_Common_name
, g.scientific_name as Genus_Name
, g.common_name as Genus_Common_name
, l.location_id
, l.location_guess
, l.latitude
, l.longitude
, u.login
, u.name
, u.orcid
, u.created_at
, u.is_suspended
, o.is_endemic
, o.is_native
, o.was_introduced
, o.description
, o.published_timestamp
, o.identification_disagreements_count
, o.observation_timestamp
, o.conservation_status
, o.is_extinct
, o.quality
, o.project_id
, CONCAT(o.photo_url, '?raw=true') as photo_url
, replace(CONCAT(o.photo_url, '?raw=true'), 'original', 'square') as square_photo_url

FROM TIL_DATA_ENGINEERING.JC_NATURE.S_Observations o
INNER JOIN S_Taxon  t
    ON o.taxon_id = t.taxon_id
INNER JOIN S_LOCATION l
     ON o.location_id = l.location_id
 INNER JOIN S_USER u
     ON o.user_id = u.user_id
LEFT JOIN S_REFERENCE_TAXONOMY k
    ON t.kingdom_ID = k.taxon_id
LEFT JOIN S_REFERENCE_TAXONOMY phy
    ON t.Phylum_ID = phy.taxon_id
LEFT JOIN S_REFERENCE_TAXONOMY c
    ON t.class_id = c.taxon_id
LEFT JOIN S_REFERENCE_TAXONOMY ord
    ON t.order_id = ord.taxon_id
LEFT JOIN S_REFERENCE_TAXONOMY f
    ON t.family_ID = f.taxon_id
LEFT JOIN S_REFERENCE_TAXONOMY g
    ON t.genus_ID = g.taxon_id
JOIN LATERAL FLATTEN(input => o.place_ids) flat
RIGHT JOIN TIL_DATA_ENGINEERING.JC_NATURE.S_PLACES p -- Right join so parks without observations are kept
  ON flat.value::STRING = p.place_id;
