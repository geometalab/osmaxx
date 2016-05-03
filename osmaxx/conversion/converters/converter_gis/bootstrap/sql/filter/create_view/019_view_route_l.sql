CREATE OR REPLACE VIEW view_osmaxx.route_l AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    type,
    name,
    label,
    tags
FROM osmaxx.route_l;
