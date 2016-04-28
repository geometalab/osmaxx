DROP TABLE if exists osmaxx.geoname_l;
DROP TABLE if exists osmaxx.geoname_p;

CREATE TABLE osmaxx.geoname_l (
    osm_id bigint,
    lastchange timestamp without time zone,
    geomtype char(1),
    geom geometry(MULTILINESTRING, 4326),
    type text,
    name text,
    name_en text,
    name_fr text,
    name_es text,
    name_de text,
    int_name text,
    label text,
    tags text,
    population int,
    wikipedia text
);

CREATE TABLE osmaxx.geoname_p (
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
    tags text,
    population int,
    wikipedia text
);
