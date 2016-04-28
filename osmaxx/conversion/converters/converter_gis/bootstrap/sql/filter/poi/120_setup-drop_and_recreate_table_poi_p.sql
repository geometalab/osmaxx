-----------------------------
--          poi_p          --
-----------------------------
DROP TABLE if exists osmaxx.poi_p;
CREATE TABLE osmaxx.poi_p(
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
