CREATE OR REPLACE VIEW view_osmaxx.water_l AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    type,
    name,
    label,
    tags,
    width
FROM osmaxx.water_l;
