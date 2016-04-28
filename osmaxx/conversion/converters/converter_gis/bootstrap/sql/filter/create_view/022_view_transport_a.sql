CREATE OR REPLACE VIEW view_osmaxx.transport_a AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    aggtype,
    type,
    name,
    label,
    tags
FROM osmaxx.transport_a;
