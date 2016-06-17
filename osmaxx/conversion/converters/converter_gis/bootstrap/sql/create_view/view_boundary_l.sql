CREATE OR REPLACE VIEW view_osmaxx.boundary_l AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    type,
    name,
    label,
    tags
FROM osmaxx.boundary_l;
