--power--
INSERT INTO osmaxx.utility_p
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange ,
    'N' AS geomtype,     -- Node
    way AS geom,
-- Combining Tags for different kinds of Power POIs --
    case
     when "power"='plant' then 'plant'
     when "power"='tower' then 'tower'
     when "power"='pole' then 'pole'
     when "power"='generator' then 'station'
     when "power"='station' or "power"='sub_station'  then 'substation'
     when "power"='transformer' then 'transformer'
     else 'power'
    end as aggtype,
    case
     when "power"='plant' then 'plant'
     when "power"='tower' then 'tower'
     when "power"='pole' then 'pole'
     when "power"='generator' then
        case
         when "generator:source"='nuclear' then 'nuclear'
         when "generator:source"='solar' then 'solar'
         when "generator:source"='gas' or "generator:source"='coal' then 'fossil'
         when "generator:source"='hydro' then 'hydro'
         when "generator:source"='wind' then 'wind'
         else 'station'
        end
     when "power_source"='photovoltaic' then 'solar'
     when "power_source"='hydro' then 'hydro'
     when "power_source"='wind' then 'wind'
     when "power"='station' or "power"='sub_station'  then 'substation'
     when "power"='transformer' then 'transformer'
     else 'power'
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
  WHERE "power" is not null or power_source is not null
UNION
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange ,
    CASE
     WHEN osm_id<0 THEN 'R' -- Relation
     ELSE 'W'               -- Way
     END AS geomtype,
    ST_Centroid(way) AS geom,
    case
     when "power"='plant' then 'plant'
     when "power"='tower' then 'tower'
     when "power"='pole' then 'pole'
     when "power"='generator' then 'station'
     when "power"='station' or "power"='sub_station'  then 'substation'
     when "power"='transformer' then 'transformer'
     else 'power'
    end as aggtype,
    case
     when "power"='plant' then 'plant'
     when "power"='tower' then 'tower'
     when "power"='pole' then 'pole'
     when "power"='generator' then
        case
         when "generator:source"='nuclear' then 'nuclear'
         when "generator:source"='solar' then 'solar'
         when "generator:source"='gas' or "generator:source"='coal' then 'fossil'
         when "generator:source"='hydro' then 'hydro'
         when "generator:source"='wind' then 'wind'
         else 'station'
        end
     when "power_source"='photovoltaic' then 'solar'
     when "power_source"='hydro' then 'hydro'
     when "power_source"='wind' then 'wind'
     when "power"='station' or "power"='sub_station'  then 'substation'
     when "power"='transformer' then 'transformer'
     else 'power'
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
  WHERE "power" is not null or power_source is not null;
