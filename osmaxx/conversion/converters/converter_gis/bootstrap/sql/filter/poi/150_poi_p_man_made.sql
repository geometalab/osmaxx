---------------------------
--       man_made        --
---------------------------
INSERT INTO osmaxx.poi_p
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange,
    'N' AS geomtype, -- Node
    way AS geom,
-- Combining the different tags in Man-made POIs into different categories --
    case
     when man_made in ('tower','water_tower','windmill','lighthouse','watermill','surveillance') then 'miscpoi'
     else 'man_made'
    end as aggtype,
    case
     when man_made='tower' then
         case
          when "tower:type"='observation' then 'observation_tower'
          when "tower:type"='communication' then 'comm_tower'
          else 'tower'
         end
     when man_made in ('lighthouse','surveillance','water_tower','watermill','windmill') then man_made
     else 'man_made'
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
  FROM osm_point
  WHERE man_made not in ('water_well','water_works','wastewater_plant')
UNION
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange,
    CASE
    WHEN osm_id<0 THEN 'R'  -- Relation
     ELSE 'W'               -- Way
     END AS geomtype,
    ST_Centroid(way) AS geom,
-- Combining the different tags in Man-made POIs into different categories --
    case
     when man_made in ('tower','water_tower','windmill','lighthouse','watermill','surveillance') then 'miscpoi'
     else 'man_made'
    end as aggtype,
    case
     when man_made='tower' then
         case
          when "tower:type"='observation' then 'observation_tower'
          when "tower:type"='communication' then 'comm_tower'
          else 'tower'
         end
     when man_made in ('lighthouse','surveillance','water_tower','watermill','windmill') then man_made
     else 'man_made'
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
  WHERE man_made not in ('water_well','water_works','wastewater_plant');
