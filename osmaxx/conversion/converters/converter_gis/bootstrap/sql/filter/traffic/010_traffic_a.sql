INSERT INTO osmaxx.traffic_a
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange ,
    CASE
     WHEN osm_id<0 THEN 'R' -- Relation
     ELSE 'W'               -- Way
     END AS geomtype,
    ST_Multi(way) AS geom,
    case
     when amenity='fuel' then 'fuel'
     when amenity in ('parking','bicycle_parking') then 'parking'
    end as aggtype,
    case
     when amenity='fuel' then 'fuel'
     when amenity='parking' then
        case
         when parking in ('site','multi-storey','underground','surface') then parking
         else 'parking'
        end
     when amenity='bicycle_parking' then 'bicycle'
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
    case
     when 'parking' is not null then "access"
    end as "access"
  FROM osm_polygon
  WHERE amenity in ('parking','fuel','bicycle_parking');
