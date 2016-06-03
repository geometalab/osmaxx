CREATE OR REPLACE VIEW view_osmaxx.natural_a AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    type,
    name,
    label,
    tags
FROM osmaxx.natural_a;
