CREATE OR REPLACE VIEW view_osmaxx.natural_p AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    type,
    name,
    label,
    tags
FROM osmaxx.natural_p;
