CREATE OR REPLACE VIEW view_osmaxx.utility_l AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    type,
    name,
    label,
    tags,
    operator,
    voltage,
    frequency
FROM osmaxx.utility_l;
