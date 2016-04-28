INSERT INTO osmaxx.boundary_l
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange ,
    CASE
     WHEN osm_id<0 THEN 'R' -- R=Relation
     ELSE 'W'               -- W=Way
     END AS geomtype,
    ST_Multi(way) AS geom,

-- Differentiates between the administrative boundaries --
    case
     when boundary='protected_area' then 'protected_area'
     when boundary='national_park' then 'national_park'
     when boundary='administrative' then
        case
         when admin_level='2' then 'national'
          when admin_level is not null then 'admin_level' || admin_level
         else 'administrative'
        end
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
  FROM osm_line
  WHERE boundary='administrative' or boundary='national_park' or boundary='protected_area';
