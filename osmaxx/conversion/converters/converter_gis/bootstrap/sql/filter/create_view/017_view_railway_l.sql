CREATE OR REPLACE VIEW view_osmaxx.railway_l AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    aggtype,
    type,
    name,
    label,
    tags,
    z_order,
    bridge,
    tunnel,
    voltage,
    frequency
FROM osmaxx.railway_l;
