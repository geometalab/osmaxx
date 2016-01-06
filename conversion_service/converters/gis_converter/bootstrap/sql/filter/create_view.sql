CREATE OR REPLACE VIEW view_osmaxx.address_p AS SELECT
	osm_id,
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags,
	street,
	housenumber,
	postcode,
	city,
	country
FROM osmaxx.address_p;

CREATE OR REPLACE VIEW view_osmaxx.adminarea_a AS SELECT 
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags
FROM osmaxx.adminarea_a;

CREATE OR REPLACE VIEW view_osmaxx.boundary_l AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags
FROM osmaxx.boundary_l;

CREATE OR REPLACE VIEW view_osmaxx.building_a AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags,
	height
FROM osmaxx.building_a;

CREATE OR REPLACE VIEW view_osmaxx.geoname_l AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags,
	population
FROM osmaxx.geoname_l;

CREATE OR REPLACE VIEW view_osmaxx.geoname_p AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags,
	population
FROM osmaxx.geoname_p;

CREATE OR REPLACE VIEW view_osmaxx.landuse_a AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags
FROM osmaxx.landuse_a;

CREATE OR REPLACE VIEW view_osmaxx.military_a AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags
FROM osmaxx.military_a;

CREATE OR REPLACE VIEW view_osmaxx.military_p AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags
FROM osmaxx.military_p;

CREATE OR REPLACE VIEW view_osmaxx.misc_l AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	aggtype,
	type, 
	name, 
	label,
	tags
FROM osmaxx.misc_l;

CREATE OR REPLACE VIEW view_osmaxx.natural_a AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags
FROM osmaxx.natural_a;

CREATE OR REPLACE VIEW view_osmaxx.natural_p AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags
FROM osmaxx.natural_p;

CREATE OR REPLACE VIEW view_osmaxx.nonop_l AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags,
	ref,
	z_order,
	status
FROM osmaxx.nonop_l;

CREATE OR REPLACE VIEW view_osmaxx.pow_a AS SELECT
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
	contact_phone,
	opening_hours,
	"access"
FROM osmaxx.pow_a;

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
	contact_phone,
	opening_hours,
	"access"
FROM osmaxx.pow_p;

CREATE OR REPLACE VIEW view_osmaxx.poi_a AS SELECT
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
	contact_phone,
	opening_hours,
	cuisine,
	"access",
	brand,
	tower_type
FROM osmaxx.poi_a;

CREATE OR REPLACE VIEW view_osmaxx.poi_p AS SELECT
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
	contact_phone,
	opening_hours,
	cuisine,
	"access",
	brand,
	tower_type
FROM osmaxx.poi_p;

CREATE OR REPLACE VIEW view_osmaxx.railway_l AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	aggtype,
	type, 
	name, 
	label,
	tags,
	z_order,
	bridge,
	tunnel,
	voltage,
	frequency
FROM osmaxx.railway_l;

CREATE OR REPLACE VIEW view_osmaxx.road_l AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	aggtype,
	type, 
	name, 
	label,
	tags,
	ref,
	oneway,
	z_order,
	bridge,
	tunnel
FROM osmaxx.road_l;

CREATE OR REPLACE VIEW view_osmaxx.route_l AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags
FROM osmaxx.route_l;

CREATE OR REPLACE VIEW view_osmaxx.traffic_a AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	aggtype,
	type, 
	name, 
	label,
	tags,
	"access"
FROM osmaxx.traffic_a;

CREATE OR REPLACE VIEW view_osmaxx.traffic_p AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	aggtype,
	type, 
	name, 
	label,
	tags,
	"access"
FROM osmaxx.traffic_p;

CREATE OR REPLACE VIEW view_osmaxx.transport_a AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom,
	aggtype,
	type, 
	name, 
	label,
	tags
FROM osmaxx.transport_a;

CREATE OR REPLACE VIEW view_osmaxx.transport_p AS SELECT 
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	aggtype,
	type, 
	name, 
	label,
	tags
FROM osmaxx.transport_p;


CREATE OR REPLACE VIEW view_osmaxx.utility_a AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom,
	aggtype,
	type, 
	name, 
	label,
	tags
FROM osmaxx.utility_a;

CREATE OR REPLACE VIEW view_osmaxx.utility_p AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom,
	aggtype,
	type, 
	name, 
	label,
	tags
FROM osmaxx.utility_p;

CREATE OR REPLACE VIEW view_osmaxx.utility_l AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags,
	operator,
	voltage,
	frequency
FROM osmaxx.utility_l;


CREATE OR REPLACE VIEW view_osmaxx.water_a AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags
FROM osmaxx.water_a;

CREATE OR REPLACE VIEW view_osmaxx.water_p AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags
FROM osmaxx.water_p;

CREATE OR REPLACE VIEW view_osmaxx.water_l AS SELECT
	osm_id, 
	lastchange, 
	geomtype,
	geom, 
	type, 
	name, 
	label,
	tags,
	width
FROM osmaxx.water_l;
