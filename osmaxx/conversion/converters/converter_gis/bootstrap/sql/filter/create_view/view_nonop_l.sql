CREATE OR REPLACE VIEW view_osmaxx.nonop_l AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    type,
    sub_type,
    name,
    label,
    tags,
    ref,
    z_order,
    status
FROM osmaxx.nonop_l;
