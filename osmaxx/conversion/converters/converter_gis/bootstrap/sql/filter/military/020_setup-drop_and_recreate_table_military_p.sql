-----------------
--  military_p --
-----------------
DROP TABLE if exists osmaxx.military_p;
CREATE TABLE osmaxx.military_p (
    osm_id bigint,
    lastchange timestamp without time zone,
    geomtype text,
    geom geometry(POINT, 4326),
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
