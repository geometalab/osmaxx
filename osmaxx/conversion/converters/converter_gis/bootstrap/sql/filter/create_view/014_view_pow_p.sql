CREATE OR REPLACE VIEW view_osmaxx.pow_p AS SELECT
    osm_id,
    lastchange,
    geomtype,
    geom,
    aggtype,
    type,
    name,
    label,
    tags,
    website,
    wikipedia,
    phone,
    opening_hours,
    "access"
FROM osmaxx.pow_p;
