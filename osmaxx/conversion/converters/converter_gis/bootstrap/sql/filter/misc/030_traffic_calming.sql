-- traffic_calming --
INSERT INTO osmaxx.misc_l
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange,
    CASE
     WHEN osm_id<0 THEN 'R' -- Relation
     ELSE 'W'               -- Way
     END AS geomtype,
    ST_Multi(way) AS geom,
    'traffic_calming' as aggtype,
-- Combining different tags into traffic_calming tag --
    case
     when traffic_calming in ('hump','bump','table','chicane','cushion') then traffic_calming
     else 'traffic_calming'
    end AS type,
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
  WHERE traffic_calming is not null
UNION
(
  WITH osm_single_polygon AS (
      SELECT osm_id, osm_timestamp, traffic_calming, name, "name:en", "name:fr", "name:es", "name:de", int_name, tags,

      CASE WHEN ST_GeometryType(way) = ANY(array['ST_MultiPolygon', 'ST_Polygon'])
        THEN ST_Boundary(way)
        ELSE way
      END AS way
      FROM osm_polygon
  )
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange,
    CASE
     WHEN osm_id<0 THEN 'R' -- R=Relation
     ELSE 'W'               -- W=Way
     END AS geomtype,
    ST_Multi(way) AS geom,
    'traffic_calming' as aggtype,
-- Combining different tags into traffic_calming tag --
    case
     when traffic_calming in ('hump','bump','table','chicane','cushion') then traffic_calming
     else 'traffic_calming'
    end AS type,

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
  FROM osm_single_polygon
  WHERE traffic_calming is not null
);
