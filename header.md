# Introduction

## Credits and legal issues

Credits go to OpenSteetMap and to Geofabrik.
This document is licensed under CC-BY-SA.
The data referred to is from OpenStreetMap planet file licensed under ODbL 1.0.

## Goal, scope, and limits

Notes regarding limits, quality and out of scope of the data model and the related datasets.
Goal and scope: Das Osmaxx-Datenmodell ist zur möglichst breiten Nutzung ausgelegt
(Kartendarstellung, Orientierung, POI-Suche und räumliche Analyse und später Routing). D.h. es
wird versucht, so viele Informationen (Tabellen, Attribute und Wertebereiche) wie möglich aus OSM
herauszuholen, die einigermassen konsistent erfasst werden bzw. die sich filtern („Cleansing“ und
Homogenisierung) oder aus den Daten herleiten lassen („Data Curation“). Das ist zwangsläufig
mehr, als beispielsweise für die (gedruckte) Kartendarstellung eines topografischen
Landschaftsmodells nötig ist.
These are known limits, omissions and bugs:

1. Current data export exports POLYGON instead of MULTPOLYGON
2. Statistics is missing
3. Missing tables: coastline_l, adminunit_a
4. tbd.

Tbd.

## Status of this document and future releases

This document and the project just started and thus is in e pre-mature state.

These are possible enhancements in next releases

* File STATISTICS.txt whih contains a report about tables, attributes and it's rows and
  values.
* Final data model (V.3?)
* Adding attribute height to tables like poi_p from external digital terrain model data
      like SRTM3.

## How OSM data is being curated (discussion) ###

Semicolons in tag values:

* Data value will be changed to ‘others’ for such events

Data Cleaning:

* Spelling errors
* Upper case errors
* Values singular and plural
* Handling values which contains words

Elevation: Elevation values will not be set in this release.

Type-'others'. Data value will be change to ‘others’ as it cannot be categorized. This is
introduced to ensure values that are misspelled, concatenated, illegible or user defined are
sorted accordingly into their table. Seeing this type of value given to some feature is due to a
few reasons. 1) Data is not in the list of core value to be considered. 2) Value is being given
by users where we might know understand the value significance.

Grouping of features. unable to group features like airports and power station as buildings are
not defined to specific areas to be able to group them together.

Multiple Table. There are instances where different table can contain the same feature. e.g.
buildings_a and poi_a (like campus areas or school areas) where it can overlap one another. This
have not been resolve, therefore, users do take note of double entry.

'Refer to table'. This is to keep the documentation short and not allowing it to repeat the common attribute value which is similar to other table.

Administrative boundary extracted on the fly and placed into boundary_l table but these are
without warranty to be consistent. There exist other sources with validated boundaries including
country borders and coastlines.

Landcover contains partial landuse elements while some landcover elements are put into natural or
water.

Building addresses are not yet handled due to the complexity of this issue.


# Specification

## Identifiers

The original OSM schema contains an id (type bigint) for every element node,way and relation.
This OSM id is mapped to attribute osm_id (see chapter “Common Attributes”). The id in OSM is not
stable but often the only one, one can work with. During transformation I can happen that thie
osm_id is being changed or duplicated:

* `osm2pgsql` generates areas/polygons out of ways and relations. These objects get negative
  values of the way or the relation.
* `osm2pgsql` splits ways which are too long
* tags can contain many values separated by semicolon (e.g. “shop-a;b”); this object may
  be split into two for each shop-value (“shop-a” and “shop-b”) while the osm_id os
  maintained.

## Metadata

* Datum  (coordinate reference system) of data: WGS84 (EPSG: 4326)
* Character Encoding: UTF-8

## File Names

Base file names are formed according to following template:
osm_tablename_g_vNN (example: osm_building_a_v01.gpkg)
... with following meaning:

* osm_: Prefix
* tablename: A table name from the data model.
* _g: layer geometry type (g is a char out of “p”, “l” or “a”, meaning point, linestring,
  area/polygon)
* vNN: Version of the data model

For some roads and other tables of geometry type (Multi-)Linestring, there will be tables with
generalized geometry, called _gen0, _gen1 as follows (gen- generalized):

* _gen0: smoothed for highest zoom level
* _gen1: simplified
* _gen2: more simplified

example: osm_building_a_gen1_v01.gpkg

## Layer Specification Headers

|Headers                |Description                                                           |
| --------------------- | -------------------------------------------------------------------- |
|Additional Attribute   |This is the addition attribute that is introduce to the table to provide more information on top of the Common Layer Attributes.|
|Values of attributes 'type' |Tells what the database values might contain based on the description of the tables under 3. Layer Overview. It also helps to defined the value meanings to remove unwanted vagueness.|
|Values of attributes 'aggtype' and 'type'   |Same as the above but this table includes the aggregrate values which is to group the 'type' with more specific grouping|

## Common Attributes

These attributes are common to all tables (except maybe tables from external sources).


