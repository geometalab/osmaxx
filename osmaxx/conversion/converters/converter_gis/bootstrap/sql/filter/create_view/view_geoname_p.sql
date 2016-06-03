CREATE OR REPLACE VIEW view_osmaxx.geoname_p AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    type,
    name,
    label,
    tags,
    population
FROM osmaxx.geoname_p;
