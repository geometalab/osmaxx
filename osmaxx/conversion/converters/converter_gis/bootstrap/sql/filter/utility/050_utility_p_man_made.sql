--man_made--
INSERT INTO osmaxx.utility_p
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange ,
    CASE
     WHEN osm_id<0 THEN 'R' -- Relation
     ELSE 'W'               -- Way
     END AS geomtype,
    way AS geom,
    'man_made' AS aggtype,
    man_made as type,
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
 WHERE man_made in ('water_works','wastewater_plant','storage_tank')
UNION
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange ,
    'W' AS geomtype,
    ST_Centroid(way) AS geom,
    'man_made' AS aggtype,
    man_made as type,
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
 WHERE man_made in ('water_works','wastewater_plant','storage_tank');
