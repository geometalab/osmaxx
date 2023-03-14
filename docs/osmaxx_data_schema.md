# Introduction

## Credits and legal issues

Credits go to OpenSteetMap and to Geofabrik.
This document is licensed under CC-BY-SA.
The data referred to is from OpenStreetMap planet file licensed under ODbL 1.0.

## Goal, scope, and limits

The OSMaxx extracts are designed for broad usage.
This goes beyond the transformations usually necessary to create a
topological map.

There are known limits, omissions and bugs, which are being tracked
in the GitHub-repository https://github.com/geometalab/osmaxx/issues. 

## Status of this document and future releases

This document and the project just started and thus is in e pre-mature state.

These are possible enhancements in next releases:

* File STATISTICS.txt which contains a report about tables, attributes and it's rows and
  values.
* Final data model (V.3?)
* Adding attribute height to tables like poi_p from external digital terrain model data
      like SRTM3.

## How OSM data is being curated (discussion)

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
generalized geometry, called `_gen0`, `_gen1` as follows (gen- generalized):

* `_gen0`: smoothed for highest zoom level
* `_gen1`: simplified
* `_gen2`: more simplified

example: `osm_building_a_gen1_v01.gpkg`

## Layer Specification Headers

|Headers                |Description                                                           |
| --------------------- | -------------------------------------------------------------------- |
|Additional Attribute   |This is the addition attribute that is introduce to the table to provide more information on top of the Common Layer Attributes.|
|Values of attributes 'type' |Tells what the database values might contain based on the description of the tables under 3. Layer Overview. It also helps to defined the value meanings to remove unwanted vagueness.|
|Values of attributes 'aggtype' and 'type'   |Same as the above but this table includes the aggregrate values which is to group the 'type' with more specific grouping|

## Common Attributes

These attributes are common to all tables except the ones derived from OSM costline data processed by openstreetmapdata.com.


