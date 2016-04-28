CREATE OR REPLACE VIEW view_osmaxx.water_p AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    type,
    name,
    label,
    tags
FROM osmaxx.water_p;
