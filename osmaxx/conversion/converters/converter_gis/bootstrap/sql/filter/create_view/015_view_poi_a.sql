CREATE OR REPLACE VIEW view_osmaxx.poi_a AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    aggtype,
    type,
    name,
    label,
    tags,
    website,
    wikipedia,
    phone,
    opening_hours,
    cuisine,
    "access",
    brand,
    tower_type
FROM osmaxx.poi_a;
