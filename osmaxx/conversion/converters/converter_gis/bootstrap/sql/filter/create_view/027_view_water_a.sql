CREATE OR REPLACE VIEW view_osmaxx.water_a AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    type,
    name,
    label,
    tags
FROM osmaxx.water_a;
