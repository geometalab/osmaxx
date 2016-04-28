--man_made--
INSERT INTO osmaxx.utility_l
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange ,
    'W' AS geomtype,       -- Way
    ST_Multi(way) AS geom,
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
    cast(tags as text) as tags,
    operator as operator,
    null as voltage,
    null as frequency
 FROM osm_line
 WHERE man_made in ('pipeline');
