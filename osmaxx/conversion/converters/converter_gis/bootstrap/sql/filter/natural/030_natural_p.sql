INSERT INTO osmaxx.natural_p
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange ,
    'N' AS geomtype, -- N=Node
    way AS geom,
-- Differentiating between different natural NODES --
    case
     when "natural" in ('beach','cave_entrance','fell','grassland','heath','moor','mud','peak','rock','saddle','sand','sinkhole','stone',
                'tree','volcano','wood','glacier','wetland') then "natural"
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
  FROM osm_point
  WHERE "natural" not in ('water', 'spring','bare_rock','scree','cliff')
UNION
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange ,
    CASE
     WHEN osm_id<0 THEN 'R' -- Relations
     ELSE 'W'               -- W=Way
     END AS geomtype,
    ST_Centroid(way) AS geom,
-- Differentiating between different natural NODES --
    case
     when "natural" in ('beach','cave_entrance','fell','grassland','heath',
                'moor','mud','peak','rock','saddle','sand','sinkhole','stone',
                'tree','volcano','wood','glacier','wetland') then "natural"
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
  WHERE "natural" not in ('water', 'spring','bare_rock','scree','cliff');
