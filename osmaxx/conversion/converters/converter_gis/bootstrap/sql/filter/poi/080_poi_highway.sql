---------------------------
--         highway       --
---------------------------
INSERT INTO osmaxx.poi_a
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange,
    CASE
     WHEN osm_id<0 THEN 'R' -- Relation
     ELSE 'W'               -- Way
     END AS geomtype,
    ST_Multi(way) AS geom,
-- Combining the different tags in Highway into different categories --
    case
     when highway='emergency_access_point' then 'miscpoi'
    end as aggtype,
    case
     when highway='emergency_access_point' then 'emergency_access'
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
    cast(tags as text) as tags,
    website as website,
    wikipedia as wikipedia,
    case
        when "contact:phone" is not NULL then "contact:phone"
        else phone
    end as phone,
    opening_hours as opening_hours,
    cuisine as cuisine,
    "access" as "access",
    brand as brand,
    "tower:type" as tower_type
  FROM osm_polygon
  WHERE highway='emergency_access_point';
