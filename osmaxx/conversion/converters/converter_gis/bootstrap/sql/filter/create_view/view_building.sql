CREATE OR REPLACE VIEW view_osmaxx.building_a AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    type,
    name,
    label,
    tags,
    height
FROM osmaxx.building_a;
