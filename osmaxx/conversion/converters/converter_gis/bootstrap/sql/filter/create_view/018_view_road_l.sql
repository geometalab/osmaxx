CREATE OR REPLACE VIEW view_osmaxx.road_l AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    aggtype,
    type,
    name,
    label,
    tags,
    ref,
    oneway,
    z_order,
    bridge,
    tunnel
FROM osmaxx.road_l;
