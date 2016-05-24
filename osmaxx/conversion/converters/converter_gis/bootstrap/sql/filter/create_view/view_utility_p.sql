CREATE OR REPLACE VIEW view_osmaxx.utility_p AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    aggtype,
    type,
    name,
    label,
    tags
FROM osmaxx.utility_p;
