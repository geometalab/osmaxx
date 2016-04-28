INSERT INTO osmaxx.natural_a
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange,
    CASE
     WHEN osm_id<0 THEN 'R' -- R=Relation
     ELSE 'W'               -- W=Way
     END AS geomtype,
    ST_Multi(way) AS geom,

-- Differentiating between different natural AREAS --
    case
     when "natural" in ('bare_rock','beach','cave_entrance','fell','grassland','heath','moor','mud','sand','scree','sinkhole','wood','glacier','wetland') then "natural"
     when "natural"='scrub' or landuse='scrub' then 'scrub'
     else 'natural'
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
  WHERE "natural" not in ('water', 'spring','rock','peak','tree','volcano','saddle','cliff');
