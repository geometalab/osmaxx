-----------------
---  nonop_l  ---
-----------------
-- Planned Infrastructure not usable for Traffic  or transport --
DROP TABLE if exists osmaxx.nonop_l;
CREATE TABLE osmaxx.nonop_l (
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
    ref text,
    bridge boolean,
    tunnel boolean,
    z_order smallint,
    status text
);
