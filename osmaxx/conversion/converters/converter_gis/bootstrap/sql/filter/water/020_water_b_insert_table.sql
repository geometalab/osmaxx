INSERT INTO osmaxx.water_p
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange,
    'N' AS geomtype,    -- Node
    way AS geom,
-- Classifying different Water Bodies --
    case
     when "natural" is not null then "natural"
     when leisure is not null then leisure
     when man_made is not null  then man_made
     when waterway in ('riverbank','dam','waterfall','lock_gate','weir') then waterway
     else 'waterway'
    end as type,

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
    cast(tags as text) as tags
     FROM osm_point
     WHERE waterway is not null or leisure in ('slipway','marina')  or man_made in ('reservoir_covered') or "natural" in ('water','spring')
UNION
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange,
    CASE
     WHEN osm_id<0 THEN 'R' -- Relation
     ELSE 'W'               -- Way
     END AS geomtype,
    ST_Centroid(way) AS geom,
-- Classifying different Water Bodies --
    case
     when "natural" is not null then "natural"
     when leisure is not null then leisure
     when man_made is not null  then man_made
     when waterway in ('riverbank','dam','waterfall','lock_gate','weir') then waterway
     else 'waterway'
    end as type,

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
    cast(tags as text) as tags
     FROM osm_polygon
     WHERE waterway is not null or leisure in ('slipway','marina')  or man_made in ('reservoir_covered') or "natural" in ('water','spring');