|Attribute   |Data Type         |Description                                   |Osm Tags       |
| ---------- | ---------------- | -------------------------------------------- | ------------- |
|osm_id|bigint|The ID of the OSM element (node, way or relationship) corresponding to the feature. The uniqueness is only within an OSM element. OSM does not guarantee uniqueness. But it's often the only ID one can get from the origin. `osm2pgsql` generates negative osm_ids when areas are created from relations. And `osm2pgsql` creates sometimes duplicates by splitting large ways.|`osm_id=*`|
|lastchange |timestamp without time zone |The timestamp of the last time the feature was changed (UTC)|`osm_lastchange=*`|
|geomtype|varchar(1)|This will define whether it is a node (“N”), a way (“W”) or a relation (“R”).|(n/a)|
|geom|geometry(geometry, 4326)|The “geometry” of the feature can be POINT, MULTILINESTRING or MULTIPOLYGON|`way=*`|
|type|text(Enum)|This will define the feature type| |
|name|text|The name which is in general use (which means cyrillic, arabic etc.)|`name=*`|
|name_intl|text|The name which is written in english, international|`Coalesce(name:en, int_name, name:fr,name:es,name:de, name)`|
|name_en|text|The name which is written in english|`name:en=*`|
|name_fr|text|The name which is written in french|`name:fr=*`|
|name_es|text|The name which is written in spanish|`name:es=*`|
|name_de|text|The name which is written in german|`name:de=*`|
|name_int|text|The international name of the feature|`int_name=*`|
|label|text|Translated name through transliterated| |
|tags|text|Additional OSM tags in form `"<key>"=>"<value>"`, separated by `, `, e.g. `"network"=>"RMV", "note:de"=>"RB34 ist das Teilstück Stockheim bis Bad Vilbel"` or `"name:ca"=>"Frankfurt del Main", "name:ru"=>"Франкфурт-на-Майне", "de:place"=>"city", "wikidata"=>"Q1794", "short_name"=>"Frankfurt", "name:prefix"=>"Stadt", "de:regionalschluessel"=>"064120000000", "TMC:cid_58:tabcd_1:Class"=>"Area", "TMC:cid_58:tabcd_1:LCLversion"=>"9.00", "TMC:cid_58:tabcd_1:LocationCode"=>"414", "de:amtlicher_gemeindeschluessel"=>"06412000"`| |


## Layer Overview

See file name conventions above about the meaning of “_a” etc.


|Tables        |Geometry Type        |Description                                              |
| ------------ | ------------------- | ------------------------------------------------------- |
|address_p|POINT|Stores a point type of entrances and address information |
|adminarea_a|MULTIPOLYGON|Administrative boundaries range from large groups of nation states right down to small administrative districts and suburbs, with an indication of this size/level of importance.|
|boundary_l|MULTILINESTRING|The boundary is used to mark the borders of areas, mostly political, but possibly also of other administrative area|
|building_a|MULTIPOLYGON|To mark the outline of the area of buildings|
|geoname_l|MULTILINESTRING|The boarder of a settlement which is marked around the node and to mark the specific type of settlement. Eg. City, town, village, etc|
|geoname_p|POINT|It is to mark the centre of a named settlement and the specific type of settlement. Eg. City, town, village, etc|
|landuse_a|MULTIPOLYGON|Landuse describes the human use of land, for example fields and pastures.|
|military_a|MULTIPOLYGON|See military_p|
|military_p|POINT|The military is for buildings and area used by the military.|
|misc_l|MULTILINESTRING|This contains elements could not be categorized into specific tables. E.g barrier and cliffs.|
|natural_a|MULTIPOLYGON|see natural_p|
|natural_p|POINT|Used to describes natural physical land features, including small modification by humans. E.g glacier, volcano, mud, etc.|
|nonop_l|MULTILINESTRING|non-op./planned infrastructure not usable for traffic or transport|
|poi_a|MULTIPOLYGON|Points of interest features of a generic place, like shops, amenities,  leisure, accomondation, pitches etc.|
|poi_p|POINT |Points of interest features of a generic place, like shops, amenities, leisure, accomondation, etc.    |
|pow_a|MULTIPOLYGON|See pow_p|
|pow_p|POINT|This it a place of worship where people of different religion can go. e.g. church, temples(buddist, taoist, etc.), mosque(muslims)|
|railway_l|MULTILINESTRING|All forms of transport using metal rails, including mainline services, subways, heritage lines and trams.|
|road_l|MULTILINESTRING|Any road, route, way, or thoroughfare on land which connects one location to another and has been paved or otherwise improved to allow travel by some conveyance, including motorised vehicles, cyclists, pedestrians, horse, riders, and others|
|route_l|MULTILINESTRING|A route is a customary or regular line of passage or travel, often predetermined and publicized. Routes consist of paths taken repeatedly by people and vehicles.|
|traffic_a|MULTIPOLYGON|See traffic_p|
|traffic_p|POINT|It contains information regarding the rules of the road. Which allow better flow of traffic. E.g. Road signs, traffic calming, etc.|
|transport_a|MULTIPOLYGON|See transport_p|
|transport_p|POINT|Features which mark out points or location where it enable transporting anyone from one place to another. E.g. Bus stops, train station, etc.|
|utility_a|MULTIPOLYGON|See utility_l|
|utility_p|POINT|See utility_l|
|utility_l|MULTILINESTRING|All features which are part of the utility body. E.g. Power structure (powerlines, power building), pipelines (oil, water, gas etc.),  etc..|
|water_a|MULTIPOLYGON|See water_l|
|water_p|POINT|See water_l|
|water_l|MULTILINESTRING|All features which are part of the waterbody. E.g. Dams, river, etc. |


# Layers Specification

