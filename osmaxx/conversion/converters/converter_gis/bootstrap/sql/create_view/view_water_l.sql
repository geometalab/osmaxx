CREATE OR REPLACE VIEW view_osmaxx.water_l AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    "type",
    "name",
    name_en,
    name_fr,
    name_es,
    name_de,
    int_name,
    label,
    tags,
    width
FROM osmaxx.water_l;
