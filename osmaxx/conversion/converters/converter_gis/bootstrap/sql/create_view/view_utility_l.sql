CREATE OR REPLACE VIEW view_osmaxx.utility_l AS SELECT
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
    operator,
    voltage,
    frequency
FROM osmaxx.utility_l;
