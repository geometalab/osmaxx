DROP TABLE if exists osmaxx.misc_l;
CREATE TABLE osmaxx.misc_l(
    osm_id bigint,
    lastchange timestamp without time zone,
    geomtype char(1),
    geom geometry(MULTILINESTRING, 4326),
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
