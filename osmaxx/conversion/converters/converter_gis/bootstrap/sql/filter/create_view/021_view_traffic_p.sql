CREATE OR REPLACE VIEW view_osmaxx.traffic_p AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    aggtype,
    type,
    name,
    label,
    tags,
    "access"
FROM osmaxx.traffic_p;
