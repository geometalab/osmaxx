CREATE OR REPLACE VIEW view_osmaxx.landuse_a AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    type,
    name,
    label,
    tags
FROM osmaxx.landuse_a;
