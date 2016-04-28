-----------------
--  building_a --
-----------------
DROP TABLE if exists osmaxx.building_a;
CREATE TABLE osmaxx.building_a (
    osm_id bigint,
    lastchange timestamp without time zone,
    geomtype char(1),
    geom geometry(MULTIPOLYGON, 4326),
    type text,
    name text,
    name_en text,
    name_fr text,
    name_es text,
    name_de text,
    int_name text,
    label text,
    tags text,
    height float
);