|Attribute   |Data Type         |Description                                   |Osm Tags       |osm2pgsql column |
| ---------- | ---------------- | -------------------------------------------- | ------------- | --------------- |
|osm_id|bigint|The ID of the OSM element (node, way or relationship) corresponding to the feature. The uniqueness is only within an OSM element. OSM does not guarantee uniqueness. But it's often the only ID one can get from the origin. `osm2pgsql` generates negative osm_ids when areas are created from relations. And `osm2pgsql` creates sometimes duplicates by splitting large ways.| |`osm_id`|
|lastchange |timestamp without time zone |The timestamp of the last time the feature was changed (UTC)|`osm_lastchange=*`| |
|geomtype|varchar(1)|This will define whether it is a node (“N”), a way (“W”) or a relation (“R”).|(n/a)| |
|geom|geometry(geometry, 4326)|The “geometry” of the feature can be POINT, MULTILINESTRING or MULTIPOLYGON| |`way`|
|type|text(Enum)|This will define the feature type| |
|name|text|The feature's (locally or regionally) common default name i.e. the one usually displayed on street signs. May be in a non-Latin script (cyrillic, arabic etc.)|`name=*`| |
|name_en|text|The feature's English name|`name:en=*`| |
|name_fr|text|The feature's French name|`name:fr=*`| |
|name_es|text|The feature's Spanish name|`name:es=*`| |
|name_de|text|The feature's German name|`name:de=*`| |
|name_int|text|The international name of the feature|`int_name=*`| |
|label|text|A name of the feature readable by those only knowing Latin script. See [below](#attribute-label) for details.| | |
|tags|text|Additional OSM tags in form `"<key>"=>"<value>"`, separated by `, `, e.g. `"network"=>"RMV", "note:de"=>"RB34 ist das Teilstück Stockheim bis Bad Vilbel"` or `"name:ca"=>"Frankfurt del Main", "name:ru"=>"Франкфурт-на-Майне", "de:place"=>"city", "wikidata"=>"Q1794", "short_name"=>"Frankfurt", "name:prefix"=>"Stadt", "de:regionalschluessel"=>"064120000000", "TMC:cid_58:tabcd_1:Class"=>"Area", "TMC:cid_58:tabcd_1:LCLversion"=>"9.00", "TMC:cid_58:tabcd_1:LocationCode"=>"414", "de:amtlicher_gemeindeschluessel"=>"06412000"`| |`tags`|


### Attribute `label`

The intended audience of a map you create from OSMaxx data
might not (only) be the regional population in or near the mapped area.
A feature's or place's common name might thus be in a script
that is hard to (re-)recognize and remember, let alone pronounce
by members of your audience.
As a convenience when producing maps for non-local audiences,
OSMaxx provides a feature name suitable for such audiences
(under the assumption that they do know Latin script)
in the attribute `label`
according to the following logic:

1. The feature's common name (OSM tag `name=*`) is used if it already is is in Latin script.
2. Else, the feature's English, French, Spanish or German name (in this precedence) is used,
   if known to OSM (tag `name:<language>=*`).
3. Else, the feature's international name (tag `int_name`) is transliterated to Latin and the result is used,
   if the international name is known to OSM.
4. Else, the feature's common name (`name=*`) is transliterated to Latin and the result is used.

Note that a transliteration is not a transcription. In contrast to a transcription it

* doesn't generally give the right idea about the name's correct pronunciation.
* might contain non-pronunciation-related diacritics and punctuation
  that allows for lossless back-transliteration to the origianl script.

## Layer Overview

See file name conventions above about the meaning of “_a” etc.


|Tables        |Geometry Type        |Description                                              |
| ------------ | ------------------- | ------------------------------------------------------- |
|address_p|POINT|Stores a point type of entrances and address information|
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
|poi_a|MULTIPOLYGON|Points of interest features of a generic place, like shops, amenities, leisure, accomondation, pitches etc.|
|poi_p|POINT|Points of interest features of a generic place, like shops, amenities, leisure, accomondation, etc.|
|pow_a|MULTIPOLYGON|See pow_p|
|pow_p|POINT|This it a place of worship where people of different religion can go. e.g. church, temples(buddist, taoist, etc.), mosque(muslims)|
|railway_l|MULTILINESTRING|All forms of transport using metal rails, including mainline services, subways, heritage lines and trams.|
|road_l|MULTILINESTRING|Any road, route, way, or thoroughfare on land which connects one location to another and has been paved or otherwise improved to allow travel by some conveyance, including motorised vehicles, cyclists, pedestrians, horse, riders, and others|
|route_l|MULTILINESTRING|A route is a customary or regular line of passage or travel, often predetermined and publicized. Routes consist of paths taken repeatedly by people and vehicles.|
|traffic_a|MULTIPOLYGON|See traffic_p|
|traffic_p|POINT|It contains information regarding the rules of the road. Which allow better flow of traffic. E.g. Road signs, traffic calming, etc.|
|transport_a|MULTIPOLYGON|See transport_p|
|transport_l|MULTILINESTRING|Linear features involved in transporting anyone from one place to another, e.g. runways at airports|
|transport_p|POINT|Features which mark out points or location where it enable transporting anyone from one place to another. E.g. Bus stops, train station, etc.|
|utility_a|MULTIPOLYGON|See utility_l|
|utility_l|MULTILINESTRING|All features which are part of the utility body. E.g. Power structure (powerlines, power building), pipelines (oil, water, gas etc.), etc..|
|utility_p|POINT|See utility_l|
|water_a|MULTIPOLYGON|See water_l|
|water_l|MULTILINESTRING|All features which are part of the waterbody. E.g. Dams, river, etc.|
|water_p|POINT|See water_l|
|landmass_a|MULTIPOLYGON|All land areas in the excerpt, i.e. continents and islands.|
|coastline_l|MULTILINESTRING|Linestrings for coastlines. Long linestrings are split into smaller chunks (with no more than 100 points) that are easier and faster to work with.|
|sea_a|MULTIPOLYGON|Oceans, seas and large bodies of inland water. Polygons are split into smaller overlapping chunks that are easier and faster to work with.|


# Layers Specification

## address_p


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|type|text|(see table below)| |
|street|text| |`addr:street=*` or `addr:place=*`|
|housenumber|text| |`addr:housenumber=*` or `addr:interpolation=even`+`addr:housenumber=*` or `addr:interpolation=odd`+`addr:housenumber=*` or `addr:interpolation=all`+`addr:housenumber=*`|
|postcode|text| |`addr:postcode=*`|
|city|text| |`addr:city=*`|
|country|text| |`addr:country=*`|


Values of attribute type

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|i|`addr:interpolation=even` or `addr:interpolation=odd` or `addr:interpolation=all`|Interpolated Entrances along interpolated addresses without nodes|
|e|`building=entrance`+`addr:street=*` or `building=entrance`+`addr:housenumber=*` or `building=entrance`+`addr:place=*` or `entrance=*`+`addr:street=*` or `entrance=*`+`addr:housenumber=*` or `entrance=*`+`addr:place=*`|General Entrance with entrance node|
|b|`addr:street=*`+`building=*`+**`building≠entrance`**+**`entrance≠*`** or `addr:housenumber=*`+`building=*`+**`building≠entrance`**+**`entrance≠*`** or `addr:place=*`+`building=*`+**`building≠entrance`**+**`entrance≠*`**|Entrance to a building without entrance node|
|p|`addr:street=*`+**`building≠*`**+**`entrance≠*`** or `addr:housenumber=*`+**`building≠*`**+**`entrance≠*`** or `addr:place=*`+**`building≠*`**+**`entrance≠*`**|All other address nodes|


## adminarea_a


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|type|text|(see table below)| |


Values of attribute type

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|admin_level1|`admin_level=1`+`boundary=administrative`|Efnahags-loegsaga(Exclusive Economic Zone) use in Iceland|
|national|`admin_level=2`+`boundary=administrative`|National border of a country which is listed based on ISO 3166 standard.(Note: Some dependent territories and special areas of geographical interest which do have their own ISO 3166-1 code but aren't a country).|
|admin_level3|`admin_level=3`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level4|`admin_level=4`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level5|`admin_level=5`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level6|`admin_level=6`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level7|`admin_level=7`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level8|`admin_level=8`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level9|`admin_level=9`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level10|`admin_level=10`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level11|`admin_level=11`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|administrative|`admin_level=*`|All empty or User input admin_level values to be placed under|
|national_park|`boundary=national_park`|A national park is a relatively large area of land declared by a government, to be set aside for human recreation and enjoyment, animal and environmental protection.|
|protected_area|`boundary=protected_area`|Protected areas, such as for national-parks, water protection areas or indigenous areas.|


## boundary_l


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|type|text|(see table below)| |


Values of attribute type

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|admin_level1|`admin_level=1`+`boundary=administrative`|Efnahags-loegsaga(Exclusive Economic Zone) use in Iceland|
|national|`admin_level=2`+`boundary=administrative`|National border of a country which is listed based on ISO 3166 standard.(Note: Some dependent territories and special areas of geographical interest which do have their own ISO 3166-1 code but aren't a country).|
|admin_level3|`admin_level=3`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level4|`admin_level=4`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level5|`admin_level=5`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level6|`admin_level=6`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level7|`admin_level=7`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level8|`admin_level=8`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level9|`admin_level=9`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level10|`admin_level=10`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level11|`admin_level=11`+`boundary=administrative`|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|administrative|`admin_level=*`|All empty or User input admin_level values to be placed under|
|national_park|`boundary=national_park`|A national park is a relatively large area of land declared by a government, to be set aside for human recreation and enjoyment, animal and environmental protection.|
|protected_area|`boundary=protected_area`|Protected areas, such as for national-parks, water protection areas or indigenous areas.|


## building_a


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|height|text|Stores the height of the building (Unit Meters)|`height=*`|
|type|text|(see table below)| |


Values of attribute type

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|building|`building=*`|This marks out the size and area of a building.|


## geoname_l


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|population|int|A rough number of citizens in a given place|`population=*`|
|type|text|(see table below)| |
|wikipedia|text|Provide a reference to an article in Wikipedia about the feature|`wikipedia=*`|


Values of attribute type

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|city|`place=city`|The largest urban settlement or settlements within the territory.|
|county|`place=county`|a territorial division of some countries, forming the chief unit of local administration.|
|farm|`place=farm`|A farm can be a part of a human settlement|
|hamlet|`place=hamlet`|A settlement with less than 100-200 inhabitants.|
|island|`place=island`|An island is any piece of land that is completely surrounded by water and isolated from other significant landmasses.|
|islet|`place=islet`|A very small island.|
|isolated_dwelling|`place=isolated_dweilling`|The smallest kind of settlement (1-2 households)|
|locality|`place=locality`|A named place that has no population|
|municipality|`place=municipality`|a town or district that has local government.|
|named_place|`area=yes`+`name=*`|A place where is given a name with a given area but no specific type|
|neighbourhood|`place=neighbourhood`|A neighbourhood is a smaller named, geographically localised place within a suburb of a larger city or within a town or village|
|place|`place=*`|Any other place type that are not sorted to any type above except for area without name.|
|region|`place=region`|an area, especially part of a country or the world having definable characteristics but not always fixed boundaries.|
|state|`place=state`|A large sub-national political/administrative area.|
|suburb|`place=suburb`|A part of a town or city with a well-known name and often a distinct identity.|
|town|`place=town`|An important urban centre between a village and a city in size|
|village|`place=village`|A settlement with between 1,000 and 10,000 inhabitants.|


## geoname_p


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|population|int|A rough number of citizens in a given place|`population=*`|
|type|text|(see table below)| |
|wikipedia|text|Provide a reference to an article in Wikipedia about the feature|`wikipedia=*`|


Values of attribute type

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|city|`place=city`|The largest urban settlement or settlements within the territory.|
|county|`place=county`|a territorial division of some countries, forming the chief unit of local administration.|
|farm|`place=farm`|A farm can be a part of a human settlement|
|hamlet|`place=hamlet`|A settlement with less than 100-200 inhabitants.|
|island|`place=island`|An island is any piece of land that is completely surrounded by water and isolated from other significant landmasses.|
|islet|`place=islet`|A very small island.|
|isolated_dwelling|`place=isolated_dweilling`|The smallest kind of settlement (1-2 households)|
|locality|`place=locality`|A named place that has no population|
|municipality|`place=municipality`|a town or district that has local government.|
|named_place|`area=yes`+`name=*`|A place where is given a name with a given area but no specific type|
|neighbourhood|`place=neighbourhood`|A neighbourhood is a smaller named, geographically localised place within a suburb of a larger city or within a town or village|
|place|`place=*`|Any other place type that are not sorted to any type above except for area without name.|
|region|`place=region`|an area, especially part of a country or the world having definable characteristics but not always fixed boundaries.|
|state|`place=state`|A large sub-national political/administrative area.|
|suburb|`place=suburb`|A part of a town or city with a well-known name and often a distinct identity.|
|town|`place=town`|An important urban centre between a village and a city in size|
|village|`place=village`|A settlement with between 1,000 and 10,000 inhabitants.|


## landuse_a


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|type| |(see table below)| |


Values of attribute type

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|allotments|`landuse=allotments`|A piece of land given over to local residents for growing vegetables and flowers.|
|basin|`landuse=basin`|An area of water that drains into a river.|
|commercial|`landuse=commercial`|Predominantly offices, business parks, etc.|
|farm|`landuse=farm` or `landuse=farmland`|An area of farmland used for tillage and pasture (animals, crops, vegetables, flowers, fruit growing).|
|farmyard|`landuse=farmyard`|An area of land with farm buildings like farmhouse, dwellings, farmsteads, sheds, stables, barns, equipment sheds, feed bunkers, etc. Plus the open space in between them and the shrubbery/trees around them.|
|fishfarm|`landuse=fishfarm`|A place where fishes are breeded.|
|forest|`landuse=forest`|Managed forest or woodland plantation|
|grass|`landuse=grass`|For areas covered with grass.|
|greenhouse|`landuse=greenhouse_horticulture`|Area used for growing plants in greenhouses|
|industrial|`landuse=industrial`|Predominantly workshops, factories or warehouses|
|landfill|`landuse=landfill`|Where waste is collected, sorted or covered over|
|landuse|`landuse=*`|Get all landuse that is not classified in any table|
|meadow|`landuse=forest`|An area of land primarily vegetated by grass and other non-woody plants, usually mowed for making hay|
|military|`landuse=military`|For land areas owned/used by the military for whatever purpose|
|nature_reserve|`landuse=nature_reserve`|Protected area of importance for wildlife, flora, fauna or features of geological or other special interest.|
|orchard|`landuse=orchard`|Intentional planting of trees or shrubs maintained for food production|
|park|`leisure=park` or `landuse=village_green`|An open, green area for recreation, usually municipal|
|plant_nursery|`landuse=plant_nursery`|Intentional planting of plants maintaining for the production of new plants|
|port|`landuse=port`|Port area handling commercial traffic|
|quarry|`landuse=quarry`|Surface mineral extraction|
|railway|`landuse=railway`|for marshalling yards and sidings, railway sheds, bits of grass with old rails and hardware strewn around, train washes, etc...|
|recreation_ground|`leisure=recreation_ground` or `landuse=recreation_ground`|An open green space for general recreation, which may include pitches, nets and so on, usually municipal but possibly also private to colleges or companies|
|reservoir|`landuse=reservoir`|Man made body of stored water. May be covered or uncovered.|
|residential|`landuse=residential`|Predominantly houses or apartment buildings|
|retail|`landuse=retail`|Predominantly shops|
|vineyard|`landuse=vineyard`|A piece of land where grapes are grown.|


## military_a


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|type|text|(see table below)| |


Values of attribute type

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|airfield|`military=airfield`|A place where military planes take off and land.|
|barracks|`military=barracks`|Buildings where soldiers live and work.|
|bunker|`military=bunker`|Buildings, often build from concrete, to stand even heavier fire. This includes WW2 pillboxes.|
|checkpoint|`military=checkpoint`|Place of a possible access to a restricted or secured area, where civilian visitors and vehicles will be controled by a military authority.|
|danger_area|`military=danger_area`|Usually a large marked area around something like a firing range, bombing range, etc which can be an exclusion zone.|
|military|`military=*`|Any other military type that are not sorted to any type above|
|naval_base|`military=naval_base`|A naval base|
|nuclear_site|`military=nuclear_explosion_site`|Nuclear weapons test site|
|obstacle_course|`military=obstacle_course`|A military obstacle course.|
|range|`military=range`|Where soldiers practice with their weapons (firing, bombing, artillery).|
|training_area|`military=training_area`|An area where soldiers train and weapons or other military technology are experimented with or are tested.|


## military_p


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|type|text|(see table below)| |


Values of attribute type

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|airfield|`military=airfield`|A place where military planes take off and land.|
|barracks|`military=barracks`|Buildings where soldiers live and work.|
|bunker|`military=bunker`|Buildings, often build from concrete, to stand even heavier fire. This includes WW2 pillboxes.|
|checkpoint|`military=checkpoint`|Place of a possible access to a restricted or secured area, where civilian visitors and vehicles will be controled by a military authority.|
|danger_area|`military=danger_area`|Usually a large marked area around something like a firing range, bombing range, etc which can be an exclusion zone.|
|military|`military=*`|Any other military type that are not sorted to any type above|
|naval_base|`military=naval_base`|A naval base|
|nuclear_site|`military=nuclear_explosion_site`|Nuclear weapons test site|
|obstacle_course|`military=obstacle_course`|A military obstacle course.|
|range|`military=range`|Where soldiers practice with their weapons (firing, bombing, artillery).|
|training_area|`military=training_area`|An area where soldiers train and weapons or other military technology are experimented with or are tested.|


## misc_l


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|type|text|(see table below)| |


Values of attribute type

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|barrier|barrier|`barrier=*`|A barrier is a physical structure which blocks or impedes movement. This contains any other barrier except the specifics below.|
|barrier|gate|`barrier=gate`|An entrance that can be opened or closed to get through the barrier.|
|barrier|city_wall|`barrier=city_wall`|A fortification used to defend a city or settlement from potential aggressors. From ancient to modern times, they are used to enclose settlements|
|barrier|hedge|`barrier=hedge`|A line of closely spaced shrubs and bushes, planted and trained in such a way as to form a barrier or to mark the boundary of an area.|
|barrier|fence|`barrier=fence`|A structure supported by posts driven into the ground and designed to prevent movement across a boundary. It is distinguished from a wall by the lightness of its construction.|
|barrier|retaining_wall|`barrier=retaining_wall`|Retaining walls serve to retain the lateral pressure of soil. Right side is bottom, left side is top.|
|barrier|wall|`barrier=wall`|A freestanding solid structure designed to restrict or prevent movement across a boundary. Usually made from solid brick, concrete or stone and almost always built so that it is opaque to vision.|
|barrier|avalanche_protection|`barrier=avalanche_protection`|A variety of linear structures which are placed on steep slopes to hold snow in place.|
|natural|cliff|`natural=cliff`|A vertical or almost vertical natural drop in terrain, usually with a bare rock surface.|
|traffic_calming|traffic_calming|`traffic_calming=*`|Describes features used to slow down traffic. This will contain any other traffic calming except the specifics below.|
|traffic_calming|hump|`traffic_calming=hump`|Similar to a bump, but longer - total length usually 2-4 m (in direction of travel)|
|traffic_calming|bump|`traffic_calming=bump`|Short bump - length (in direction of travel) about 30 cm or shorter. Spans the entire width of the road, but can have cuts and small gaps left and right for cyclists.|
|traffic_calming|table|`traffic_calming=table`|Designed as a long speed hump with a flat section in the middle. The flat section is long enough for all wheels of a passenger car to fit on that section simultaneously. Does not slow as much as a hump and is usually used on roads with residential speed limit. It is known as flat top hump or raised pedestrian crossing.|
|traffic_calming|chicane|`traffic_calming=chicane`|Hazards on the street you have to drive round|
|traffic_calming|cushion|`traffic_calming=cushion`|A hump with spaces between or several multiple rectangular humps aligned across the road. This allows emergency vehicles, buses (due to their wider axle) and bicycles to pass through without slowing down.|


## natural_a


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|type|text|(see table below)| |


Values of attribute type

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|bare_rock|`natural=bare_rock`|An area with sparse or no vegetation, so that the bedrock becomes visible. NOTE: Will appear only on natural_p but not natural_a|
|beach|`natural=beach`|Area of shore which is fairly open, slopes smoothly to the water, and is free of trees|
|cave_entrance|`natural=cave_entrance`|The entrance to a cave|
|fell|`natural=fell`|Bare upper lying uncultivated land principally covered with grass and often grazed.|
|glacier|`natural=glacier`|A permanent body of ice formed naturally from snow that is moving under its own weight.|
|grassland|`natural=grassland`|Where vegetation is dominated by grasses (Poaceae) and other herbaceous (non-woody) plants, except for ornamental grass, mowing for hay, etc. and grazing.|
|heath|`natural=heath`|A dwarf-shrub habitat, characterised by open, low growing woody vegetation, often dominated by plants of the Ericaceae.|
|moor|`natural=moor`|Upland areas, characterised by low-growing vegetation on acidic soils.|
|mud|`natural=mud`|Large area covered with mud|
|natural|`natural=*`|Any other natural type that are not sorted to any type above|
|sand|`natural=sand`|Ground coverage of mostly silica particles, with no or very sparse vegetation.|
|scree|`natural=scree`|Unconsolidated angular rocks formed by rockfall and weathering from adjacent rockfaces.|
|scrub|`natural=scrub` or `landuse=scrub`|Uncultivated land covered with bushes or stunted trees.|
|sinkhole|`natural=sinkhole`|A natural depression or hole in the surface topography.|
|stone|`natural=stone`|Freestanding stone; e.g., glacial erratic.|
|wetland|`natural=wetland`|The wetland tag is used for natural areas subject to inundation or with waterlogged ground|
|wood|`natural=wood`|Used for ancient or virgin woodland, with no forestry use.|


## natural_p


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|type|text|(see table below)| |


Values of attribute type

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|bare_rock|`natural=bare_rock`|An area with sparse or no vegetation, so that the bedrock becomes visible. NOTE: Will appear only on natural_p but not natural_a|
|beach|`natural=beach`|Area of shore which is fairly open, slopes smoothly to the water, and is free of trees|
|cave_entrance|`natural=cave_entrance`|The entrance to a cave|
|fell|`natural=fell`|Bare upper lying uncultivated land principally covered with grass and often grazed.|
|glacier|`natural=glacier`|A permanent body of ice formed naturally from snow that is moving under its own weight.|
|grassland|`natural=grassland`|Where vegetation is dominated by grasses (Poaceae) and other herbaceous (non-woody) plants, except for ornamental grass, mowing for hay, etc. and grazing.|
|heath|`natural=heath`|A dwarf-shrub habitat, characterised by open, low growing woody vegetation, often dominated by plants of the Ericaceae.|
|moor|`natural=moor`|Upland areas, characterised by low-growing vegetation on acidic soils.|
|mud|`natural=mud`|Large area covered with mud|
|natural|`natural=*`|Any other natural type that are not sorted to any type above|
|sand|`natural=sand`|Ground coverage of mostly silica particles, with no or very sparse vegetation.|
|scree|`natural=scree`|Unconsolidated angular rocks formed by rockfall and weathering from adjacent rockfaces.|
|scrub|`natural=scrub` or `landuse=scrub`|Uncultivated land covered with bushes or stunted trees.|
|sinkhole|`natural=sinkhole`|A natural depression or hole in the surface topography.|
|stone|`natural=stone`|Freestanding stone; e.g., glacial erratic.|
|wetland|`natural=wetland`|The wetland tag is used for natural areas subject to inundation or with waterlogged ground|
|wood|`natural=wood`|Used for ancient or virgin woodland, with no forestry use.|


## nonop_l


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|ref|text|Reference number of this road unset for railways.|`ref=*`|
|status|text|(see table below)| |
|sub_type|text|See attribute 'type' of layer road_l and railway_l, respectively.|`highway=proposed`+`proposed=*` or `highway=planned`+`planned=*` or `highway=construction`+`construction=*` or `highway=disused`+`disused=*` or `highway=abandoned`+`abandoned=*` or `railway=proposed`+`proposed=*` or `railway=planned`+`planned=*` or `railway=construction`+`construction=*` or `railway=disused`+`disused=*` or `railway=abandoned`+`abandoned=*`|
|type|text|(see table below)| |
|z_order|smallint|The layer tag is used to describe vertical relationships between different crossing or overlapping map features. Use this in combination with bridge/tunnel tags when one way passes above or under another one.|`layer=*`|


Values of attribute status

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|P|`highway=proposed` or `railway=proposed` or `highway=planned` or `railway=planned`| |
|C|`highway=construction` or `railway=construction`| |
|D|`highway=disused` or `railway=disused`| |
|A|`highway=abandoned` or `railway=abandoned`| |



Values of attribute type

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|highway|`highway=proposed` or `highway=planned` or `highway=construction` or `highway=disused` or `highway=abandoned`|Contains roads which are disused, planned, under constructions or abandoned. These type of features will be place in this table to keep the feature but display as not available|
|railway|`railway=proposed` or `railway=planned` or `railway=construction` or `railway=disused` or `railway=abandoned`|Contains railways which are disused, planned, under constructions or abandoned. These type of features will be place in this table to keep the feature but display as not available|


## poi_a


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|access|text|The legal accessibility of a element.|`access=*`|
|aggtype|text|Groups (aggregates) several different 'type' values to a common supertype, for a coarser, more general caterorization.| |
|brand|text|The identity of a specific product, service, or business. Often trademarks|`brand=*`|
|cuisine|text|The type of food served at an eating place.|`cuisine=*`|
|opening_hours|text|The timing of when something is open or close|`opening_hours=*`|
|phone|text|A telephone number associated with the object.|`phone=*` or `contact:phone=*`|
|tower_type|text|The type of tower|`tower:type=*`|
|type|text|(see table below)| |
|website|text|Specifying the link to the official website for a feature.|`website=*`|
|wikipedia|text|Provide a reference to an article in Wikipedia about the feature.|`wikipedia=*`|


Values of attribute type

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|accommodation_out|alpine_hut|`tourism=alpine_hut`|a mountain hut is a remote building positioned in the mountains designed to provided lodging accommodation for mountaineers, climbers and hikers. The access is usually restricted to foot, mountain bike or ski.|
|amenity|amenity|`amenity=*`|All other types of amenity which is not defined as above|
|destination|archaeological_site|`historic=archaeological_site`|A place in which evidence of past activity is preserved|
|public|arts_centre|`amenity=arts_centre`|A venue where a variety of arts are performed or conducted|
|destination|artwork|`tourism=artwork`|Used to tag public pieces of art. Usually such artwork are outdoors.|
|money|atm|`amenity=atm`|A device that provides the clients of a financial institution with access to financial transactions.|
|destination|attraction|`tourism=attraction`|A general place of interest for visitors. Typically used for its natural or historical significance.|
|shop|bakery|`shop=bakery`|Shop focused on selling bread|
|money|bank|`amenity=bank`|Shows the location of a bank branch.|
|catering|bar|`amenity=bar`|Bar is a purpose-built commercial establishment that sells alcoholic drinks to be consumed on the premises. They are characterised by a noisy and vibrant atmosphere, similar to a party and usually don't sell food.|
|destination|battlefield|`historic=battlefield`|The site of a battle or military skirmish in the past. This could be on land or at sea.|
|shop|beauty|`shop=beauty`|A non-hairdresser beauty shop, spa, nail salon, etc..|
|miscpoi|bench|`amenity=bench`|A bench to sit down and relax a bit|
|shop|beverages|`shop=beverages` or `shop=alcohol`|Shop focused on selling alcoholic and non-alcoholic beverages.|
|shop|bicycle|`shop=bicycle`|Shop focused on selling bicycles, bicycle equipment and may rent or repair them|
|shop|bicycle_rental|`amenity=bicycle_rental`|A place to rent a bicycle|
|catering|biergarten|`amenity=biergarten`|Biergarten or beer garden is an open-air area where alcoholic beverages along with food is prepared and served.|
|tourism|board|`information=board`+`tourism=information`|A board with information|
|shop|books|`shop=books`|Shop focused on selling books|
|shop|butcher|`shop=butcher`|Shop focused on selling meat|
|catering|cafe|`amenity=cafe`|Generally informal place with sit-down facilities selling beverages and light meals and/or snacks.|
|shop|cair_repair|`shop=car_repair`|Shop focused on car repair (usually independent of a specific car brand).|
|accommodation_out|camp_site|`tourism=camp_site`|an area where people can temporarily use a shelter, such as a tent, camper van or sometimes a caravan. Typically, the area is spilt into 'pitches' or 'sites'.|
|shop|car|`shop=car`|Car store - a place to buy cars or to get your car repaired|
|shop|car_rental|`amenity=car_rental`|A place to rent a car|
|shop|car_sharing|`amenity=car_sharing`|A place to share a car|
|shop|car_wash|`amenity=car_wash`|A place to wash a car|
|accommodation_out|caravan_site|`tourism=caravan_site`|an area where people with caravans, motorhomes, recreational vehicles can stay overnight, or longer, in allotted spaces known as 'pitches' or 'sites'. They usually provide facilities including toilets, waste disposal, water supply, power supply etc.|
|destination|castle|`historic=castle`|Castles are (often fortified) buildings from medieval and modern times|
|burial_ground|cemetery|`landuse=cemetery`|A place where people, or sometimes animals are buried which is independent of places of worship. See 'grave_yard' for burial grounds in the yard of a place of worship.|
|accommodation_in|chalet|`tourism=chalet`|is a type of accommodation used in the hospitality industry to describe one or more detached cottages with self-contained cooking facilities and/or bathroom and toilet facilities.|
|shop|chemist|`shop=chemist`|Shop focused on selling articles of personal hygiene, cosmetics, and household cleaning products|
|leisure|cinema|`amenity=cinema`|Cinema/movie theatre - place for showing movies.|
|health|clinic|`amenity=clinic`|Medium-sized medical centres with tens of staff; smaller than a hospital and larger than a doctor's practice|
|shop|clothes|`shop=clothes`|Shop focused on selling clothes|
|education|college|`amenity=college`|A place for further education usually a post-secondary education institution|
|miscpoi|comm_tower|`man_made=tower`+`tower:type=communication`|Describes the type of tower as communication tower|
|public|community_centre|`amenity=community_centre`|A place mostly used for local events and festivities.|
|shop|computer|`shop=computer`|Shop focused on selling computers, peripherals, software,|
|shop|convenience|`shop=convenience`|A small local shop carrying a small subset of the items you would find in a supermarket|
|public|courthouse|`amenity=courthouse`|A place where justice is dispensed|
|health|dentist|`amenity=dentist`|A place where a professional dental surgeon who specializes in the diagnosis, prevention, and treatment of diseases and conditions on oral care is stationed.|
|shop|department_store|`shop=department_store`|A single large store - often multiple storeys high - selling a large variety of goods|
|health|doctors|`amenity=doctors`|A Doctor's Office is a place you can go to get medical attention or a check up|
|leisure|dog_park|`amenity=dog_park`|Designated area, with or without a fenced boundary, where dog-owners are permitted to exercise their pets unrestrained|
|miscpoi|drinking_water|`amenity=drinking_water`|Drinking water is a place where humans can obtain potable water for consumption. Typically, the water is used for only drinking. Also known as a drinking fountain or water tap.|
|public|embassy|`amenity=embassy`|A representation of a country in another country.|
|miscpoi|emergency_access|`highway=emergency_access_point`|Sign number which can be used to define you current position in case of an emergency|
|miscpoi|emergency_phone|`amenity=emergency_phone` or `emergency=phone`|A telephone dedicated to emergency calls|
|catering|fast_food|`amenity=fast_food`|Is for a place concentrating on very fast counter-only service and take-away food.|
|miscpoi|fire_hydrant|`amenity=fire_hydrant` or `emergency=fire_hydrant`|A fire hydrant is an active fire protection measure, and a source of water provided in most urban, suburban and rural areas with municipal water service to enable firefighters to tap into the municipal water supply to assist in extinguishing a fire.|
|public|fire_station|`amenity=fire_station`|A fire station|
|shop|florist|`shop=florist`|Shop focused on selling bouquets of flowers|
|catering|food_court|`amenity=food_court`|An area with several different restaurant food counters and a shared eating area|
|destination|fort|`historic=fort`|A military fort - distinct from a castle as it is generally more modern|
|miscpoi|fountain|`amenity=fountain`|A fountain for cultural / decoration / recreational purposes.|
|shop|furniture|`shop=furniture`|Shop focused on selling furniture, might range from small decoration items to a whole flat interior|
|shop|garden_centre|`shop=garden_centre`|Shop focused on selling potted flowers, maybe even trees|
|recycling|general_reclycling|`amenity=recycling`|Container or centre where you can take waste for recycling.|
|shop|gift|`shop=gift`|Shop focused on selling gifts, greeting cards, or tourist gifts (souvenirs)|
|recycling|glass|`recycling:glass=yes`|Container or centre where you can take waste for recycling for glass.|
|leisure|golf_course|`leisure=golf_course`|A place or area where you can play golf.|
|public|government|`amenity=government`|Government buildings|
|burial_ground|grave_yard|`amenity=grave_yard`|A place where people, or sometimes animals are buried which is close to a place of worship. See 'cemetery' for burial grounds not in the yard of a place of worship.|
|shop|greengrocer|`shop=greengrocer`|Shop focused on selling vegetables and fruits.|
|accommodation_in|guest_house|`tourism=guest_house` or `tourism=bed_and_breakfast`|Accommodation without hotel license that is typically owner-operated, offers a room and breakfast with staff not available 24/7, ranging from purpose-built guest houses to family-based Bed & Breakfast.|
|tourism|guidepost|`information=guidepost`+`tourism=information`|Signposts/Guideposts are often found along official hiking/cycling routes to indicate the directions to different destinations|
|shop|hairdresser|`shop=hairdresser`|Here you can get your hair cut, coloured,|
|shop|hardware|`shop=doityourself` or `shop=hardware`|Shop focused on selling tools and supplies to do-it-yourself householders, gardening,|
|historic|historic|`historic=*`|All other types of historic which is not defined as above|
|health|hospital|`amenity=hospital`|Institutions for health care providing treatment by specialised staff and equipment, and often but not always providing for longer-term patient stays.|
|accommodation_in|hostel|`tourism=hostel`|Provide inexpensive accommodation, typically with them having shared bedrooms, bathrooms, kitchens, and lounges.|
|accommodation_in|hotel|`tourism=hotel`|provide accommodation for guests with usually numbered rooms. Some facilities provided may include a basic bed, storage for clothing and additional guest facilities may include swimming pool, childcare, and conference facilities.|
|miscpoi|hunting_stand|`amenity=hunting_stand`|Hunting stands are open or enclosed platforms used by hunters to place themselves at an elevated height above the terrain.|
|leisure|ice_rink|`leisure=ice_rink`|A place where you can skate or play ice hockey.|
|tourism|information|`tourism=information`|An information source for tourists, travellers and visitors|
|shop|jewelry|`shop=jewelry`|Jewellers shops.|
|kindergarten|kindergarten|`amenity=kindergarten`|A place for looking after preschool children and (typically) giving early education.|
|shop|kiosk|`shop=kiosk`|A small shop on the pavement that sells magazines, tobacco, newspapers, sweets and stamps.|
|shop|laundry|`shop=laundry` or `shop=dry_cleaning`|A shop to get your normal clothes washed and dry. Might be self-service coin operated, with service staff for drop off or it could be a Shop or kiosk offering a clothes cleaning service. The actual cleaning may be done elsewhere.|
|leisure|leisure|`leisure=*`|All other types of leisure which is not defined as above|
|public|library|`amenity=library`|A public library (municipal, university) to borrow books from.|
|miscpoi|lighthouse|`man_made=lighthouse`|Sends out a light beam to guide ships.|
|shop|mall|`shop=mall`|A shopping mall - multiple stores under one roof (also known as a shopping centre)|
|man_made|man_made|`man_made=*`|All other types of man_made which is not defined as above|
|tourism|map|`information=map`+`tourism=information`|A board with a map.|
|public|marketplace|`amenity=marketplace`|A place where trade is regulated.|
|destination|memorial|`historic=museum`|Much like a monument, but smaller. Might range from a WWII memorial to a simple plate on a wall.|
|recycling|metal|`recycling:metal=yes`|Container or centre where you can take waste for recycling for metal.|
|shop|mobile_phone|`shop=mobile_phone`|Shop focused on selling mobile phones and accessories|
|money|money_changer|`amenity=bureau_de_change`|A place to change foreign bank notes and travellers cheques|
|destination|monument|`historic=museum`|An object, especially large and made of stone, built to remember and show respect to a person or group of people|
|public|mortuary|`amenity=mortuary`|A morgue or mortuary is a building or room (as in a hospital) used for the storage of human corpses awaiting identification, or removal for autopsy, burial, cremation or some other post-death ritual.|
|accommodation_in|motel|`tourism=motel`|It's an establishment that provides accommodation designed for motorists usually on a short-term basis, with convenient parking for motor cars at or close to the room.|
|destination|museum|`tourism=museum`|An institution which has exhibitions on scientific, historical, artistic, or cultural artefacts.|
|shop|newsagent|`shop=newsagent`|Shop focused on selling newspapers, cigarettes, other goods|
|leisure|nightclub|`amenity=nightclub`|A nightclub is a place to dance and drink at night.|
|public|nursing_home|`amenity=nursing_home`|A home for disabled or elderly persons who need permanent care.|
|miscpoi|observation_tower|`man_made=observation_tower`+`tower:type=observation`|One use of an Observation tower is a tower that used to watch for and report forest fire.|
|shop|optician|`shop=optician`|Shop focused on selling eyeglasses, contact lenses|
|shop|outdoor|`shop=outdoor`|Shop focused on selling garden furniture (sheds, outdoor tables, gates, fences, ...).|
|recycling|paper|`recycling:paper=yes`|Container or centre where you can take waste for recycling for paper.|
|health|pharmacy|`amenity=pharmacy`|A shop where a pharmacist sells medications|
|destination|picnic_site|`tourism=picnic_site`|An area that is suitable for eating outdoors and may have a number of facilities within it.|
|leisure|pitch|`leisure=pitch`|An area designed for playing a particular sport, normally designated with appropriate markings.|
|leisure|playground|`amenity=playground`|These are commonly small outdoor areas with children's play equipment such as swings, climbing frames and roundabouts.|
|public|police|`amenity=police`|A police station|
|public|post_box|`amenity=post_box`|A box for the reception of mail.|
|public|post_office|`amenity=post_office`|Post office building with postal services|
|public|prison|`amenity=prison`|A prison|
|catering|pub|`amenity=pub`|A place selling beer and other alcoholic drinks; may also provide food or accommodation|
|education|public_building|`amenity=public_building`|A generic public building. (Maybe abandoned by osm but still have data concerning this)|
|catering|restaurant|`amenity=restaurant`|Is for a generally formal place with sit-down facilities selling full meals served by waiters and often licensed (where allowed) to sell alcoholic drinks.|
|destination|ruins|`historic=ruins`|Remains of structures that were once complete, but have fallen into partial or complete disrepair.|
|education|school|`amenity=school`|Institution designed for learning under the supervision of teachers.|
|accommodation_in|shelter|`amenity=shelter`|Small place to protect against bad weather conditions|
|shop|shoes|`shop=shoes`|Shop focused on selling shoes|
|shop|shop|`shop=*`|All other types of shop which is not defined as above|
|leisure|soccer_pitch|`sport=soccer`|An area designed for playing a particular sport, normally designated with appropriate markings for soccer.|
|health|social_facility|`amenity=social_facility`|Social work is a profession and a social science committed to the pursuit of social justice, to quality of life, and to the development of the full potential of each individual, group and community in a society|
|sport|sport|`sport=*`|All other types of sport which is not defined as above|
|leisure|sport_centre|`amenity=sport_centre`|A distinct facility where a range of sports take place within an enclosed area.|
|shop|sports|`shop=sports`|Shop focused on selling sporting goods.|
|leisure|stadium|`leisure=stadium`|A major sports arena with substantial tiered seating.|
|shop|stationery|`shop=stationery`|Shop focused on selling office supplies|
|shop|supermarket|`shop=supermarket`|A large store for groceries and other goods.|
|miscpoi|surveillance|`man_made=surveillance`|To mark places and buildings monitored by public or private camera.|
|leisure|swimming_pool|`amenity=swimming_pool` or `leisure=swimming_pool` or `sport=swimming_pool`|A swimming pool is a place built for swimming as a recreational activity or sport, typically taking the form of an excavated and lined pool|
|public|telephone|`amenity=telephone`|Public telephone|
|leisure|tennis_pitch|`sport=tennis`|An area designed for playing a particular sport, normally designated with appropriate markings for tennis.|
|leisure|theatre|`amenity=theatre`|Place where live theatrical performances are held.|
|destination|theme_park|`tourism=theme_park`|An area where entertainment is provided by rides, game concessions, etc., catering to large numbers to people.|
|miscpoi|toilet|`amenity=toilets`|A public accessible toilets|
|tourism|tourism|`tourism=*`|All other types of tourism which is not defined as above|
|miscpoi|tower|`man_made=tower`|A tall and often lean building or structure e.g. telecoms. All tower except below specifics.|
|public|townhall|`amenity=townhall`|Building where the administration of a village, town or city may be located, or just a community meeting place|
|shop|toys|`shop=toys`|Shop focused on selling toys.|
|shop|travel_agency|`amenity=travel_agency`|Shop focused on selling tickets for travelling.|
|education|university|`amenity=university`|An educational institution designed for instruction, examination, or both, of students in many branches of advanced learning.|
|vending|vending|`amenity=vending_machine` or `vending=*`|A general machine to vend goods, tickets and so on|
|vending|vending_cigarette|`vending=cigarettes`|A cigarette machine is a vending machine that dispenses packets of cigarettes.|
|vending|vending_parking|`vending=parking_tickets`|A machine selling tickets for parking|
|health|veterinary|`amenity=veterinary`|It is a place where there is a certified doctor that deals with the prevention, diagnosis and treatment of disease, disorder and injury in animals is stationed.|
|shop|video|`shop=video`|Shop focused on selling or renting out videos/DVDs.|
|destination|viewpoint|`tourism=viewpoint`|A place for visitors, often high, with good a scenery view of the surrounding countryside or notable buildings.|
|miscpoi|waste_basket|`amenity=waste_backet`|A single small container for depositing garbage that is easily accessible for pedestrians.|
|miscpoi|wastewater_plant|`man_made=wastewater_plant`|Facilities used to treat wastewater (known as sewage in some countries).|
|leisure|water_park|`leisure=water_park`|An amusement area with water slides, recreational swimming pools and dressing rooms.|
|miscpoi|water_tower|`man_made=water_tower`|A tower to store water in, usually found on hills beside or in a town.|
|miscpoi|water_well|`man_made=water_well`|A water well is an excavation or structure created in the ground by digging, driving, boring or drilling to access groundwater in underground aquifers.|
|miscpoi|water_works|`man_made=water_works`|A place where drinking water is found and applied to the local water pipes network.|
|miscpoi|watermill|`man_made=watermill`|traditional Watermill, mostly ancient and out of order.|
|destination|wayside_cross|`historic=wayside_cross`|A historical (usually Christian) cross. Frequently found along the way in Southern Germany, Austria and probably elsewhere.|
|destination|wayside_shrine|`historic=wayside_shrine`|A historical shrine often showing a religious depiction. Frequently found along the way in Southern Germany, Austria and probably elsewhere.|
|miscpoi|windmill|`man_made=windmill`|Windmill, mostly ancient and out of order|
|destination|zoo|`tourism=zoo`|A zoological garden or park that has confined animals on display for viewing by the public.|


## poi_p


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|access|text|The legal accessibility of a element.|`access=*`|
|aggtype|text|Groups (aggregates) several different 'type' values to a common supertype, for a coarser, more general caterorization.| |
|brand|text|The identity of a specific product, service, or business. Often trademarks|`brand=*`|
|cuisine|text|The type of food served at an eating place.|`cuisine=*`|
|opening_hours|text|The timing of when something is open or close|`opening_hours=*`|
|phone|text|A telephone number associated with the object.|`phone=*` or `contact:phone=*`|
|tower_type|text|The type of tower|`tower:type=*`|
|type|text|(see table below)| |
|website|text|Specifying the link to the official website for a feature.|`website=*`|
|wikipedia|text|Provide a reference to an article in Wikipedia about the feature.|`wikipedia=*`|


Values of attribute type

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|accommodation_out|alpine_hut|`tourism=alpine_hut`|a mountain hut is a remote building positioned in the mountains designed to provided lodging accommodation for mountaineers, climbers and hikers. The access is usually restricted to foot, mountain bike or ski.|
|amenity|amenity|`amenity=*`|All other types of amenity which is not defined as above|
|destination|archaeological_site|`historic=archaeological_site`|A place in which evidence of past activity is preserved|
|public|arts_centre|`amenity=arts_centre`|A venue where a variety of arts are performed or conducted|
|destination|artwork|`tourism=artwork`|Used to tag public pieces of art. Usually such artwork are outdoors.|
|money|atm|`amenity=atm`|A device that provides the clients of a financial institution with access to financial transactions.|
|destination|attraction|`tourism=attraction`|A general place of interest for visitors. Typically used for its natural or historical significance.|
|shop|bakery|`shop=bakery`|Shop focused on selling bread|
|money|bank|`amenity=bank`|Shows the location of a bank branch.|
|catering|bar|`amenity=bar`|Bar is a purpose-built commercial establishment that sells alcoholic drinks to be consumed on the premises. They are characterised by a noisy and vibrant atmosphere, similar to a party and usually don't sell food.|
|destination|battlefield|`historic=battlefield`|The site of a battle or military skirmish in the past. This could be on land or at sea.|
|shop|beauty|`shop=beauty`|A non-hairdresser beauty shop, spa, nail salon, etc..|
|miscpoi|bench|`amenity=bench`|A bench to sit down and relax a bit|
|shop|beverages|`shop=beverages` or `shop=alcohol`|Shop focused on selling alcoholic and non-alcoholic beverages.|
|shop|bicycle|`shop=bicycle`|Shop focused on selling bicycles, bicycle equipment and may rent or repair them|
|shop|bicycle_rental|`amenity=bicycle_rental`|A place to rent a bicycle|
|catering|biergarten|`amenity=biergarten`|Biergarten or beer garden is an open-air area where alcoholic beverages along with food is prepared and served.|
|tourism|board|`information=board`+`tourism=information`|A board with information|
|shop|books|`shop=books`|Shop focused on selling books|
|shop|butcher|`shop=butcher`|Shop focused on selling meat|
|catering|cafe|`amenity=cafe`|Generally informal place with sit-down facilities selling beverages and light meals and/or snacks.|
|shop|cair_repair|`shop=car_repair`|Shop focused on car repair (usually independent of a specific car brand).|
|accommodation_out|camp_site|`tourism=camp_site`|an area where people can temporarily use a shelter, such as a tent, camper van or sometimes a caravan. Typically, the area is spilt into 'pitches' or 'sites'.|
|shop|car|`shop=car`|Car store - a place to buy cars or to get your car repaired|
|shop|car_rental|`amenity=car_rental`|A place to rent a car|
|shop|car_sharing|`amenity=car_sharing`|A place to share a car|
|shop|car_wash|`amenity=car_wash`|A place to wash a car|
|accommodation_out|caravan_site|`tourism=caravan_site`|an area where people with caravans, motorhomes, recreational vehicles can stay overnight, or longer, in allotted spaces known as 'pitches' or 'sites'. They usually provide facilities including toilets, waste disposal, water supply, power supply etc.|
|destination|castle|`historic=castle`|Castles are (often fortified) buildings from medieval and modern times|
|burial_ground|cemetery|`landuse=cemetery`|A place where people, or sometimes animals are buried which is independent of places of worship. See 'grave_yard' for burial grounds in the yard of a place of worship.|
|accommodation_in|chalet|`tourism=chalet`|is a type of accommodation used in the hospitality industry to describe one or more detached cottages with self-contained cooking facilities and/or bathroom and toilet facilities.|
|shop|chemist|`shop=chemist`|Shop focused on selling articles of personal hygiene, cosmetics, and household cleaning products|
|leisure|cinema|`amenity=cinema`|Cinema/movie theatre - place for showing movies.|
|health|clinic|`amenity=clinic`|Medium-sized medical centres with tens of staff; smaller than a hospital and larger than a doctor's practice|
|shop|clothes|`shop=clothes`|Shop focused on selling clothes|
|education|college|`amenity=college`|A place for further education usually a post-secondary education institution|
|miscpoi|comm_tower|`man_made=tower`+`tower:type=communication`|Describes the type of tower as communication tower|
|public|community_centre|`amenity=community_centre`|A place mostly used for local events and festivities.|
|shop|computer|`shop=computer`|Shop focused on selling computers, peripherals, software,|
|shop|convenience|`shop=convenience`|A small local shop carrying a small subset of the items you would find in a supermarket|
|public|courthouse|`amenity=courthouse`|A place where justice is dispensed|
|health|dentist|`amenity=dentist`|A place where a professional dental surgeon who specializes in the diagnosis, prevention, and treatment of diseases and conditions on oral care is stationed.|
|shop|department_store|`shop=department_store`|A single large store - often multiple storeys high - selling a large variety of goods|
|health|doctors|`amenity=doctors`|A Doctor's Office is a place you can go to get medical attention or a check up|
|leisure|dog_park|`amenity=dog_park`|Designated area, with or without a fenced boundary, where dog-owners are permitted to exercise their pets unrestrained|
|miscpoi|drinking_water|`amenity=drinking_water`|Drinking water is a place where humans can obtain potable water for consumption. Typically, the water is used for only drinking. Also known as a drinking fountain or water tap.|
|public|embassy|`amenity=embassy`|A representation of a country in another country.|
|miscpoi|emergency_access|`highway=emergency_access_point`|Sign number which can be used to define you current position in case of an emergency|
|miscpoi|emergency_phone|`amenity=emergency_phone` or `emergency=phone`|A telephone dedicated to emergency calls|
|catering|fast_food|`amenity=fast_food`|Is for a place concentrating on very fast counter-only service and take-away food.|
|miscpoi|fire_hydrant|`amenity=fire_hydrant` or `emergency=fire_hydrant`|A fire hydrant is an active fire protection measure, and a source of water provided in most urban, suburban and rural areas with municipal water service to enable firefighters to tap into the municipal water supply to assist in extinguishing a fire.|
|public|fire_station|`amenity=fire_station`|A fire station|
|shop|florist|`shop=florist`|Shop focused on selling bouquets of flowers|
|catering|food_court|`amenity=food_court`|An area with several different restaurant food counters and a shared eating area|
|destination|fort|`historic=fort`|A military fort - distinct from a castle as it is generally more modern|
|miscpoi|fountain|`amenity=fountain`|A fountain for cultural / decoration / recreational purposes.|
|shop|furniture|`shop=furniture`|Shop focused on selling furniture, might range from small decoration items to a whole flat interior|
|shop|garden_centre|`shop=garden_centre`|Shop focused on selling potted flowers, maybe even trees|
|recycling|general_reclycling|`amenity=recycling`|Container or centre where you can take waste for recycling.|
|shop|gift|`shop=gift`|Shop focused on selling gifts, greeting cards, or tourist gifts (souvenirs)|
|recycling|glass|`recycling:glass=yes`|Container or centre where you can take waste for recycling for glass.|
|leisure|golf_course|`leisure=golf_course`|A place or area where you can play golf.|
|public|government|`amenity=government`|Government buildings|
|burial_ground|grave_yard|`amenity=grave_yard`|A place where people, or sometimes animals are buried which is close to a place of worship. See 'cemetery' for burial grounds not in the yard of a place of worship.|
|shop|greengrocer|`shop=greengrocer`|Shop focused on selling vegetables and fruits.|
|accommodation_in|guest_house|`tourism=guest_house` or `tourism=bed_and_breakfast`|Accommodation without hotel license that is typically owner-operated, offers a room and breakfast with staff not available 24/7, ranging from purpose-built guest houses to family-based Bed & Breakfast.|
|tourism|guidepost|`information=guidepost`+`tourism=information`|Signposts/Guideposts are often found along official hiking/cycling routes to indicate the directions to different destinations|
|shop|hairdresser|`shop=hairdresser`|Here you can get your hair cut, coloured,|
|shop|hardware|`shop=doityourself` or `shop=hardware`|Shop focused on selling tools and supplies to do-it-yourself householders, gardening,|
|historic|historic|`historic=*`|All other types of historic which is not defined as above|
|health|hospital|`amenity=hospital`|Institutions for health care providing treatment by specialised staff and equipment, and often but not always providing for longer-term patient stays.|
|accommodation_in|hostel|`tourism=hostel`|Provide inexpensive accommodation, typically with them having shared bedrooms, bathrooms, kitchens, and lounges.|
|accommodation_in|hotel|`tourism=hotel`|provide accommodation for guests with usually numbered rooms. Some facilities provided may include a basic bed, storage for clothing and additional guest facilities may include swimming pool, childcare, and conference facilities.|
|miscpoi|hunting_stand|`amenity=hunting_stand`|Hunting stands are open or enclosed platforms used by hunters to place themselves at an elevated height above the terrain.|
|leisure|ice_rink|`leisure=ice_rink`|A place where you can skate or play ice hockey.|
|tourism|information|`tourism=information`|An information source for tourists, travellers and visitors|
|shop|jewelry|`shop=jewelry`|Jewellers shops.|
|kindergarten|kindergarten|`amenity=kindergarten`|A place for looking after preschool children and (typically) giving early education.|
|shop|kiosk|`shop=kiosk`|A small shop on the pavement that sells magazines, tobacco, newspapers, sweets and stamps.|
|shop|laundry|`shop=laundry` or `shop=dry_cleaning`|A shop to get your normal clothes washed and dry. Might be self-service coin operated, with service staff for drop off or it could be a Shop or kiosk offering a clothes cleaning service. The actual cleaning may be done elsewhere.|
|leisure|leisure|`leisure=*`|All other types of leisure which is not defined as above|
|public|library|`amenity=library`|A public library (municipal, university) to borrow books from.|
|miscpoi|lighthouse|`man_made=lighthouse`|Sends out a light beam to guide ships.|
|shop|mall|`shop=mall`|A shopping mall - multiple stores under one roof (also known as a shopping centre)|
|man_made|man_made|`man_made=*`|All other types of man_made which is not defined as above|
|tourism|map|`information=map`+`tourism=information`|A board with a map.|
|public|marketplace|`amenity=marketplace`|A place where trade is regulated.|
|destination|memorial|`historic=museum`|Much like a monument, but smaller. Might range from a WWII memorial to a simple plate on a wall.|
|recycling|metal|`recycling:metal=yes`|Container or centre where you can take waste for recycling for metal.|
|shop|mobile_phone|`shop=mobile_phone`|Shop focused on selling mobile phones and accessories|
|money|money_changer|`amenity=bureau_de_change`|A place to change foreign bank notes and travellers cheques|
|destination|monument|`historic=museum`|An object, especially large and made of stone, built to remember and show respect to a person or group of people|
|public|mortuary|`amenity=mortuary`|A morgue or mortuary is a building or room (as in a hospital) used for the storage of human corpses awaiting identification, or removal for autopsy, burial, cremation or some other post-death ritual.|
|accommodation_in|motel|`tourism=motel`|It's an establishment that provides accommodation designed for motorists usually on a short-term basis, with convenient parking for motor cars at or close to the room.|
|destination|museum|`tourism=museum`|An institution which has exhibitions on scientific, historical, artistic, or cultural artefacts.|
|shop|newsagent|`shop=newsagent`|Shop focused on selling newspapers, cigarettes, other goods|
|leisure|nightclub|`amenity=nightclub`|A nightclub is a place to dance and drink at night.|
|public|nursing_home|`amenity=nursing_home`|A home for disabled or elderly persons who need permanent care.|
|miscpoi|observation_tower|`man_made=observation_tower`+`tower:type=observation`|One use of an Observation tower is a tower that used to watch for and report forest fire.|
|shop|optician|`shop=optician`|Shop focused on selling eyeglasses, contact lenses|
|shop|outdoor|`shop=outdoor`|Shop focused on selling garden furniture (sheds, outdoor tables, gates, fences, ...).|
|recycling|paper|`recycling:paper=yes`|Container or centre where you can take waste for recycling for paper.|
|health|pharmacy|`amenity=pharmacy`|A shop where a pharmacist sells medications|
|destination|picnic_site|`tourism=picnic_site`|An area that is suitable for eating outdoors and may have a number of facilities within it.|
|leisure|pitch|`leisure=pitch`|An area designed for playing a particular sport, normally designated with appropriate markings.|
|leisure|playground|`amenity=playground`|These are commonly small outdoor areas with children's play equipment such as swings, climbing frames and roundabouts.|
|public|police|`amenity=police`|A police station|
|public|post_box|`amenity=post_box`|A box for the reception of mail.|
|public|post_office|`amenity=post_office`|Post office building with postal services|
|public|prison|`amenity=prison`|A prison|
|catering|pub|`amenity=pub`|A place selling beer and other alcoholic drinks; may also provide food or accommodation|
|education|public_building|`amenity=public_building`|A generic public building. (Maybe abandoned by osm but still have data concerning this)|
|catering|restaurant|`amenity=restaurant`|Is for a generally formal place with sit-down facilities selling full meals served by waiters and often licensed (where allowed) to sell alcoholic drinks.|
|destination|ruins|`historic=ruins`|Remains of structures that were once complete, but have fallen into partial or complete disrepair.|
|education|school|`amenity=school`|Institution designed for learning under the supervision of teachers.|
|accommodation_in|shelter|`amenity=shelter`|Small place to protect against bad weather conditions|
|shop|shoes|`shop=shoes`|Shop focused on selling shoes|
|shop|shop|`shop=*`|All other types of shop which is not defined as above|
|leisure|soccer_pitch|`sport=soccer`|An area designed for playing a particular sport, normally designated with appropriate markings for soccer.|
|health|social_facility|`amenity=social_facility`|Social work is a profession and a social science committed to the pursuit of social justice, to quality of life, and to the development of the full potential of each individual, group and community in a society|
|sport|sport|`sport=*`|All other types of sport which is not defined as above|
|leisure|sport_centre|`amenity=sport_centre`|A distinct facility where a range of sports take place within an enclosed area.|
|shop|sports|`shop=sports`|Shop focused on selling sporting goods.|
|leisure|stadium|`leisure=stadium`|A major sports arena with substantial tiered seating.|
|shop|stationery|`shop=stationery`|Shop focused on selling office supplies|
|shop|supermarket|`shop=supermarket`|A large store for groceries and other goods.|
|miscpoi|surveillance|`man_made=surveillance`|To mark places and buildings monitored by public or private camera.|
|leisure|swimming_pool|`amenity=swimming_pool` or `leisure=swimming_pool` or `sport=swimming_pool`|A swimming pool is a place built for swimming as a recreational activity or sport, typically taking the form of an excavated and lined pool|
|public|telephone|`amenity=telephone`|Public telephone|
|leisure|tennis_pitch|`sport=tennis`|An area designed for playing a particular sport, normally designated with appropriate markings for tennis.|
|leisure|theatre|`amenity=theatre`|Place where live theatrical performances are held.|
|destination|theme_park|`tourism=theme_park`|An area where entertainment is provided by rides, game concessions, etc., catering to large numbers to people.|
|miscpoi|toilet|`amenity=toilets`|A public accessible toilets|
|tourism|tourism|`tourism=*`|All other types of tourism which is not defined as above|
|miscpoi|tower|`man_made=tower`|A tall and often lean building or structure e.g. telecoms. All tower except below specifics.|
|public|townhall|`amenity=townhall`|Building where the administration of a village, town or city may be located, or just a community meeting place|
|shop|toys|`shop=toys`|Shop focused on selling toys.|
|shop|travel_agency|`amenity=travel_agency`|Shop focused on selling tickets for travelling.|
|education|university|`amenity=university`|An educational institution designed for instruction, examination, or both, of students in many branches of advanced learning.|
|vending|vending|`amenity=vending_machine` or `vending=*`|A general machine to vend goods, tickets and so on|
|vending|vending_cigarette|`vending=cigarettes`|A cigarette machine is a vending machine that dispenses packets of cigarettes.|
|vending|vending_parking|`vending=parking_tickets`|A machine selling tickets for parking|
|health|veterinary|`amenity=veterinary`|It is a place where there is a certified doctor that deals with the prevention, diagnosis and treatment of disease, disorder and injury in animals is stationed.|
|shop|video|`shop=video`|Shop focused on selling or renting out videos/DVDs.|
|destination|viewpoint|`tourism=viewpoint`|A place for visitors, often high, with good a scenery view of the surrounding countryside or notable buildings.|
|miscpoi|waste_basket|`amenity=waste_backet`|A single small container for depositing garbage that is easily accessible for pedestrians.|
|miscpoi|wastewater_plant|`man_made=wastewater_plant`|Facilities used to treat wastewater (known as sewage in some countries).|
|leisure|water_park|`leisure=water_park`|An amusement area with water slides, recreational swimming pools and dressing rooms.|
|miscpoi|water_tower|`man_made=water_tower`|A tower to store water in, usually found on hills beside or in a town.|
|miscpoi|water_well|`man_made=water_well`|A water well is an excavation or structure created in the ground by digging, driving, boring or drilling to access groundwater in underground aquifers.|
|miscpoi|water_works|`man_made=water_works`|A place where drinking water is found and applied to the local water pipes network.|
|miscpoi|watermill|`man_made=watermill`|traditional Watermill, mostly ancient and out of order.|
|destination|wayside_cross|`historic=wayside_cross`|A historical (usually Christian) cross. Frequently found along the way in Southern Germany, Austria and probably elsewhere.|
|destination|wayside_shrine|`historic=wayside_shrine`|A historical shrine often showing a religious depiction. Frequently found along the way in Southern Germany, Austria and probably elsewhere.|
|miscpoi|windmill|`man_made=windmill`|Windmill, mostly ancient and out of order|
|destination|zoo|`tourism=zoo`|A zoological garden or park that has confined animals on display for viewing by the public.|


## pow_a


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|access|text|The legal accessibility of a element.|`access=*`|
|aggtype|text|Groups (aggregates) several different 'type' values to a common supertype, for a coarser, more general caterorization.| |
|opening_hours|text|The timing of when something is open or close|`opening_hours=*`|
|phone|text|A telephone number associated with the object.|`phone=*` or `contact:phone=*`|
|type|text|(see table below)| |
|website|text|Specifying the link to the official website for a feature.|`website=*`|
|wikipedia|text|Provide a reference to an article in Wikipedia about the feature.|`wikipedia=*`|


Values of attribute type

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|christian|anglican|`denomination=anglican`+`religion=christian`|A christian place of worship with denomination|
|christian|baptist|`denomination=baptist`+`religion=christian`|A christian place of worship with denomination|
|buddhist|buddhist|`religion=buddhist`|A buddist place of worship|
|christian|catholic|`denomination=catholic`+`religion=christian`|A christian place of worship with denomination|
|christian|christian|`denomination=*`+`religion=christian`|A christian place of worship. This is a generalise christian type other then the specific denomination|
|christian|evangelical|`denomination=evangelical`+`religion=christian`|A christian place of worship with denomination|
|hindu|hindu|`religion=hindu`|A hindu place of worship|
|jewish|jewish|`religion=jewish`|A jewish place of worship|
|christian|lutheran|`denomination=lutheran`+`religion=christian`|A christian place of worship with denomination|
|christian|methodist|`denomination=methodist`+`religion=christian`|A christian place of worship with denomination|
|christian|mormon|`denomination=mormon`+`religion=christian`|A christian place of worship with denomination|
|muslim|muslim|`denomination=*`+`religion=muslim`|A muslim place of worship. This is a generalise muslim type other then the specific denomination|
|christian|orthodox|`denomination=orthodox`+`religion=christian`|A christian place of worship with denomination|
|place_of_worship|place_of_worship|`religion=*` or `amenity=place_of_worship`|A place of worship which is not tag to any of the above.|
|christian|presbyterian|`denomination=presbyterian`+`religion=christian`|A christian place of worship with denomination|
|christian|protestant|`denomination=protestant`+`religion=christian`|A christian place of worship with denomination|
|muslim|shia|`denomination=shia`+`religion=muslim`|A muslim place of worship with denomination.|
|shinto|shinto|`religion=shinto`|A shinto place of worship|
|sikh|sikh|`religion=sikh`|A sikh place of worship|
|muslim|sunni|`denomination=sunni`+`religion=muslim`|A muslim place of worship with denomination.|
|taoist|taoist|`religion=taoist`|A taoist place of worship|


## pow_p


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|access|text|The legal accessibility of a element.|`access=*`|
|aggtype|text|Groups (aggregates) several different 'type' values to a common supertype, for a coarser, more general caterorization.| |
|opening_hours|text|The timing of when something is open or close|`opening_hours=*`|
|phone|text|A telephone number associated with the object.|`phone=*` or `contact:phone=*`|
|type|text|(see table below)| |
|website|text|Specifying the link to the official website for a feature.|`website=*`|
|wikipedia|text|Provide a reference to an article in Wikipedia about the feature.|`wikipedia=*`|


Values of attribute type

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|christian|anglican|`denomination=anglican`+`religion=christian`|A christian place of worship with denomination|
|christian|baptist|`denomination=baptist`+`religion=christian`|A christian place of worship with denomination|
|buddhist|buddhist|`religion=buddhist`|A buddist place of worship|
|christian|catholic|`denomination=catholic`+`religion=christian`|A christian place of worship with denomination|
|christian|christian|`denomination=*`+`religion=christian`|A christian place of worship. This is a generalise christian type other then the specific denomination|
|christian|evangelical|`denomination=evangelical`+`religion=christian`|A christian place of worship with denomination|
|hindu|hindu|`religion=hindu`|A hindu place of worship|
|jewish|jewish|`religion=jewish`|A jewish place of worship|
|christian|lutheran|`denomination=lutheran`+`religion=christian`|A christian place of worship with denomination|
|christian|methodist|`denomination=methodist`+`religion=christian`|A christian place of worship with denomination|
|christian|mormon|`denomination=mormon`+`religion=christian`|A christian place of worship with denomination|
|muslim|muslim|`denomination=*`+`religion=muslim`|A muslim place of worship. This is a generalise muslim type other then the specific denomination|
|christian|orthodox|`denomination=orthodox`+`religion=christian`|A christian place of worship with denomination|
|place_of_worship|place_of_worship|`religion=*` or `amenity=place_of_worship`|A place of worship which is not tag to any of the above.|
|christian|presbyterian|`denomination=presbyterian`+`religion=christian`|A christian place of worship with denomination|
|christian|protestant|`denomination=protestant`+`religion=christian`|A christian place of worship with denomination|
|muslim|shia|`denomination=shia`+`religion=muslim`|A muslim place of worship with denomination.|
|shinto|shinto|`religion=shinto`|A shinto place of worship|
|sikh|sikh|`religion=sikh`|A sikh place of worship|
|muslim|sunni|`denomination=sunni`+`religion=muslim`|A muslim place of worship with denomination.|
|taoist|taoist|`religion=taoist`|A taoist place of worship|


## railway_l


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|aggtype|text|Groups (aggregates) several different 'type' values to a common supertype, for a coarser, more general caterorization.| |
|bridge|boolean|A bridge is an artificial construction that spans features such as roads, railways, waterways or valleys and carries a road, railway or other feature. (see table below)| |
|frequency|text|The electrical frequency that the electrified cable is running on|`frequency=*`|
|tunnel|boolean|A tunnel is an underground passage for a road or similar. (see table below)| |
|type|text|(see table below)| |
|voltage|text|The voltage level the electrified cable is running on|`voltage=*`|
|z_order|smallint|The layer tag is used to describe vertical relationships between different crossing or overlapping map features. Use this in combination with bridge/tunnel tags when one way passes above or under another one. For describing different floors within a building or levels of multilevel parking decks use levels instead of layers.|`layer=*`|


Values of attribute bridge

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|False|**`bridge≠split_log`**+**`bridge≠beam`**+**`bridge≠culvert`**+**`bridge≠low_water_crossing`**+**`bridge≠yes`**+**`bridge≠suspension`**+**`bridge≠viaduct`**+**`bridge≠aqueduct`**+**`bridge≠covered`**| |
|True|`bridge=split_log` or `bridge=beam` or `bridge=culvert` or `bridge=low_water_crossing` or `bridge=yes` or `bridge=suspension` or `bridge=viaduct` or `bridge=aqueduct` or `bridge=covered`| |



Values of attribute tunnel

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|False|**`tunnel≠passage`**+**`tunnel≠culvert`**+**`tunnel≠noiseprotection galerie`**+**`tunnel≠gallery`**+**`tunnel≠building_passage`**+**`tunnel≠avalanche_protector`**+**`tunnel≠viaduct`**+**`tunnel≠tunnel`**+**`tunnel≠yes`**| |
|True|`tunnel=passage` or `tunnel=culvert` or `tunnel=noiseprotection galerie` or `tunnel=gallery` or `tunnel=building_passage` or `tunnel=avalanche_protector` or `tunnel=viaduct` or `tunnel=tunnel` or `tunnel=yes`| |



Values of attribute type

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|railway|rail|`railway=rail`|Full sized passenger or freight trains in the standard gauge for the country or state.|
|railway|light_rail|`railway=light_rail`|A higher-standard tram system, normally in its own right-of-way. Often it connects towns and thus reaches a considerable length (tens of kilometer).|
|railway|subway|`railway=subway`|A city passenger rail service running mostly grade separated|
|railway|tram|`railway=tram`|One or two carriage rail vehicles, usually sharing motor road|
|railway|monorail|`railway=monorail`|A railway with only a single rail.|
|railway|narrow_gauge|`railway=narrow_gauge`|Narrow-gauge passenger or freight trains.|
|railway|miniature|`railway=miniature`|Miniature railways are narrower than narrow gauge and carry passengers. They can be found in parks.|
|railway|funicular|`railway=funicular`|Cable driven inclined railways|
|railway|railway|`railway=*`|All other types of railways which is not defined as above|
|aerialway|drag_lift|`aerialway=drag_lift`|an overhead tow-line for skiers and riders.|
|aerialway|chair_lift|`aerialway=chair_lift` or `aerialway=high_speed_chair_lift`|Looped cable with a series of single chairs (typically seating two or four people, but can be more). Exposed to the open air (can have a bubble).|
|aerialway|cable_car|`aerialway=cable_car`|Just one or two large cars. The cable forms a loop, but the cars do not loop around, they just move up and down on their own side.|
|aerialway|gondola|`aerialway=gondola`|Many cars on a looped cable.|
|aerialway|goods|`aerialway=goods`|A cable/wire supported lift for goods. Passenger transport is usually not allowed.|
|aerialway|platter|`aerialway=platter`|Platter lift (poma). Overhead tow-line for skiers and riders with platters.|
|aerialway|t-bar|`aerialway=t-bar`|T-bar lift. Overhead tow-line for skiers and riders with T-shaped carriers for two passengers.|
|aerialway|j-bar|`aerialway=j-bar`|J-bar lift or L-bar lift. Overhead tow-line for skiers and riders with carriers in J-shape.|
|aerialway|magic_carpet|`aerialway=magic_carpet`|Ski lift for small children resembling a conveyor belt.|
|aerialway|zip_line|`aerialway=zip_line`|Zip lines, Flying fox and similar|
|aerialway|rope_tow|`aerialway=rope_tow`|Ski tow lift. Tow-line for skiers and riders where passenger hold by hand or use special tow grabbers.|
|aerialway|mixed_lift|`aerialway=mixed_lift`|A lift mixed with gondola and chair_lift|
|aerialway|aerialway|`aerialway=*`|All other types of aerialways which is not defined as above|


## road_l


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|aggtype|text|"roundabout" for roundabouts, otherweise the general type/importance of the road or way. See the "type" attribute for a road's or way's specific type for both, roundabout and non-roundabout roads/ways.| |
|bridge|boolean|A bridge is an artificial construction that spans features such as roads, railways, waterways or valleys and carries a road, railway or other feature. (see table below)| |
|maxspeed|smallint|Specifies the maximum legal speed limit on a road, railway or waterway|`maxspeed=*`|
|oneway|boolean|Oneway streets are streets where you are only allowed to drive in one direction.|`oneway=*`|
|ref|text|Used for reference numbers or codes. Common for roads, highway exits, routes, etc.|`ref=*`|
|tunnel|boolean|A tunnel is an underground passage for a road or similar. (see table below)| |
|type|text|(see table below)| |
|z_order|smallint|The layer tag is used to describe vertical relationships between different crossing or overlapping map features. Use this in combination with bridge/tunnel tags when one way passes above or under another one. For describing different floors within a building or levels of multilevel parking decks use levels instead of layers.|`layer=*`|


Values of attribute bridge

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|False|**`bridge≠split_log`**+**`bridge≠beam`**+**`bridge≠culvert`**+**`bridge≠low_water_crossing`**+**`bridge≠yes`**+**`bridge≠suspension`**+**`bridge≠viaduct`**+**`bridge≠aqueduct`**+**`bridge≠covered`**| |
|True|`bridge=split_log` or `bridge=beam` or `bridge=culvert` or `bridge=low_water_crossing` or `bridge=yes` or `bridge=suspension` or `bridge=viaduct` or `bridge=aqueduct` or `bridge=covered`| |



Values of attribute tunnel

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|False|**`tunnel≠passage`**+**`tunnel≠culvert`**+**`tunnel≠noiseprotection galerie`**+**`tunnel≠gallery`**+**`tunnel≠building_passage`**+**`tunnel≠avalanche_protector`**+**`tunnel≠viaduct`**+**`tunnel≠tunnel`**+**`tunnel≠yes`**| |
|True|`tunnel=passage` or `tunnel=culvert` or `tunnel=noiseprotection galerie` or `tunnel=gallery` or `tunnel=building_passage` or `tunnel=avalanche_protector` or `tunnel=viaduct` or `tunnel=tunnel` or `tunnel=yes`| |



Values of attribute type

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|major_road|motorway|`highway=motorway`+**`junction≠roundabout`**|A restricted access major divided highway, normally with 2 or more running lanes plus emergency hard shoulder. Equivalent to the Freeway, Autobahn, etc..|
|major_road|trunk|`highway=trunk`+**`junction≠roundabout`**|The most important roads in a country's system that aren't motorways. (Need not necessarily be a divided highway.)|
|major_road|primary|`highway=primary`+**`junction≠roundabout`**|The next most important roads in a country's system. (Often link larger towns.)|
|major_road|secondary|`highway=secondary`+**`junction≠roundabout`**|The next most important roads in a country's system. (Often link smaller towns and villages.)	|
|major_road|tertiary|`highway=tertiary`+**`junction≠roundabout`**|The next most important roads in a country's system.|
|minor_road|unclassified|`highway=unclassified`+**`junction≠roundabout`**|The least most important through roads in a country's system - i.e. minor roads of a lower classification than tertiary, but which serve a purpose other than access to properties. (The word 'unclassified' is a historical artefact of the UK road system and does not mean that the classification is unknown; you can use highway=road for that.)	|
|minor_road|residential|`highway=residential`+**`junction≠roundabout`**|Roads which are primarily lined with and serve as an access to housing.|
|minor_road|living_street|`highway=living_street`+**`junction≠roundabout`**|For living streets, which are residential streets where pedestrians have legal priority over cars, speeds are kept very low and where children are allowed to play on the street.	|
|minor_road|pedestrian|`highway=pedestrian`+**`junction≠roundabout`**|For roads used mainly/exclusively for pedestrians in shopping and some residential areas which may allow access by motorised vehicles only for very limited periods of the day. To create a 'square' or 'plaza' create a closed way and tag as pedestrian.|
|highway_links|motorway_link|`highway=motorway_link`+**`junction≠roundabout`**|The link roads (sliproads/ramps) leading to/from a motorway from/to a motorway or lower class highway. Normally with the same motorway restrictions.|
|highway_links|trunk_link|`highway=trunk_link`+**`junction≠roundabout`**|The link roads (sliproads/ramps) leading to/from a trunk road from/to a trunk road or lower class highway.|
|highway_links|primary_link|`highway=primary_link`+**`junction≠roundabout`**|The link roads (sliproads/ramps) leading to/from a primary road from/to a primary road or lower class highway.|
|highway_links|secondary_link|`highway=secondary_link`+**`junction≠roundabout`**|The link roads (sliproads/ramps) leading to/from a secondary road from/to a secondary road or lower class highway.|
|small_road|service|`highway=service`+**`junction≠roundabout`**|For access roads to, or within an industrial estate, camp site, business park, car park etc. Can be used in conjunction with service=* to indicate the type of usage and with access=* to indicate who can use it and in what circumstances.|
|track|track|`highway=track`+**`junction≠roundabout`**+**`tracktype≠*`**|Roads for agricultural use, gravel roads in the forest etc. and no tracktype tag is present|
|track|grade1|`highway=track`+`tracktype=grade1`+**`junction≠roundabout`**|Solid. Usually a paved or heavily compacted hardcore surface.|
|track|grade2|`highway=track`+`tracktype=grade2`+**`junction≠roundabout`**|Mostly solid. Usually an unpaved track with surface of gravel mixed with a varying amount of sand, silt, and clay.|
|track|grade3|`highway=track`+`tracktype=grade3`+**`junction≠roundabout`**|Even mixture of hard and soft materials. Almost always an unpaved track.|
|track|grade4|`highway=track`+`tracktype=grade4`+**`junction≠roundabout`**|Mostly soft. Almost always an unpaved track prominently with soil/sand/grass, but with some hard materials, or compressed materials mixed in.|
|track|grade5|`highway=track`+`tracktype=grade5`+**`junction≠roundabout`**|Soft. Almost always an unpaved track lacking hard materials, uncompacted, subtle on the landscape, with surface of soil/sand/grass.|
|no_large_vehicle|bridleway|`highway=bridleway`+**`junction≠roundabout`**|For horses.|
|no_large_vehicle|cycleway|`highway=cycleway`+**`junction≠roundabout`**|Cycling infrastructure that is an inherent part of a road - particularly 'cycle lanes' which are a part of the road|
|no_large_vehicle|footway|`highway=footway`+**`junction≠roundabout`**|For designated footpaths; i.e., mainly/exclusively for pedestrians. This includes walking tracks and gravel paths.|
|no_large_vehicle|path|`highway=path`+**`junction≠roundabout`**|A non-specific path.|
|no_large_vehicle|steps|`highway=steps`+**`junction≠roundabout`**|For flights of steps (stairs) on footways.|
|unclassified|road|`highway=*`+**`roundabout≠*`**|A road where the mapper is unable to ascertain the classification from the information available. This is intended as a temporary tag to mark a road until it has been properly surveyed|
|roundabout|motorway|`highway=motorway`+`junction=roundabout`|A roundabout on a motorway|
|roundabout|trunk|`highway=trunk`+`junction=roundabout`|A roundabout on a trunk road|
|roundabout|primary|`highway=primary`+`junction=roundabout`|A roundabout on a primary road|
|roundabout|secondary|`highway=secondary`+`junction=roundabout`|A roundabout on a secondary road|
|roundabout|tertiary|`highway=tertiary`+`junction=roundabout`|A roundabout on a tertiary road|
|roundabout|unclassified|`highway=unclassified`+`junction=roundabout`|A roundabout on a minor public roads (typically at the lowest level of the interconnecting grid network)|
|roundabout|residential|`highway=residential`+`junction=roundabout`|A roundabout on a residential road|
|roundabout|living_street|`highway=living_street`+`junction=roundabout`|A roundabout on a living street|
|roundabout|pedestrian|`highway=pedestrian`+`junction=roundabout`|A pedestrian roundabout|
|roundabout|motorway_link|`highway=motorway_link`+`junction=roundabout`|A roundabout on a link road (sliproad/ramp) leading to/from a motorway from/to a motorway or lower class road|
|roundabout|trunk_link|`highway=trunk_link`+`junction=roundabout`|A roundabout on a link road (sliproad/ramp) leading to/from a trunk road from/to a trunk road or lower class road|
|roundabout|primary_link|`highway=primary_link`+`junction=roundabout`|A roundabout on a link road (sliproad/ramp) leading to/from a primary road from/to a primary road or lower class road|
|roundabout|secondary_link|`highway=secondary_link`+`junction=roundabout`|A roundabout on a link road (sliproad/ramp) leading to/from a secondary road from/to a secondary road or lower class road|
|roundabout|service|`highway=service`+`junction=roundabout`|A roundabout on a service road|
|roundabout|track|`highway=track`+`junction=roundabout`+**`tracktype≠*`**|A roundabout on a track|
|roundabout|grade1|`highway=track`+`junction=roundabout`+`tracktype=grade1`|A roundabout on a grade 1 track|
|roundabout|grade2|`highway=track`+`junction=roundabout`+`tracktype=grade2`|A roundabout on a grade 2 track|
|roundabout|grade3|`highway=track`+`junction=roundabout`+`tracktype=grade3`|A roundabout on a grade 3 track|
|roundabout|grade4|`highway=track`+`junction=roundabout`+`tracktype=grade4`|A roundabout on a grade 4 track|
|roundabout|grade5|`highway=track`+`junction=roundabout`+`tracktype=grade5`|A roundabout on a grade 5 track|
|roundabout|bridleway|`highway=bridleway`+`junction=roundabout`|A roundabout on a bridleway|
|roundabout|cycleway|`highway=cycleway`+`junction=roundabout`|A roundabout on a cycleway|
|roundabout|footway|`highway=footway`+`junction=roundabout`|A roundabout on a designated footpath|
|roundabout|path|`highway=path`+`junction=roundabout`|A roundabout on a non-specific path|
|roundabout|steps|`highway=steps`+`junction=roundabout`|A roundabout on a flights of steps (stairs) on a footway|
|roundabout|roundabout|`junction=roundabout`|A roundabout on a road of other or unkown classification|


## route_l


Various types of "routes" (customary or regular lines of passage or travel, often predetermined and publicized), from bus lines to hiking trails. Not suitable for "routing" (navigation)!

This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|type|text|(see table below)| |


Values of attribute type

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|bicycle|`route=bicycle`|Cycle routes or bicycle route are named or numbered or otherwise signed routes. May go along roads, trails or dedicated cycle paths.|
|bus|`route=bus`|The route of a bus service|
|canoe|`route=canoe`|Route for canoeing through a waterway.|
|detour|`route=detour`|A detour is a named and permanent route you can take if there is a traffic jam on the main route.|
|ferry|`route=ferry`|Displays the route of a ferry on sea.|
|hiking|`route=hiking`|Hiking route is a distinct path that a person may take to walk which is usually often used.|
|horse|`route=horse`|A route that horses can walk on|
|inline_skates|`route=inline_skates`|Inline skate routes are named or numbered or otherwise signed routes. May go along roads, footways or other suitable paths.|
|light_rail|`route=light_rail`|Light rail or light rail transit (LRT) is typically an urban form of public transport often using rolling stock similar to a tramway, but operating primarily along exclusive rights-of-way and having vehicles capable of operating as a single tramcar or as multiple units coupled together to form a train.|
|mtb|`route=mtb`|Mountainbiking route|
|nordic_walking|`route=nordic_walking`|Nordic walking routes are named or numbered or otherwise signed routes.|
|pipeline|`route=pipeline`|For pipelines, pipeline markers, and pipeline stations.|
|piste|`route=piste`|Route of a piste (e.g., snowshoe or XC-Ski trails) in a winter sport area.|
|power|`route=power`|where power lines use the same towers (the same way) most likely in utility_l (power)|
|railway|`route=railway`|All forms of transport using metal rails, including mainline services, subways, heritage lines and trams|
|road|`route=road`|Map various road routes/long roads.|
|running|`route=running`|For running (jogging) routes.|
|ski|`route=ski`|For ski tracks|
|train|`route=train`|Train services|
|tram|`route=tram`|Trams services|
|route|`route=*`|Any route not specified above.|


## traffic_a


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|access|text(later)|For describing the legal accessibility of a element.|`access=*`|
|aggtype|text|Groups (aggregates) several different 'type' values to a common supertype, for a coarser, more general caterorization.| |
|type|text|(see table below)| |


Values of attribute type

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|parking|bicycle|`amenity=bicycle_parking`|A place where bicycles can park|
|fuel|fuel|`amenity=fuel`|Petrol station; gas station; marine fuel|
|parking|multi-storey|`amenity=parking`+`parking=multi-storey`|A building built to park cars on multiple levels|
|parking|parking|`amenity=parking`+`parking=*`|A place for parking cars. This contains any other parking except the specifics below.|
|parking|surface|`amenity=parking`+`parking=surface`|Open area parking normally on ground level|
|parking|underground|`amenity=parking`+`parking=underground`|Carpark is built below the ground level|


## traffic_p


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|access|text(later)|For describing the legal accessibility of a element.|`access=*`|
|aggtype|text|Groups (aggregates) several different 'type' values to a common supertype, for a coarser, more general caterorization.| |
|type|text|(see table below)| |


Values of attribute type

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|barrier|barrier|`barrier=*`|A barrier is a physical structure which blocks or impedes movement. This contains any other barrier except the specifics below.|
|parking|bicycle|`amenity=bicycle_parking`|A place where bicycles can park|
|barrier|block|`barrier=block`|A large, solid, immobile block that can be moved only with heavy machinery or great effort. Typically big solid things made of concrete for stopping larger vehicles. Sometimes natural boulders are used for the same purpose.|
|barrier|bollard|`barrier=bollard`|solid (usually concrete or metal) pillar or pillars in the middle of the road to prevent passage by some traffic.|
|traffic_calming|bump|`traffic_calming=bump`|Short bump - length (in direction of travel) about 30 cm or shorter. Spans the entire width of the road, but can have cuts and small gaps left and right for cyclists.|
|barrier|cattle_grid|`barrier=cattle_grid`|Bars in the road surface that allow wheeled vehicles but not animals to cross. Sometimes known as a Texas Gate, even outside of Texas|
|traffic_calming|chicane|`traffic_calming=chicane`|Hazards on the street you have to drive round|
|general_traffic|crossing|`highway=crossing`|Pedestrians can cross a street here|
|traffic_calming|cushion|`traffic_calming=cushion`|A hump with spaces between or several multiple rectangular humps aligned across the road. This allows emergency vehicles, buses (due to their wider axle) and bicycles to pass through without slowing down.|
|barrier|cycle_barrier|`barrier=cycle_barrier`|Barriers to bicycle traffic, most typically a pair of staggered steel bars perpendicular to the way itself whose gaps allow pedestrians to pass.|
|barrier|entrance|`barrier=entrance`|A gap in a linear barrier with nothing that limits passing through|
|barrier|fence|`barrier=fence`|A structure supported by posts driven into the ground and designed to prevent movement across a boundary. It is distinguished from a wall by the lightness of its construction.|
|general_traffic|ford|`highway=ford`|The road crosses through stream or river, vehicles must enter any water.|
|fuel|fuel|`amenity=fuel`|Petrol station; gas station; marine fuel|
|barrier|gate|`barrier=gate`|An entrance that can be opened or closed to get through the barrier.|
|general_traffic|general_traffic|`highway=*`|Contain all other highway except the specifics below.|
|traffic_calming|hump|`traffic_calming=hump`|Similar to a bump, but longer - total length usually 2-4 m (in direction of travel)|
|barrier|kissing_gate|`barrier=kissing_gate`|A gate which allows people to cross, but not livestock.|
|general_traffic|level_crossing|`highway=level_crossing`|A crossing between a railway and a road.|
|barrier|lift_gate|`barrier=lift_gate`|A lift gate (boom barrier) is a bar, or pole pivoted in such a way as to allow the boom to block vehicular access through a controlled point.|
|general_traffic|mini_roundabout|`highway=mini_roundabout`|Similar to roundabouts, but at the center there is either a painted circle or a fully traversable island.|
|general_traffic|motorway_junction|`highway=motorway_junction`|Indicates a junction (UK) or exit (US).|
|parking|multi-storey|`amenity=parking`+`parking=multi-storey`|A building built to park cars on multiple levels|
|parking|parking|`amenity=parking`+`parking=*`|A place for parking cars. This contains any other parking except the specifics below.|
|service|services|`amenity=services`|Generally for access to a building, motorway service station, beach, campsite, industrial estate, business park, etc.|
|general_traffic|speed_camera|`highway=speed_camera`|A fixed road-side or overhead speed camera.|
|barrier|stile|`barrier=stile`|A stile allows pedestrians to cross a wall or fence, but never actually 'opens' the barrier|
|general_traffic|stop|`highway=stop`|A stop sign|
|general_traffic|street_lamp|`highway=street_lamp`|A street light, lamppost, street lamp, light standard, or lamp standard is a raised source of light on the edge of a road, which is turned on or lit at a certain time every night|
|parking|surface|`amenity=parking`+`parking=surface`|Open area parking normally on ground level|
|traffic_calming|table|`traffic_calming=table`|Designed as a long speed hump with a flat section in the middle. The flat section is long enough for all wheels of a passenger car to fit on that section simultaneously. Does not slow as much as a hump and is usually used on roads with residential speed limit. It is known as flat top hump or raised pedestrian crossing.|
|barrier|toll_booth|`barrier=toll_booth`|A road usage toll or fee is collected here.|
|barrier|traffic_calming|`traffic_calming=*`|Describes features used to slow down traffic. This will contain any other traffic calming except the specifics below.|
|general_traffic|traffic_signals|`highway=traffic_signals`|The light that control the traffic|
|general_traffic|turning_circle|`highway=turning_circle`|A turning circle is a rounded, widened area usually, but not necessarily, at the end of a road to facilitate easier turning of a vehicle. Also known as a cul de sac.|
|parking|underground|`amenity=parking`+`parking=underground`|Carpark is built below the ground level|


## transport_a


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|type|text|(see table below)| |


Values of attribute type

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|aerialway|aerialway|`aerialway=*`|All other types of aerialway which is not defined as above|
|other_traffic|aerialway_station|`aerialway=station`|A station, where passengers can enter and/or leave the aerialway|
|aeroway|aeroway|`aeroway=*`|All other types of aeroway which is not defined as above|
|air_traffic|airport|`amenity=airport` or `aeroway=aerodrome`|An Aerodrome (UK), Airport (US)|
|air_traffic|apron|`aeroway=apron`|An apron is the surfaced part of an airport where planes park.|
|bus|bus_station|`amenity=bus_station`|A station is an area designed to access bus.|
|bus|bus_stop|`railway=bus_stop` or `bus=yes`+`public_transport=stop_position`|A bus stop is a place where public buses stop.|
|water_traffic|ferry_terminal|`amenity=ferry_terminal`|Ferry terminal/stop. A place where people/cars/etc. can board and leave a ferry.|
|air_traffic|helipad|`aeroway=helipad`|A place where helicopters can land.|
|railway|railway_halt|`railway=halt` or `public_transport=stop_position`+`train=yes`|A small station, may not have a platform, trains may only stop on request.|
|railway|railway_station|`railway=station`|Railway stations (including main line, light rail, subway, etc.) are places where customers can access railway services|
|air_traffic|runway|`aeroway=runway`|Where airplanes take off and land|
|public_transport|stop_position|`public_transport=stop_position`|Where public transports stop to pick up passengers|
|taxi|taxi_stand|`amenity=taxi`|A place where taxi waits for passengers|
|air_traffic|taxiway|`aeroway=taxiway`|Where airplanes manouevre between runways and parking areas.|


## transport_l


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|type|text|(see table below)| |


Values of attribute type

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|air_traffic|apron|`aeroway=apron`|An apron is the surfaced part of an airport where planes park.|
|air_traffic|runway|`aeroway=runway`|Where airplanes take off and land|
|air_traffic|taxiway|`aeroway=taxiway`|Where airplanes manouevre between runways and parking areas.|


## transport_p


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|type|text|(see table below)| |


Values of attribute type

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|aerialway|aerialway|`aerialway=*`|All other types of aerialway which is not defined as above|
|other_traffic|aerialway_station|`aerialway=station`|A station, where passengers can enter and/or leave the aerialway|
|aeroway|aeroway|`aeroway=*`|All other types of aeroway which is not defined as above|
|air_traffic|airport|`amenity=airport` or `aeroway=aerodrome`|An Aerodrome (UK), Airport (US)|
|air_traffic|apron|`aeroway=apron`|An apron is the surfaced part of an airport where planes park.|
|bus|bus_station|`amenity=bus_station`|A station is an area designed to access bus.|
|bus|bus_stop|`railway=bus_stop` or `bus=yes`+`public_transport=stop_position`|A bus stop is a place where public buses stop.|
|water_traffic|ferry_terminal|`amenity=ferry_terminal`|Ferry terminal/stop. A place where people/cars/etc. can board and leave a ferry.|
|air_traffic|helipad|`aeroway=helipad`|A place where helicopters can land.|
|railway|railway_halt|`railway=halt` or `public_transport=stop_position`+`train=yes`|A small station, may not have a platform, trains may only stop on request.|
|railway|railway_station|`railway=station`|Railway stations (including main line, light rail, subway, etc.) are places where customers can access railway services|
|air_traffic|runway|`aeroway=runway`|Where airplanes take off and land|
|public_transport|stop_position|`public_transport=stop_position`|Where public transports stop to pick up passengers|
|taxi|taxi_stand|`amenity=taxi`|A place where taxi waits for passengers|
|air_traffic|taxiway|`aeroway=taxiway`|Where airplanes manouevre between runways and parking areas.|


## utility_a


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|aggtype|text|Groups (aggregates) several different 'type' values to a common supertype, for a coarser, more general caterorization.| |
|type|text|(see table below)| |


Values of attribute type

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|plant|plant|`power=plant`|The (usually fenced) site of a power plant a.k.a. power station, generating station, or powerhouse (an industrial facility for the generation of energy), enclosing one or more power generators. The individual generators will have aggtype 'station' (see below).|
|tower|tower|`power=tower`|For towers or pylons carrying high voltage electricity cables. Normally constructed from steel latticework but tubular or solid pylons are also commonly used.|
|station|station|`power=generator`|A device used to convert power from one form to another. This contain all other power except the specifics below.|
|station|nuclear|`generator:source=nuclear`+`power=generator`|A nuclear power plant is a thermal power station in which the heat source is one or more nuclear reactors.|
|station|solar|`generator:source=solar`+`power=generator` or `power=generator`+`power_source=photovoltaic`|Solar powerplant does conversion of sunlight into electricity, either directly using photovoltaics (PV), or indirectly using concentrated solar power (CSP).|
|station|fossil|`generator:source=gas`+`power=generator` or `generator:source=coal`+`power=generator`|Using the combustion of fuels to heat the water to in turn spin the generators turbine |
|station|hydro|`generator:source=water`+`power=generator` or `power_source=hydro`|Hydroelectricity is the term referring to electricity generated by hydropower; the production of electrical power through the use of the gravitational force of falling or flowing water. It is the most widely used form of renewable energy.|
|station|wind|`generator:source=wind`+`power=generator` or `power_source=wind`|A wind turbine is a device that converts kinetic energy from the wind into mechanical energy. If the mechanical energy is used to produce electricity, the device may be called a wind generator.|
|substation|substation|`power=station` or `power=substation` or `power=sub_station`|A tag for electricity substations. These provide voltage step-up/step-down, switching, conditioning, etc. Substations may be large facilities (up to several acres) for very high voltage transmission lines or just small buildings or kiosks near the street for low voltage distribution lines|
|transformer|transformer|`power=transformer`|A static device for transferring electric energy by inductive coupling between its windings. Large power transformers are typically located inside substations.|
|man_made|water_works|`man_made=water_works`|Place where drinking water is found and applied to the local waterpipes network.|
|man_made|wastewater_plant|`man_made=wastewater_plant`|Facilities used to treat wastewater|
|man_made|storage_tank|`man_made=storage_tank`|A large holding tank, typically cylindrical.|
|power|power|`power=*`|All other types of power which is not defined as above|


## utility_l


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|frequency|text|The frequency level the power line is running on|`frequency=*`|
|operator|text|Which company is handling this utility_lines|`operator=*`|
|type|text|(see table below)| |
|voltage|text|The voltage level the power line is running on|`voltage=*`|


Values of attribute type

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|power|cable|`power=cable`|A high voltage earth cables|
|power|line|`power=line`|A overground high voltage power line|
|power|minor_cable|`power=minor_underground_cable` or `power=minor_cable`|A smaller line under earth|
|power|minor_line|`power=minor_line`|A smaller overhead line|
|man_made|pipeline|`man_made=pipeline`|A pipe for carrying various fluids, such as water, gas, sewage.|
|power|power|`power=*`|All other power line which is not specific.|


## utility_p


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|aggtype|text|Groups (aggregates) several different 'type' values to a common supertype, for a coarser, more general caterorization.| |
|type|text|(see table below)| |


Values of attribute type

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|plant|plant|`power=plant`|The (usually fenced) site of a power plant a.k.a. power station, generating station, or powerhouse (an industrial facility for the generation of energy), enclosing one or more power generators. The individual generators will have aggtype 'station' (see below).|
|tower|tower|`power=tower`|For towers or pylons carrying high voltage electricity cables. Normally constructed from steel latticework but tubular or solid pylons are also commonly used.|
|station|station|`power=generator`|A device used to convert power from one form to another. This contain all other power except the specifics below.|
|station|nuclear|`generator:source=nuclear`+`power=generator`|A nuclear power plant is a thermal power station in which the heat source is one or more nuclear reactors.|
|station|solar|`generator:source=solar`+`power=generator` or `power=generator`+`power_source=photovoltaic`|Solar powerplant does conversion of sunlight into electricity, either directly using photovoltaics (PV), or indirectly using concentrated solar power (CSP).|
|station|fossil|`generator:source=gas`+`power=generator` or `generator:source=coal`+`power=generator`|Using the combustion of fuels to heat the water to in turn spin the generators turbine |
|station|hydro|`generator:source=water`+`power=generator` or `power_source=hydro`|Hydroelectricity is the term referring to electricity generated by hydropower; the production of electrical power through the use of the gravitational force of falling or flowing water. It is the most widely used form of renewable energy.|
|station|wind|`generator:source=wind`+`power=generator` or `power_source=wind`|A wind turbine is a device that converts kinetic energy from the wind into mechanical energy. If the mechanical energy is used to produce electricity, the device may be called a wind generator.|
|substation|substation|`power=station` or `power=substation` or `power=sub_station`|A tag for electricity substations. These provide voltage step-up/step-down, switching, conditioning, etc. Substations may be large facilities (up to several acres) for very high voltage transmission lines or just small buildings or kiosks near the street for low voltage distribution lines|
|transformer|transformer|`power=transformer`|A static device for transferring electric energy by inductive coupling between its windings. Large power transformers are typically located inside substations.|
|man_made|water_works|`man_made=water_works`|Place where drinking water is found and applied to the local waterpipes network.|
|man_made|wastewater_plant|`man_made=wastewater_plant`|Facilities used to treat wastewater|
|man_made|storage_tank|`man_made=storage_tank`|A large holding tank, typically cylindrical.|
|pole|pole|`power=pole`|For single (often wooden or concrete) poles carrying medium/low voltage electricity cables.|
|power|power|`power=*`|All other types of power which is not defined as above|


## water_a


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|type|text|(see table below)| |


Values of attribute type

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|dam|`waterway=dam`|A wall built across a river or stream to impound the water. A dam normally does not have water flowing over the top of it.|
|marina|`leisure=marina`|For mooring leisure yachts and motor boats|
|pier|`man_made=pier`|A 'bridge into the ocean', usually for recreation.|
|reservoir_covered|`man_made=reservoir_covered`|A covered reservoir is a large man-made tank for holding fresh water|
|riverbank|`waterway=riverbank`|For tagging wide rivers which need to be defined by an area rather than just shown as a linear way.|
|slipway|`leisure=slipway`|Boats can be launched here|
|spring|`natural=spring`|A spring is a point where water naturally surfaces|
|water|`natural=water`|Used to mark body of standing water, such as a lake or pond.|
|waterway|`waterway=*`|Rivers or other kind of waterways. This contains any other water traffic except the specifics below.|
|weir|`waterway=weir`|A barrier built across a river, sometimes to divert water for industrial purposes. Water can still flow over the top.|


## water_l


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|type|int|(see table below)| |
|width|int|The the measurement or extent of something from side to side; the lesser of two or the least of three dimensions of a body.|`width=*`|


Values of attribute type

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|river|`waterway=river`|A large natural stream of water flowing in a channel to the sea, a lake, or another river.|
|stream|`waterway=stream`|A small and narrow river.|
|canal|`waterway=canal`|An artificial waterway constructed to allow the passage of boats or ships inland or to convey water for irrigation.|
|drain|`waterway=drain`|A channel or pipe carrying off any excess liquid.|
|waterway|`waterway=*`|Other waterways which is user-defined|
|pier|`man_made=pier`|A 'bridge into the ocean', usually for recreation.|


## water_p


This layer has the [common attributes](#common-attributes) as well as the following attributes:

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|type|text|(see table below)| |


Values of attribute type

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|dam|`waterway=dam`|A wall built across a river or stream to impound the water. A dam normally does not have water flowing over the top of it.|
|lock_gate|`waterway=lock_gate`|Top or bottom gate of a lock. (A Lock is a device for raising and lowering boats between stretches of water of different levels on river and canal waterways.)|
|marina|`leisure=marina`|For mooring leisure yachts and motor boats|
|pier|`man_made=pier`|A 'bridge into the ocean', usually for recreation.|
|reservoir_covered|`man_made=reservoir_covered`|A covered reservoir is a large man-made tank for holding fresh water|
|riverbank|`waterway=riverbank`|For tagging wide rivers which need to be defined by an area rather than just shown as a linear way.|
|slipway|`leisure=slipway`|Boats can be launched here|
|spring|`natural=spring`|A spring is a point where water naturally surfaces|
|water|`natural=water`|Used to mark body of standing water, such as a lake or pond.|
|waterfall|`waterway=waterfall`|A waterfall is a place where water flows over a vertical drop in the course of a stream or river.|
|waterway|`waterway=*`|Rivers or other kind of waterways. This contains any other water traffic except the specifics below.|
|weir|`waterway=weir`|A barrier built across a river, sometimes to divert water for industrial purposes. Water can still flow over the top.|


## landmass_a

Pre-processed data from [OpenStreetMapData 'Land polygons'](http://openstreetmapdata.com/data/land-polygons)

This layer _only_ has the following attributes (it _doesn't_ feature the [common attributes](#common-attributes)):

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|fid|int| | |

## coastline_l

Pre-processed data from [OpenStreetMapData 'Coastlines'](http://openstreetmapdata.com/data/coastlines)

This layer _only_ has the following attributes (it _doesn't_ feature the [common attributes](#common-attributes)):

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|fid|int| | |

## sea_a

Pre-processed data from [OpenStreetMapData 'Water polygons'](http://openstreetmapdata.com/data/water-polygons)

This layer _only_ has the following attributes (it _doesn't_ feature the [common attributes](#common-attributes)):

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|fid|int| | |

