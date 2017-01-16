CREATE OR REPLACE VIEW view_osmaxx.utility_a AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    aggtype,
    type,
    name,
    label,
    tags
FROM osmaxx.utility_a;
