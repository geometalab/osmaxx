CREATE OR REPLACE VIEW view_osmaxx.geoname_p AS SELECT
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
    population
FROM osmaxx.geoname_p;
