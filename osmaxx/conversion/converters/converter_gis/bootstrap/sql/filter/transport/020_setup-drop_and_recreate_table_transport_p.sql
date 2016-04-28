-----------------
-- transport_p --
-----------------
DROP TABLE if exists osmaxx.transport_p;
CREATE TABLE osmaxx.transport_p(
    osm_id bigint,
    lastchange timestamp without time zone,
    geomtype text,
    geom geometry(POINT, 4326),
    aggtype text,
    type text,
    name text,
    name_en text,
    name_fr text,
    name_es text,
    name_de text,
    int_name text,
    label text,
    tags text
);
