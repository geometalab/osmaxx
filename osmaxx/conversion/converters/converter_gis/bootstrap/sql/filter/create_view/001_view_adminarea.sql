CREATE OR REPLACE VIEW view_osmaxx.adminarea_a AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    type,
    name,
    label,
    tags
FROM osmaxx.adminarea_a;
