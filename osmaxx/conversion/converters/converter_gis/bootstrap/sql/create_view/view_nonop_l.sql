CREATE OR REPLACE VIEW view_osmaxx.nonop_l AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    "type",
    sub_type,
    "name",
    name_en,
    name_fr,
    name_es,
    name_de,
    int_name,
    label,
    tags,
    ref,
    z_order,
    status
FROM osmaxx.nonop_l;
