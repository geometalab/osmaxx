CREATE OR REPLACE VIEW view_osmaxx.misc_l AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    aggtype,
    type,
    name,
    label,
    tags
FROM osmaxx.misc_l;
