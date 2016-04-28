INSERT INTO osmaxx.pow_a
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange,
    CASE
     WHEN osm_id<0 THEN 'R' -- Relation
     ELSE 'W'               -- Way
     END AS geomtype,
    ST_Multi(way) AS geom,
-- Combining the different tags in Religion --
    case
     when religion in ('buddhist','hindu','jewish','shinto','sikh','taoist','christian','muslim') then religion
     else 'place_of_worship'
    end as aggtype,
    case
     when religion in ('buddhist','hindu','jewish','shinto','sikh','taoist') then religion
     when religion='christian' then
        case
         when denomination in ('anglican','baptist','catholic','evangelical','lutheran','methodist','orthodox','protestant','mormon','presbyterian') then denomination
         else 'christian'
        end
     when religion='muslim' then
        case
         when denomination in ('shia', 'sunni') then denomination
         else 'muslim'
        end
     else 'place_of_worship'
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
    "access" as "access"
  FROM osm_polygon
  WHERE religion is not null or amenity='place_of_worship';
