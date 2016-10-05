CREATE OR REPLACE VIEW view_osmaxx.misc_l AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    aggtype,
    "type",
    "name",
    name_en,
    name_fr,
    name_es,
    name_de,
    int_name,
    label,
    tags
FROM osmaxx.misc_l;
