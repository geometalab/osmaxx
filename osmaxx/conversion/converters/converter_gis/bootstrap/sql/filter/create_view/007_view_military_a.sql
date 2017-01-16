CREATE OR REPLACE VIEW view_osmaxx.military_a AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    type,
    name,
    label,
    tags
FROM osmaxx.military_a;
