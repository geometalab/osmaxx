CREATE OR REPLACE VIEW view_osmaxx.address_p AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    type,
    name,
    label,
    tags,
    street,
    housenumber,
    postcode,
    city,
    country
FROM osmaxx.address_p;
