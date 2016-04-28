-----------------
--  address_p  --
-----------------
DROP TABLE if exists osmaxx.address_p;
CREATE TABLE osmaxx.address_p(
    osm_id bigint,
    lastchange timestamp without time zone,
    geomtype char(1),
    geom geometry(POINT, 4326),
    type char(1),
    name text,
    name_en text,
    name_fr text,
    name_es text,
    name_de text,
    int_name text,
    label text,
    tags text,
    street text,
    housenumber text,
    postcode text,
    city text,
    country text
);
