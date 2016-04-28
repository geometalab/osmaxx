-----------------------------
--          poi_a          --
-----------------------------
DROP TABLE if exists osmaxx.poi_a;
CREATE TABLE osmaxx.poi_a(
    osm_id bigint,
    lastchange timestamp without time zone,
    geomtype char(1),
    geom geometry(MULTIPOLYGON, 4326),
    aggtype text,
    type text,
    name text,
    name_en text,
    name_fr text,
    name_es text,
    name_de text,
    int_name text,
    label text,
    tags text,
    website text,
    wikipedia text,
    phone text,
    opening_hours text,
    cuisine text,
    "access" text,
    brand text,
    tower_type text
);
