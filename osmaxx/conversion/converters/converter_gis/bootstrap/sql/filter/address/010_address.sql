------------------
--   building   --
------------------

-- Without the Entrance Node i.e; just the building --
INSERT INTO osmaxx.address_p
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange,
    'N' AS geomtype, -- When address is linked to a node
    way AS geom,
    'b' AS type,     -- When address is linked to a building
    name as name,
    "name:en" as name_en,
    "name:fr" as name_fr,
    "name:es" as name_es,
    "name:de" as name_de,
    int_name as name_int,
    case
        when name is not null AND name = transliterate(name) then name
        when "name:en" is not null then "name:en"
        when "name:fr" is not null then "name:fr"
        when "name:es" is not null then "name:es"
        when "name:de" is not null then "name:de"
        when name is not null then transliterate(name)
        else NULL
    end as label,
    cast(tags as text) as tags,
    case
        when "addr:street" is not null then "addr:street"
        when "addr:place" is not null then "addr:place"
        else NULL
    end  as street,
    "addr:housenumber" as housenumber,
    "addr:postcode" as postcode,
    "addr:place" as city,
    "addr:country" as country
  FROM osm_point
where building !='entrance' and entrance is null and ("addr:street" !='' OR "addr:housenumber"!='' OR "addr:place"!='')

-- Without the Entrance Node and the addresses are part of a way  --
UNION
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange,
    CASE
     WHEN osm_id<0 THEN 'R' -- R=Relation
     ELSE 'W'               -- W=Way
     END AS geomtype,
    ST_Centroid(way) AS geom,
    'b' AS type,
    name as name,
    "name:en" as name_en,
    "name:fr" as name_fr,
    "name:es" as name_es,
    "name:de" as name_de,
    int_name as name_int,
    case
        when name is not null AND name = transliterate(name) then name
        when "name:en" is not null then "name:en"
        when "name:fr" is not null then "name:fr"
        when "name:es" is not null then "name:es"
        when "name:de" is not null then "name:de"
        when name is not null then transliterate(name)
        else NULL
    end as label,
    cast(tags as text) as tags,
    case
        when "addr:street" is not null then "addr:street"
        when "addr:place" is not null then "addr:place"
        else NULL
    end  as street,
    "addr:housenumber" as housenumber,
    "addr:postcode" as postcode,
    "addr:place" as city,
    "addr:country" as country
  FROM osm_polygon
where building !='entrance' and entrance is null and ("addr:street" !='' OR "addr:housenumber"!='' OR "addr:place"!='');
