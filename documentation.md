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
* osm2pgsql generates areas/polygons out of ways and relations. These objects get negative 
  values of the way or the relation.  
* osm2pgsql splits ways which are too long  
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

These attributes are common to all tables (eventually except table from external sources).


|Attribute   |Data Type         |Description                                   |Osm Tags       |
| ---------- | ---------------- | -------------------------------------------- | ------------- |
|osm_id|bigint|The id taken over from OSM elements node, way or relationship. The uniqueness is only within an OSM element. OSM does not guarantee uniqueness. But its often the only id one can get from the origin.  osm2pgsql generates negative osm_ids when areas are created from relations. And osm2pgsql creates sometimes duplicates by splitting large ways.|osm_id=*|
|lastchange |timestamp without time zone |The timestamp of the last time the feature was changed (UTC)|osm_lastchange=* | 
|geomtype|varchar(1)|This will define weather it is a node (“N”), a way (“W”) or a relation (“R”). Self derivitive not from OSM database.|(n/a)|
|geom|geometry(geometry, 4326)|The “geometry” of the feature can be POINT, MULTILINESTRING or MULTIPOLYGON|way=*|
|type|text(Enum)|This will define the feature type| |
|name|text|The name shich is in general use (which means cyrillic, arabic etc.)|name=* |
|name_intl|text|The name which is written in english, international|Coalesce(name:en, int_name, name:fr,name:es,name:de, name)|
|name_fr|text|The name which is written in french|name:fr=*|
|name_es|text|The name which is written in spanish|name:es=*|
|name_de|text|The name which is written in german|name:de=*|
|name_int|text|The international name of the feature|int_name=*|
|label|text|Translated name through transliterated| |


 

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

## adminarea_a


 Values of attributes type  

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|national_park|boundary='national_park' |A national park is a relatively large area of land declared by a government, to be set aside for human recreation and enjoyment, animal and environmental protection.|
|admin_level1|boundary='administrative' admin_level='1'|Efnahags-loegsaga(Exclusive Economic Zone) use in Iceland|
|national|boundary='administrative' admin_level='2'|National border of a country which is listed based on ISO 3166 standard.(Note: Some dependent territories and special areas of geographical interest which do have their own ISO 3166-1 code but aren't a country).|
|admin_level3|boundary='administrative' admin_level='3'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level4|boundary='administrative' admin_level='4'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level5|boundary='administrative' admin_level='5'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level6|boundary='administrative' admin_level='6'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level7|boundary='administrative' admin_level='7'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level8|boundary='administrative' admin_level='8'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level9|boundary='administrative' admin_level='9'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level10|boundary='administrative' admin_level='10'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level11|boundary='administrative' admin_level='11'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|protected_area|boundary='protected_area' |Protected areas, such as for national-parks, water protection areas or indigenous areas.|
|administrative|admin_level=* |All empty or User input admin_level values to be placed under|



## boundary_l


 Values of attributes type  

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|national_park|boundary='national_park' |A national park is a relatively large area of land declared by a government, to be set aside for human recreation and enjoyment, animal and environmental protection.|
|admin_level1|boundary='administrative' admin_level='1'|Efnahags-loegsaga(Exclusive Economic Zone) use in Iceland|
|national|boundary='administrative' admin_level='2'|National border of a country which is listed based on ISO 3166 standard.(Note: Some dependent territories and special areas of geographical interest which do have their own ISO 3166-1 code but aren't a country).|
|admin_level3|boundary='administrative' admin_level='3'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level4|boundary='administrative' admin_level='4'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level5|boundary='administrative' admin_level='5'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level6|boundary='administrative' admin_level='6'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level7|boundary='administrative' admin_level='7'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level8|boundary='administrative' admin_level='8'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level9|boundary='administrative' admin_level='9'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level10|boundary='administrative' admin_level='10'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|admin_level11|boundary='administrative' admin_level='11'|Considered as subnational borders where it can be specified as parish, district, region, province and state|
|protected_area|boundary='protected_area' |Protected areas, such as for national-parks, water protection areas or indigenous areas.|
|administrative|admin_level=* |All empty or User input admin_level values to be placed under|



## building_a

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|height|text|Stores the height of the building (Unit Meters)|height=*|

 Values of attributes type  

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|building|building=* |This marks out the size and area of a building.|

## geoname_l

refer to geoname_p

## geoname_p

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|wikipedia|text|Provide a reference to an article in Wikipedia about the feature|wikipedia=*|
|population|int|A rough number of citizens in a given place|population=*|

 Values of attributes type  

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|named_place|area='yes' name=*|A place where is given a name with a given area but no specific type|
|farm|place='farm' |A farm can be a part of a human settlement|
|municipality|place='municipality' |a town or district that has local government.|
|isolated_dwelling|place='isolated_dweilling' |The smallest kind of settlement (1-2 households)|
|hamlet|place='hamlet' |A settlement with less than 100-200 inhabitants.|
|county|place='county' |a territorial division of some countries, forming the chief unit of local administration.|
|suburb|place='suburb' |A part of a town or city with a well-known name and often a distinct identity.|
|village|place='village' |A settlement with between 1,000 and 10,000 inhabitants.|
|islet|place='islet' |A very small island.|
|neighbourhood|place='neighbourhood' |A neighbourhood is a smaller named, geographically localised place within a suburb of a larger city or within a town or village|
|town|place='town' |An important urban centre between a village and a city in size|
|city|place='city' |The largest urban settlement or settlements within the territory.|
|locality|place='locality' |A named place that has no population|
|island|place='island' |An island is any piece of land that is completely surrounded by water and isolated from other significant landmasses.|
|region|place='region' |an area, especially part of a country or the world having definable characteristics but not always fixed boundaries.|
|state|place='state' |A large sub-national political/administrative area.|
|place|place=* |Any other place type that are not sorted to any type above except for area without name.|

## landuse_a

 Values of attributes type  

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|industrial|landuse='industrial' |Predominantly workshops, factories or warehouses|
|meadow|landuse='forest' |An area of land primarily vegetated by grass and other non-woody plants, usually mowed for making hay|
|reservoir|landuse='reservoir' |Man made body of stored water. May be covered or uncovered.|
|retail|landuse='retail' |Predominantly shops|
|farm|landuse='farm' landuse='farmland'|An area of farmland used for tillage and pasture (animals, crops, vegetables, flowers, fruit growing).|
|park|leisure='park' landuse='village_green'|An open, green area for recreation, usually municipal|
|commercial|landuse='commercial' |Predominantly offices, business parks, etc.|
|allotments|landuse='allotments' |A piece of land given over to local residents for growing vegetables and flowers.|
|plant_nursery|landuse='plant_nursery' |Intentional planting of plants maintaining for the production of new plants|
|fishfarm|landuse='fishfarm' |A place where fishes are breeded.|
|greenhouse|landuse='greenhouse_horticulture' |Area used for growing plants in greenhouses|
|recreation_ground|leisure='recreation_ground' landuse='recreation_ground'|An open green space for general recreation, which may include pitches, nets and so on, usually municipal but possibly also private to colleges or companies|
|farmyard|landuse='farmyard' |An area of land with farm buildings like farmhouse, dwellings, farmsteads, sheds, stables, barns, equipment sheds, feed bunkers, etc. Plus the open space in between them and the shrubbery/trees around them.|
|port|landuse='port' |Port area handling commercial traffic|
|landfill|landuse='landfill' |Where waste is collected, sorted or covered over|
|nature_reserve|landuse='nature_reserve' |Protected area of importance for wildlife, flora, fauna or features of geological or other special interest.|
|grass|landuse='grass' |For areas covered with grass.|
|quarry|landuse='quarry' |Surface mineral extraction|
|orchard|landuse='orchard' |Intentional planting of trees or shrubs maintained for food production|
|residential|landuse='residential' |Predominantly houses or apartment buildings|
|vineyard|landuse='vineyard' |A piece of land where grapes are grown.|
|railway|landuse='railway' |for marshalling yards and sidings, railway sheds, bits of grass with old rails and hardware strewn around, train washes, etc...|
|forest|landuse='forest' |Managed forest or woodland plantation|
|military|landuse='military' |For land areas owned/used by the military for whatever purpose|
|basin|landuse='basin' |An area of water that drains into a river.|
|landuse|landuse=* |Get all landuse that is not classified in any table|


## military_p

 Values of attributes type  

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|nuclear_site|military='nuclear_explosion_site' |Nuclear weapons test site|
|training_area|military='training_area' |An area where soldiers train and weapons or other military technology are experimented with or are tested.|
|danger_area|military='danger_area' |Usually a large marked area around something like a firing range, bombing range, etc which can be an exclusion zone.|
|obstacle_course|military='obstacle_course' |A military obstacle course.|
|checkpoint|military='checkpoint' |Place of a possible access to a restricted or secured area, where civilian visitors and vehicles will be controled by a military authority.|
|range|military='range' |Where soldiers practice with their weapons (firing, bombing, artillery).|
|airfield|military='airfield' |A place where military planes take off and land.|
|bunker|military='bunker' |Buildings, often build from concrete, to stand even heavier fire. This includes WW2 pillboxes.|
|naval_base|military='naval_base' |A naval base|
|military|military=* |Any other military type that are not sorted to any type above|
|barracks|military='barracks' |Buildings where soldiers live and work.|

## military_a

refer to military_p

## misc_l

 Values of attributes type  

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|traffic_calming|traffic_calming|traffic_calming=* |Describes features used to slow down traffic. This will contain any other traffic calming except the specifics below.|
|barrier|barrier|barrier=* |A barrier is a physical structure which blocks or impedes movement. This contains any other barrier except the specifics below.|
|traffic_calming|chicane|traffic_calming='chicane' |Hazards on the street you have to drive round|
|barrier|wall|barrier='wall' |A freestanding solid structure designed to restrict or prevent movement across a boundary. Usually made from solid brick, concrete or stone and almost always built so that it is opaque to vision.|
|traffic_calming|hump|traffic_calming='hump' |Similar to a bump, but longer - total length usually 2-4 m (in direction of travel)|
|barrier|retaining_wall|barrier='retaining_wall' |Retaining walls serve to retain the lateral pressure of soil. Right side is bottom, left side is top.|
|traffic_calming|bump|traffic_calming='bump' |Short bump - length (in direction of travel) about 30 cm or shorter. Spans the entire width of the road, but can have cuts and small gaps left and right for cyclists.|
|barrier|city_wall|barrier='city_wall' |A fortification used to defend a city or settlement from potential aggressors. From ancient to modern times, they are used to enclose settlements|
|traffic_calming|cushion|traffic_calming='cushion' |A hump with spaces between or several multiple rectangular humps aligned across the road. This allows emergency vehicles, buses (due to their wider axle) and bicycles to pass through without slowing down.|
|barrier|avalanche_protection|barrier='avalanche_protection' |A variety of linear structures which are placed on steep slopes to hold snow in place.|
|barrier|gate|barrier='gate' |An entrance that can be opened or closed to get through the barrier.|
|barrier|hedge|barrier='hedge' |A line of closely spaced shrubs and bushes, planted and trained in such a way as to form a barrier or to mark the boundary of an area.|
|traffic_calming|table|traffic_calming='table' |Designed as a long speed hump with a flat section in the middle. The flat section is long enough for all wheels of a passenger car to fit on that section simultaneously. Does not slow as much as a hump and is usually used on roads with residential speed limit. It is known as flat top hump or raised pedestrian crossing.|
|barrier|fence|barrier='fence' |A structure supported by posts driven into the ground and designed to prevent movement across a boundary. It is distinguished from a wall by the lightness of its construction.|
|natural|cliff|natural='cliff' |A vertical or almost vertical natural drop in terrain, usually with a bare rock surface.|


## natural_a

 Values of attributes type  

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|scrub|natural='scrub' landuse='scrub'|Uncultivated land covered with bushes or stunted trees.|
|fell|natural='fell' |Bare upper lying uncultivated land principally covered with grass and often grazed.|
|wetland|natural='wetland' |The wetland tag is used for natural areas subject to inundation or with waterlogged ground|
|sinkhole|natural='sinkhole' |A natural depression or hole in the surface topography.|
|bare_rock|natural='bare_rock' |An area with sparse or no vegetation, so that the bedrock becomes visible. NOTE: Will appear only on natural_p but not natural_a|
|wood|natural='wood' |Used for ancient or virgin woodland, with no forestry use.|
|stone|natural='stone' |Freestanding stone; e.g., glacial erratic.|
|natural|natural=* |Any other natural type that are not sorted to any type above|
|glacier|natural='glacier' |A permanent body of ice formed naturally from snow that is moving under its own weight.|
|heath|natural='heath' |A dwarf-shrub habitat, characterised by open, low growing woody vegetation, often dominated by plants of the Ericaceae.|
|mud|natural='mud' |Large area covered with mud|
|sand|natural='sand' |Ground coverage of mostly silica particles, with no or very sparse vegetation.|
|scree|natural='scree' |Unconsolidated angular rocks formed by rockfall and weathering from adjacent rockfaces.|
|moor|natural='moor' |Upland areas, characterised by low-growing vegetation on acidic soils.|
|grassland|natural='grassland' |Where vegetation is dominated by grasses (Poaceae) and other herbaceous (non-woody) plants, except for ornamental grass, mowing for hay, etc. and grazing.|
|cave_entrance|natural='cave_entrance' |The entrance to a cave|
|beach|natural='beach' |Area of shore which is fairly open, slopes smoothly to the water, and is free of trees|


## natural_p

refer to natural_a

## nonop_l

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|z_order|smallint|The layer tag is used to describe vertical relationships between different crossing or overlapping map features. Use this in combination with bridge/tunnel tags when one way passes above or under another one.|layer=*|
|ref|text|Reference number of this road unset for railways.|ref=*|
|status|text|P for Planned; C for underconstruction; D for disused; A for abandoned; this is dependent on the values.| |

 Values of attributes type  

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|railway|railway='planned' railway='construction' railway='disused' railway='abandoned'|Contains railways which are disused, planned, under constructions or abandoned. These type of features will be place in this table to keep the feature but display as not available|
|highway|highway='planned' highway='construction' highway='disused' highway='abandoned'|Contains roads which are disused, planned, under constructions or abandoned. These type of features will be place in this table to keep the feature but display as not available|


## poi_p

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|aggtype|text|Grouping several different 'type' to a common 'type'. (aka enmu)| |
|website|text|Specifying the link to the official website for a feature.|website=*|
|cuisine|text|The type of food served at an eating place.|cuisine=*|
|opening_hours|text|The timing of when something is open or close|opening_hours=*|
|brand|text|The identity of a specific product, service, or business. Often trademarks|brand=*|
|wikipedia|text|Provide a reference to an article in Wikipedia about the feature.|wikipedia=*|
|access|text|The legal accessibility of a element.|access=*|
|phone|text|A telephone number associated with the object.|phone=*|
|tower_type|text|The type of tower|tower:type=*|
|contact_phone|text|Phone number|contact:phone=*|

 Values of attributes type  

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|shop|shop|shop=* |All other types of shop which is not defined as above|
|shop|outdoor|shop='outdoor' |Shop focused on selling garden furniture (sheds, outdoor tables, gates, fences, ...).|
|miscpoi|comm_tower|man_made='tower' tower:type='communication'|Describes the type of tower as communication tower|
|shop|shoes|shop='shoes' |Shop focused on selling shoes|
|destination|wayside_shrine|historic='wayside_shrine' |A historical shrine often showing a religious depiction. Frequently found along the way in Southern Germany, Austria and probably elsewhere.|
|health|social_facility|amenity='social_facility' |Social work is a profession and a social science committed to the pursuit of social justice, to quality of life, and to the development of the full potential of each individual, group and community in a society|
|health|clinic|amenity='clinic' |Medium-sized medical centres with tens of staff; smaller than a hospital and larger than a doctor's practice|
|recycling|paper|recycling:paper='yes' |Container or centre where you can take waste for recycling for paper.|
|leisure|pitch|leisure='pitch' |An area designed for playing a particular sport, normally designated with appropriate markings.|
|public|post_office|amenity='post_office' |Post office building with postal services|
|destination|archaeological_site|historic='archaeological_site' |A place in which evidence of past activity is preserved|
|public|police|amenity='police' |A police station|
|public|townhall|amenity='townhall' |Building where the administration of a village, town or city may be located, or just a community meeting place|
|public|community_centre|amenity='community_centre' |A place mostly used for local events and festivities.|
|health|pharmacy|amenity='pharmacy' |A shop where a pharmacist sells medications|
|kindergarten|kindergarten|amenity='kindergarten' |A place for looking after preschool children and (typically) giving early education.|
|destination|attraction|tourism='attraction' |A general place of interest for visitors. Typically used for its natural or historical significance.|
|tourism|board|tourism='information' information='board'|A board with information|
|public|prison|amenity='prison' |A prison|
|shop|stationery|shop='stationery' |Shop focused on selling office supplies|
|shop|garden_centre|shop='garden_centre' |Shop focused on selling potted flowers, maybe even trees|
|miscpoi|water_well|man_made='water_well' |A water well is an excavation or structure created in the ground by digging, driving, boring or drilling to access groundwater in underground aquifers.|
|destination|viewpoint|tourism='viewpoint' |A place for visitors, often high, with good a scenery view of the surrounding countryside or notable buildings.|
|public|government|amenity='government' |Government buildings|
|shop|department_store|shop='department_store' |A single large store - often multiple storeys high - selling a large variety of goods|
|leisure|golf_course|leisure='golf_course' |A place or area where you can play golf.|
|leisure|leisure|leisure=* |All other types of leisure which is not defined as above|
|miscpoi|waste_basket|amenity='waste_backet' |A single small container for depositing garbage that is easily accessible for pedestrians.|
|historic|historic|historic=* |All other types of historic which is not defined as above|
|destination|artwork|tourism='artwork' |Used to tag public pieces of art. Usually such artwork are outdoors.|
|catering|bar|amenity='bar' |Bar is a purpose-built commercial establishment that sells alcoholic drinks to be consumed on the premises. They are characterised by a noisy and vibrant atmosphere, similar to a party and usually don't sell food.|
|tourism|tourism|tourism=* |All other types of tourism which is not defined as above|
|vending|vending_parking|vending='parking_tickets' |A machine selling tickets for parking|
|money|bank|amenity='bank' |Shows the location of a bank branch.|
|shop|furniture|shop='furniture' |Shop focused on selling furniture, might range from small decoration items to a whole flat interior|
|education|school|amenity='school' |Institution designed for learning under the supervision of teachers.|
|vending|vending|amenity='vending_machine' vending=*|A general machine to vend goods, tickets and so on|
|shop|optician|shop='optician' |Shop focused on selling eyeglasses, contact lenses|
|shop|gift|shop='gift' |Shop focused on selling gifts, greeting cards, or tourist gifts (souvenirs)|
|education|university|amenity='university' |An educational institution designed for instruction, examination, or both, of students in many branches of advanced learning.|
|shop|convenience|shop='convenience' |A small local shop carrying a small subset of the items you would find in a supermarket|
|public|embassy|amenity='embassy' |A representation of a country in another country.|
|miscpoi|observation_tower|man_made='observation_tower' tower:type='observation'|One use of an Observation tower is a tower that used to watch for and report forest fire.|
|shop|greengrocer|shop='greengrocer' |Shop focused on selling vegetables and fruits.|
|destination|ruins|historic='ruins' |Remains of structures that were once complete, but have fallen into partial or complete disrepair.|
|shop|clothes|shop='clothes' |Shop focused on selling clothes|
|destination|battlefield|historic='battlefield' |The site of a battle or military skirmish in the past. This could be on land or at sea.|
|shop|bicycle|shop='bicycle' |Shop focused on selling bicycles, bicycle equipment and may rent or repair them|
|public|fire_station|amenity='fire_station' |A fire station|
|shop|newsagent|shop='newsagent' |Shop focused on selling newspapers, cigarettes, other goods|
|public|library|amenity='library' |A public library (municipal, university) to borrow books from.|
|miscpoi|emergency_access|highway='emergency_access_point' |Sign number which can be used to define you current position in case of an emergency|
|shop|books|shop='books' |Shop focused on selling books|
|education|college|amenity='college' |A place for further education usually a post-secondary education institution|
|sport|sport|sport=* |All other types of sport which is not defined as above|
|accommodation_in|guest_house|tourism='guest_house' tourism='bed_and_breakfast'|Accommodation without hotel license that is typically owner-operated, offers a room and breakfast with staff not available 24/7, ranging from purpose-built guest houses to family-based Bed & Breakfast.|
|accommodation_in|hostel|tourism='hostel' |Provide inexpensive accommodation, typically with them having shared bedrooms, bathrooms, kitchens, and lounges.|
|accommodation_out|alpine_hut|tourism='alpine_hut' |a mountain hut is a remote building positioned in the mountains designed to provided lodging accommodation for mountaineers, climbers and hikers. The access is usually restricted to foot, mountain bike or ski.|
|catering|food_court|amenity='food_court' |An area with several different restaurant food counters and a shared eating area|
|public|mortuary|amenity='mortuary' |A morgue or mortuary is a building or room (as in a hospital) used for the storage of human corpses awaiting identification, or removal for autopsy, burial, cremation or some other post-death ritual.|
|accommodation_in|motel|tourism='motel' |It's an establishment that provides accommodation designed for motorists usually on a short-term basis, with convenient parking for motor cars at or close to the room.|
|health|veterinary|amenity='veterinary' |It is a place where there is a certified doctor that deals with the prevention, diagnosis and treatment of disease, disorder and injury in animals is stationed.|
|man_made|man_made|man_made=* |All other types of man_made which is not defined as above|
|miscpoi|fountain|amenity='fountain' |A fountain for cultural / decoration / recreational purposes.|
|leisure|playground|amenity='playground' |These are commonly small outdoor areas with children's play equipment such as swings, climbing frames and roundabouts.|
|tourism|guidepost|tourism='information' information='guidepost'|Signposts/Guideposts are often found along official hiking/cycling routes to indicate the directions to different destinations|
|catering|fast_food|amenity='fast_food' |Is for a place concentrating on very fast counter-only service and take-away food.|
|shop|hairdresser|shop='hairdresser' |Here you can get your hair cut, coloured,|
|public|post_box|amenity='post_box' |A box for the reception of mail.|
|shop|beverages|shop='beverages' shop='alcohol'|Shop focused on selling alcoholic and non-alcoholic beverages.|
|leisure|water_park|leisure='water_park' |An amusement area with water slides, recreational swimming pools and dressing rooms.|
|catering|pub|amenity='pub' |A place selling beer and other alcoholic drinks; may also provide food or accommodation|
|shop|supermarket|shop='supermarket' |A large store for groceries and other goods.|
|catering|biergarten|amenity='biergarten' |Biergarten or beer garden is an open-air area where alcoholic beverages along with food is prepared and served.|
|miscpoi|tower|man_made='tower' |A tall and often lean building or structure e.g. telecoms. All tower except below specifics.|
|shop|bicycle_rental|amenity='bicycle_rental' |A place to rent a bicycle|
|public|courthouse|amenity='courthouse' |A place where justice is dispensed|
|destination|zoo|tourism='zoo' |A zoological garden or park that has confined animals on display for viewing by the public.|
|catering|restaurant|amenity='restaurant' |Is for a generally formal place with sit-down facilities selling full meals served by waiters and often licensed (where allowed) to sell alcoholic drinks.|
|money|atm|amenity='atm' |A device that provides the clients of a financial institution with access to financial transactions.|
|leisure|nightclub|amenity='nightclub' |A nightclub is a place to dance and drink at night.|
|destination|castle|historic='castle' |Castles are (often fortified) buildings from medieval and modern times|
|health|hospital|amenity='hospital' |Institutions for health care providing treatment by specialised staff and equipment, and often but not always providing for longer-term patient stays.|
|public|marketplace|amenity='marketplace' |A place where trade is regulated.|
|public|nursing_home|amenity='nursing_home' |A home for disabled or elderly persons who need permanent care.|
|shop|toys|shop='toys' |Shop focused on selling toys.|
|shop|florist|shop='florist' |Shop focused on selling bouquets of flowers|
|shop|car_sharing|amenity='car_sharing' |A place to share a car|
|miscpoi|bench|amenity='bench' |A bench to sit down and relax a bit|
|destination|wayside_cross|historic='wayside_cross' |A historical (usually Christian) cross. Frequently found along the way in Southern Germany, Austria and probably elsewhere.|
|miscpoi|lighthouse|man_made='lighthouse' |Sends out a light beam to guide ships.|
|leisure|soccer_pitch|sport='soccer' |An area designed for playing a particular sport, normally designated with appropriate markings for soccer.|
|destination|museum|tourism='museum' |An institution which has exhibitions on scientific, historical, artistic, or cultural artefacts.|
|shop|sports|shop='sports' |Shop focused on selling sporting goods.|
|shop|car_rental|amenity='car_rental' |A place to rent a car|
|leisure|tennis_pitch|sport='tennis' |An area designed for playing a particular sport, normally designated with appropriate markings for tennis.|
|miscpoi|drinking_water|amenity='drinking_water' |Drinking water is a place where humans can obtain potable water for consumption. Typically, the water is used for only drinking. Also known as a drinking fountain or water tap.|
|shop|mobile_phone|shop='mobile_phone' |Shop focused on selling mobile phones and accessories|
|leisure|stadium|leisure='stadium' |A major sports arena with substantial tiered seating.|
|public|graveyard|amenity='prison' landuse='cemetery'|A (smaller) place of burial, often you'll find a church nearby. Large places are usually cemetery.|
|accommodation_in|hotel|tourism='hotel' |provide accommodation for guests with usually numbered rooms. Some facilities provided may include a basic bed, storage for clothing and additional guest facilities may include swimming pool, childcare, and conference facilities.|
|shop|kiosk|shop='kiosk' |A small shop on the pavement that sells magazines, tobacco, newspapers, sweets and stamps.|
|recycling|glass|recycling:glass='yes' |Container or centre where you can take waste for recycling for glass.|
|health|dentist|amenity='dentist' |A place where a professional dental surgeon who specializes in the diagnosis, prevention, and treatment of diseases and conditions on oral care is stationed.|
|miscpoi|water_works|man_made='water_works' |A place where drinking water is found and applied to the local water pipes network.|
|health|doctors|amenity='doctors' |A Doctor's Office is a place you can go to get medical attention or a check up|
|destination|fort|historic='fort' |A military fort - distinct from a castle as it is generally more modern|
|leisure|dog_park|amenity='dog_park' |Designated area, with or without a fenced boundary, where dog-owners are permitted to exercise their pets unrestrained|
|miscpoi|hunting_stand|amenity='hunting_stand' |Hunting stands are open or enclosed platforms used by hunters to place themselves at an elevated height above the terrain.|
|destination|theme_park|tourism='theme_park' |An area where entertainment is provided by rides, game concessions, etc., catering to large numbers to people.|
|shop|car|shop='car' |Car store - a place to buy cars or to get your car repaired|
|shop|mall|shop='mall' |A shopping mall - multiple stores under one roof (also known as a shopping centre)|
|shop|computer|shop='computer' |Shop focused on selling computers, peripherals, software,|
|miscpoi|watermill|man_made='watermill' |traditional Watermill, mostly ancient and out of order.|
|destination|monument|historic='museum' |An object, especially large and made of stone, built to remember and show respect to a person or group of people|
|shop|video|shop='video' |Shop focused on selling or renting out videos/DVDs.|
|miscpoi|toilet|amenity='toilets' |A public accessible toilets|
|amenity|amenity|amenity=* |All other types of amenity which is not defined as above|
|recycling|general_reclycling|amenity='recycling' |Container or centre where you can take waste for recycling.|
|education|public_building|amenity='public_building' |A generic public building. (Maybe abandoned by osm but still have data concerning this)|
|leisure|cinema|amenity='cinema' |Cinema/movie theatre - place for showing movies.|
|leisure|sport_centre|amenity='sport_centre' |A distinct facility where a range of sports take place within an enclosed area.|
|shop|car_wash|amenity='car_wash' |A place to wash a car|
|public|telephone|amenity='telephone' |Public telephone|
|shop|travel_agency|amenity='travel_agency' |Shop focused on selling tickets for travelling.|
|shop|hardware|shop='doityourself' shop='hardware'|Shop focused on selling tools and supplies to do-it-yourself householders, gardening,|
|miscpoi|wastewater_plant|man_made='wastewater_plant' |Facilities used to treat wastewater (known as sewage in some countries).|
|accommodation_in|chalet|tourism='chalet' |is a type of accommodation used in the hospitality industry to describe one or more detached cottages with self-contained cooking facilities and/or bathroom and toilet facilities.|
|leisure|theatre|amenity='theatre' |Place where live theatrical performances are held.|
|catering|cafe|amenity='cafe' |Generally informal place with sit-down facilities selling beverages and light meals and/or snacks.|
|money|money_changer|amenity='bureau_de_change' |A place to change foreign bank notes and travellers cheques|
|shop|cair_repair|shop='car_repair' |Shop focused on car repair (usually independent of a specific car brand).|
|tourism|information|tourism='information' |An information source for tourists, travellers and visitors|
|vending|vending_cigarette|vending='cigarettes' |A cigarette machine is a vending machine that dispenses packets of cigarettes.|
|shop|butcher|shop='butcher' |Shop focused on selling meat|
|miscpoi|surveillance|man_made='surveillance' |To mark places and buildings monitored by public or private camera.|
|accommodation_out|caravan_site|tourism='caravan_site' |an area where people with caravans, motorhomes, recreational vehicles can stay overnight, or longer, in allotted spaces known as 'pitches' or 'sites'. They usually provide facilities including toilets, waste disposal, water supply, power supply etc.|
|public|arts_centre|amenity='arts_centre' |A venue where a variety of arts are performed or conducted|
|shop|chemist|shop='chemist' |Shop focused on selling articles of personal hygiene, cosmetics, and household cleaning products|
|miscpoi|windmill|man_made='windmill' |Windmill, mostly ancient and out of order|
|tourism|map|tourism='information' information='map'|A board with a map.|
|shop|laundry|shop='laundry' shop='dry_cleaning'|A shop to get your normal clothes washed and dry. Might be self-service coin operated, with service staff for drop off or it could be a Shop or kiosk offering a clothes cleaning service. The actual cleaning may be done elsewhere.|
|shop|beauty|shop='beauty' |A non-hairdresser beauty shop, spa, nail salon, etc..|
|accommodation_in|shelter|amenity='shelter' |Small place to protect against bad weather conditions|
|destination|picnic_site|tourism='picnic_site' |An area that is suitable for eating outdoors and may have a number of facilities within it.|
|miscpoi|emergency_phone|amenity='emergency_phone' emergency='phone'|A telephone dedicated to emergency calls|
|leisure|ice_rink|leisure='ice_rink' |A place where you can skate or play ice hockey.|
|miscpoi|water_tower|man_made='water_tower' |A tower to store water in, usually found on hills beside or in a town.|
|shop|jewelry|shop='jewelry' |Jewellers shops.|
|miscpoi|fire_hydrant|amenity='fire_hydrant' emergency='fire_hydrant'|A fire hydrant is an active fire protection measure, and a source of water provided in most urban, suburban and rural areas with municipal water service to enable firefighters to tap into the municipal water supply to assist in extinguishing a fire.|
|recycling|metal|recycling:metal='yes' |Container or centre where you can take waste for recycling for metal.|
|destination|memorial|historic='museum' |Much like a monument, but smaller. Might range from a WWII memorial to a simple plate on a wall.|
|leisure|swimming_pool|amenity='swimming_pool' leisure='swimming_pool'|A swimming pool is a place built for swimming as a recreational activity or sport, typically taking the form of an excavated and lined pool|
|shop|bakery|shop='bakery' |Shop focused on selling bread|
|accommodation_out|camp_site|tourism='camp_site' |an area where people can temporarily use a shelter, such as a tent, camper van or sometimes a caravan. Typically, the area is spilt into 'pitches' or 'sites'.|


## poi_a

refer to poi_p

## pow_p

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|aggtype|text|Grouping several different 'type' to a common 'type'. (aka enmu)| |
|website|text|Specifying the link to the official website for a feature.|website=*|
|opening_hours|text|The timing of when something is open or close|opening_hours=*|
|wikipedia|text|Provide a reference to an article in Wikipedia about the feature.|wikipedia=*|
|access|text|The legal accessibility of a element.|access=*|
|phone|text|A telephone number associated with the object.|phone=*|
|contact_phone|text|Phone number|contact:phone=*|

 Values of attributes type  

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|christian|anglican|religion='christian' denomination='anglican'|A christian place of worship with denomination|
|christian|presbyterian|religion='christian' denomination='presbyterian'|A christian place of worship with denomination|
|muslim|shia|religion='muslim' denomination='shia'|A muslim place of worship with denomination.|
|christian|christian|religion='christian' denomination=*|A christian place of worship. This is a generalise christian type other then the specific denomination|
|christian|lutheran|religion='christian' denomination='lutheran'|A christian place of worship with denomination|
|jewish|jewish|religion='jewish' |A jewish place of worship|
|christian|mormon|religion='christian' denomination='mormon'|A christian place of worship with denomination|
|muslim|muslim|religion='muslim' denomination=*|A muslim place of worship. This is a generalise muslim type other then the specific denomination|
|christian|methodist|religion='christian' denomination='methodist'|A christian place of worship with denomination|
|christian|protestant|religion='christian' denomination='protestant'|A christian place of worship with denomination|
|taoist|taoist|religion='taoist' |A taoist place of worship|
|muslim|sunni|religion='muslim' denomination='sunni'|A muslim place of worship with denomination.|
|sikh|sikh|religion='sikh' |A sikh place of worship|
|christian|evangelical|religion='christian' denomination='evangelical'|A christian place of worship with denomination|
|christian|catholic|religion='christian' denomination='catholic'|A christian place of worship with denomination|
|christian|baptist|religion='christian' denomination='baptist'|A christian place of worship with denomination|
|hindu|hindu|religion='hindu' |A hindu place of worship|
|christian|orthodox|religion='christian' denomination='orthodox'|A christian place of worship with denomination|
|buddhist|buddhist|religion='buddhist' |A buddist place of worship|
|shinto|shinto|religion='shinto' |A shinto place of worship|
|place_of_worship|place_of_worship|religion=* amenity='place_of_worship'|A place of worship which is not tag to any of the above.|

## pow_a

refer to pow_p


## railway_bridge_l

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|aggtype|text|Grouping several different 'type' to a common 'type'. (aka enmu)| |
|z_order|smallint|The layer tag is used to describe vertical relationships between different crossing or overlapping map features. Use this in combination with bridge/tunnel tags when one way passes above or under another one. For describing different floors within a building or levels of multilevel parking decks use levels instead of layers.|layer=*|
|bridge|boolean|A bridge is an artificial construction that spans features such as roads, railways, waterways or valleys and carries a road, railway or other feature.|bridge=yes|
|tunnel|boolean|A tunnel is an underground passage for a road or similar.|tunnel=no|
|voltage|text|The voltage level the electrified cable is running on|voltage=*|
|frequency|text|The electrical frequncy that the electrified cable is running on|frequency=*|

railway_bridge_l: bridge = 1
railway_tunnel_l: tunnel = 1
railway_ground_l: bridge = 0, tunnel = 0

 Values of attributes type  

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|railway|narrow_gauge|railway='narrow_gauge' |Narrow-gauge passenger or freight trains.|
|aerialway|zip_line|aerialway='zip_line' |Zip lines, Flying fox and similar|
|railway|tram|railway='tram' |One or two carriage rail vehicles, usually sharing motor road|
|aerialway|drag_lift|aerialway='drag_lift' |an overhead tow-line for skiers and riders.|
|railway|rail|railway='rail' |Full sized passenger or freight trains in the standard gauge for the country or state.|
|aerialway|chair_lift|aerialway='chair_lift' aerialway='high_speed_chair_lift'|Looped cable with a series of single chairs (typically seating two or four people, but can be more). Exposed to the open air (can have a bubble).|
|railway|monorail|railway='monorail' |A railway with only a single rail.|
|railway|subway|railway='subway' |A city passenger rail service running mostly grade separated|
|aerialway|magic_carpet|aerialway='magic_carpet' |Ski lift for small children resembling a conveyor belt.|
|aerialway|t-bar|aerialway='t-bar' |T-bar lift. Overhead tow-line for skiers and riders with T-shaped carriers for two passengers.|
|aerialway|goods|aerialway='goods' |A cable/wire supported lift for goods. Passenger transport is usually not allowed.|
|aerialway|aerialway|aerialway='{}' |All other types of aerialways which is not defined as above|
|aerialway|j-bar|aerialway='t-bar' |J-bar lift or L-bar lift. Overhead tow-line for skiers and riders with carriers in J-shape.|
|railway|funicular|railway='funicular' |Cable driven inclined railways|
|aerialway|gondola|aerialway='gondola' |Many cars on a looped cable.|
|aerialway|cable_car|aerialway='cable_car' |Just one or two large cars. The cable forms a loop, but the cars do not loop around, they just move up and down on their own side.|
|railway|miniature|railway='miniature' |Miniature railways are narrower than narrow gauge and carry passengers. They can be found in parks.|
|railway|light_rail|railway='light_rail' |A higher-standard tram system, normally in its own right-of-way. Often it connects towns and thus reaches a considerable length (tens of kilometer).|
|aerialway|rope_tow|aerialway='rope_tow' |Ski tow lift. Tow-line for skiers and riders where passenger hold by hand or use special tow grabbers.|
|railway|railway|railway='{}' |All other types of railways which is not defined as above|
|aerialway|platter|aerialway='platter' |Platter lift (poma). Overhead tow-line for skiers and riders with platters.|
|aerialway|mixed_lift|aerialway='mixed_lift' |A lift mixed with gondola and chair_lift|


## road_ground_l

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|aggtype|text|Grouping several different 'type' to a common 'type'. (aka enmu)| |
|ref|text|Used for reference numbers or codes.Common for roads, highway exits, routes, etc.|ref=*|
|z_order|smallint|The layer tag is used to describe vertical relationships between different crossing or overlapping map features. Use this in combination with bridge/tunnel tags when one way passes above or under another one. For describing different floors within a building or levels of multilevel parking decks use levels instead of layers.|layer=*|
|maxspeed|smallint|Specifies the maximum legal speed limit on a road, railway or waterway|maxspeed=*|
|oneway|boolean|Oneway streets are streets where you are only allowed to drive in one direction.|oneway=*|
|bridge|boolean|A bridge is an artificial construction that spans features such as roads, railways, waterways or valleys and carries a road, railway or other feature.|bridge=no|
|tunnel|boolean|A tunnel is an underground passage for a road or similar.|tunnel=no|  

railway_bridge_l: bridge = 1
railway_tunnel_l: tunnel = 1
railway_ground_l: bridge = 0, tunnel = 0


 Values of attributes type  

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|roundabout|living_street|hihgway='living_street' junction='roundabout'|For living streets, which are residential streets where pedestrians have legal priority over cars, speeds are kept very low and where children are allowed to play on the street.|
|roundabout|track|hihgway='service' tracktype=*|Roads for agricultural use, gravel roads in the forest etc. and no tracktype tag is present,|
|roundabout|trunk|hihgway='trunk' junction='roundabout'|The most important roads in a country's system that aren't motorways. (Need not necessarily be a divided highway.)|
|roundabout|primary|hihgway='primary' junction='roundabout'|The next most important roads in a country's system. (Often link larger towns.)|
|roundabout|motorway|hihgway='motorway' junction='roundabout'|A restricted access major divided highway, normally with 2 or more running lanes plus emergency hard shoulder. Equivalent to the Freeway, Autobahn, etc..|
|roundabout|pedestrian|hihgway='pedestrian' junction='roundabout'|For roads used mainly/exclusively for pedestrians in shopping and some residential areas which may allow access by motorised vehicles only for very limited periods of the day. To create a 'square' or 'plaza' create a closed way and tag as pedestrian.|
|roundabout|grade3|hihgway='track' tracktype='grade3'|Even mixture of hard and soft materials. Almost always an unpaved track.|
|junction|grade2|hihgway='track' tracktype='grade2'|Mostly solid. Usually an unpaved track with surface of gravel mixed with a varying amount of sand, silt, and clay.|
|roundabout|grade5|hihgway='track' tracktype='grade5'|Soft. Almost always an unpaved track lacking hard materials, uncompacted, subtle on the landscape, with surface of soil/sand/grass.|
|roundabout|grade4|hihgway='track' tracktype='grade4'|Mostly soft. Almost always an unpaved track prominently with soil/sand/grass, but with some hard materials, or compressed materials mixed in.|
|roundabout|bridleway|hihgway='bridleway' junction='roundabout'|For horses.|
|roundabout|secondary_link|hihgway='secondary_link' junction='roundabout'|The link roads (sliproads/ramps) leading to/from a secondary road from/to a secondary road or lower class highway.|
|track|grade1|hihgway='track' tracktype='grade1'|Solid. Usually a paved or heavily compacted hardcore surface.|
|roundabout|path|hihgway='path' junction='roundabout'|A non-specific path.|
|roundabout|tertiary|hihgway='tertiary' junction='roundabout'|The next most important roads in a country's system.|
|roundabout|secondary|hihgway='secondary' junction='roundabout'|The next most important roads in a country's system. (Often link smaller towns and villages.)|
|roundabout|primary_link|hihgway='primary_link' junction='roundabout'|The link roads (sliproads/ramps) leading to/from a primary road from/to a primary road or lower class highway.|
|junction|footway|hihgway='footway' junction='roundabout'|For designated footpaths; i.e., mainly/exclusively for pedestrians. This includes walking tracks and gravel paths.|
|roundabout|service|hihgway='service' junction='roundabout'|For access roads to, or within an industrial estate, camp site, business park, car park etc. Can be used in conjunction with service=* to indicate the type of usage and with access=* to indicate who can use it and in what circumstances.|
|roundabout|residential|hihgway='residential' junction='roundabout'|Roads which are primarily lined with and serve as an access to housing.|
|roundabout|motorway_link|hihgway='motorway_link' junction='roundabout'|The link roads (sliproads/ramps) leading to/from a motorway from/to a motorway or lower class highway. Normally with the same motorway restrictions.|
|junction|cycleway|hihgway='cycleway' junction='roundabout'|Cycling infrastructure that is an inherent part of a road - particularly "cycle lanes" which are a part of the road|
|roundabout|unclassified|hihgway='unclassified' junction='roundabout'|The least most important through roads in a country's system - i.e. minor roads of a lower classification than tertiary, but which serve a purpose other than access to properties. (The word 'unclassified' is a historical artefact of the UK road system and does not mean that the classification is unknown; you can use highway=road for that.)|
|roundabout|steps|hihgway='steps' junction='roundabout'|For flights of steps (stairs) on footways.|
|roundabout|trunk_link|hihgway='trunk_link' junction='roundabout'|The link roads (sliproads/ramps) leading to/from a trunk road from/to a trunk road or lower class highway.|
|unclassified|road|hihgway='{}' roundabout=*|A road where the mapper is unable to ascertain the classification from the information available. This is intended as a temporary tag to mark a road until it has been properly surveyed|
|roundabout|roundabout|hihgway=* junction='roundabout'|This contains any other roundabout except the specifics above.|


## route_l

 Values of attributes type  

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|bicycle|route='bicycle' |Cycle routes or bicycle route are named or numbered or otherwise signed routes. May go along roads, trails or dedicated cycle paths.|
|power|route='power' |where power lines use the same towers (the same way) most likely in utility_l (power)|
|bus|route='bus' |The route of a bus service|
|detour|route='detour' |A detour is a named and permanent route you can take if there is a traffic jam on the main route.|
|nordic_walking|route='nordic_walking' |Nordic walking routes are named or numbered or otherwise signed routes.|
|running|route='running' |For running (jogging) routes.|
|train|route='train' |Train services|
|piste|route='piste' |Route of a piste (e.g., snowshoe or XC-Ski trails) in a winter sport area.|
|inline_skates|route='inline_skates' |Inline skate routes are named or numbered or otherwise signed routes. May go along roads, footways or other suitable paths.|
|horse|route='horse' |A route that horses can walk on|
|hiking|route='hiking' |Hiking route is a distinct path that a person may take to walk which is usually often used.|
|tram|route='tram' |Trams services|
|route|route=* |This contains any other route except the specifics above.|
|campe|route='canoe' |Route for canoeing through a waterway.|
|light_rail|route='light_rail' |Light rail or light rail transit (LRT) is typically an urban form of public transport often using rolling stock similar to a tramway, but operating primarily along exclusive rights-of-way and having vehicles capable of operating as a single tramcar or as multiple units coupled together to form a train.|
|mtb|route='mtb' |Mountainbiking route|
|ferry|route='ferry' |Displays the route of a ferry on sea.|
|railway|route='railway' |All forms of transport using metal rails, including mainline services, subways, heritage lines and trams|
|pipeline|route='pipeline' |For pipelines, pipeline markers, and pipeline stations.|
|ski|route='ski' |For ski tracks|
|road|route='road' |Map various road routes/long roads.|


## traffic_a

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|aggtype|text|Grouping several different 'type' to a common 'type'. (aka enmu)| |
|access|text(later)|For describing the legal accessibility of a element.|access=*|

 Values of attributes type  

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|fuel|fuel|amenity='fuel' |Petrol station; gas station; marine fuel|
|parking|bicycle|amenity='bicycle_parking' |A place where bicycles can park|
|parking|parking|amenity='parking' parking=*|A place for parking cars. This contains any other parking except the specifics below.|
|parking|underground|amenity='parking' parking='underground'|Carpark is built below the ground level|
|parking|multi-storey|amenity='parking' parking='multi-storey'|A building built to park cars on multiple levels|
|parking|surface|amenity='parking' parking='surface'|Open area parking normally on ground level|


## traffic_p

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|aggtype|text|Grouping several different 'type' to a common 'type'. (aka enmu)| |
|access|text(later)|For describing the legal accessibility of a element.|access=*|

 Values of attributes type  

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|barrier|lift_gate|barrier='lift_gate' |A lift gate (boom barrier) is a bar, or pole pivoted in such a way as to allow the boom to block vehicular access through a controlled point.|
|parking|bicycle|amenity='bicycle_parking' |A place where bicycles can park|
|barrier|fence|barrier='fence' |A structure supported by posts driven into the ground and designed to prevent movement across a boundary. It is distinguished from a wall by the lightness of its construction.|
|barrier|cattle_grid|barrier='cattle_grid' |Bars in the road surface that allow wheeled vehicles but not animals to cross. Sometimes known as a Texas Gate, even outside of Texas|
|traffic_calming|bump|traffic_calming='bump' |Short bump - length (in direction of travel) about 30 cm or shorter. Spans the entire width of the road, but can have cuts and small gaps left and right for cyclists.|
|parking|multi-storey|amenity='parking' parking='multi-storey'|A building built to park cars on multiple levels|
|parking|surface|amenity='parking' parking='surface'|Open area parking normally on ground level|
|barrier|stile|barrier='stile' |A stile allows pedestrians to cross a wall or fence, but never actually "opens" the barrier|
|parking|parking|amenity='parking' parking=*|A place for parking cars. This contains any other parking except the specifics below.|
|traffic_calming|table|traffic_calming='table' |Designed as a long speed hump with a flat section in the middle. The flat section is long enough for all wheels of a passenger car to fit on that section simultaneously. Does not slow as much as a hump and is usually used on roads with residential speed limit. It is known as flat top hump or raised pedestrian crossing.|
|general_traffic|mini_roundabout|highway='mini_roundabout' |Similar to roundabouts, but at the center there is either a painted circle or a fully traversable island.|
|barrier|toll_booth|barrier='toll_booth' |A road usage toll or fee is collected here.|
|barrier|barrier|barrier=* |A barrier is a physical structure which blocks or impedes movement. This contains any other barrier except the specifics below.|
|traffic_calming|hump|traffic_calming='hump' |Similar to a bump, but longer - total length usually 2-4 m (in direction of travel)|
|barrier|cycle_barrier|barrier='cycle_barrier' |Barriers to bicycle traffic, most typically a pair of staggered steel bars perpendicular to the way itself whose gaps allow pedestrians to pass.|
|general_traffic|general_traffic|highway=* |Contain all other highway except the specifics below.|
|barrier|bollard|barrier='bollard' |solid (usually concrete or metal) pillar or pillars in the middle of the road to prevent passage by some traffic.|
|fuel|fuel|amenity='fuel' |Petrol station; gas station; marine fuel|
|barrier|gate|barrier='gate' |An entrance that can be opened or closed to get through the barrier.|
|general_traffic|turning_circle|highway='turning_circle' |A turning circle is a rounded, widened area usually, but not necessarily, at the end of a road to facilitate easier turning of a vehicle. Also known as a cul de sac.|
|barrier|entrance|barrier='entrance' |A gap in a linear barrier with nothing that limits passing through|
|general_traffic|speed_camera|highway='speed_camera' |A fixed road-side or overhead speed camera.|
|traffic_calming|chicane|traffic_calming='chicane' |Hazards on the street you have to drive round|
|general_traffic|stop|highway='stop' |A stop sign|
|general_traffic|motorway_junction|highway='motorway_junction' |Indicates a junction (UK) or exit (US).|
|general_traffic|ford|highway='ford' |The road crosses through stream or river, vehicles must enter any water.|
|parking|underground|amenity='parking' parking='underground'|Carpark is built below the ground level|
|general_traffic|level_crossing|highway='level_crossing' |A crossing between a railway and a road.|
|traffic_calming|cushion|traffic_calming='cushion' |A hump with spaces between or several multiple rectangular humps aligned across the road. This allows emergency vehicles, buses (due to their wider axle) and bicycles to pass through without slowing down.|
|service|services|amenity='services' |Generally for access to a building, motorway service station, beach, campsite, industrial estate, business park, etc.|
|general_traffic|street_lamp|highway='street_lamp' |A street light, lamppost, street lamp, light standard, or lamp standard is a raised source of light on the edge of a road, which is turned on or lit at a certain time every night|
|barrier|traffic_calming|traffic_calming=* |Describes features used to slow down traffic. This will contain any other traffic calming except the specifics below.|
|general_traffic|traffic_signals|highway='traffic_signals' |The light that control the traffic|
|barrier|kissing_gate|barrier='kissing_gate' |A gate which allows people to cross, but not livestock.|
|general_traffic|crossing|highway='crossing' |Pedestrians can cross a street here|
|barrier|block|barrier='block' |A large, solid, immobile block that can be moved only with heavy machinery or great effort. Typically big solid things made of concrete for stopping larger vehicles. Sometimes natural boulders are used for the same purpose.|


## transport_a


 Values of attributes type  

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|air_traffic|apron|aeroway='taxiway' |An apron is the surfaced part of an airport where planes park.|
|public_transport|stop_position|public_transport='stop_position' |Where public transports stop to pick up passengers|
|railway|railway_halt|railway='halt' public_transport='stop_position'|A small station, may not have a platform, trains may only stop on request.|
|aerialway|aerialway|aerialway=* |All other types of aerialway which is not defined as above|
|water_traffic|ferry_terminal|amenity='ferry_terminal' |Ferry terminal/stop. A place where people/cars/etc. can board and leave a ferry.|
|air_traffic|runway|aeroway='runway' |Where airplanes take off and land|
|air_traffic|taxiway|aeroway='taxiway' |Where airplanes manouevre between runways and parking areas.|
|bus|bus_stop|railway='bus_stop' public_transport='stop_position'|A bus stop is a place where public buses stop.|
|air_traffic|airport|amenity='taxi' aeroway='aerodrome'|An Aerodrome (UK), Airport (US)|
|railway|railway_station|railway='station' |Railway stations (including main line, light rail, subway, etc.) are places where customers can access railway services|
|taxi|taxi_stand|amenity='taxi' |A place where taxi waits for passengers|
|bus|bus_station|amenity='bus_station' |A station is an area designed to access bus.|
|aeroway|aeroway|aeroway=* |All other types of aeroway which is not defined as above|
|air_traffic|helipad|aeroway='helipad' |A place where helicopters can land.|
|other_traffic|aerialway_station|aerialway='station' |A station, where passengers can enter and/or leave the aerialway|


## utility_a

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|aggtype|text|Grouping several different 'type' to a common 'type'. (aka enmu)| |

 Values of attributes type  

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|substation|substation|power='station' power='substation'|A tag for electricity substations. These provide voltage step-up/step-down, switching, conditioning, etc. Substations may be large facilities (up to several acres) for very high voltage transmission lines or just small buildings or kiosks near the street for low voltage distribution lines|
|transformer|transformer|power='transformer' |A static device for transferring electric energy by inductive coupling between its windings. Large power transformers are typically located inside substations.|
|station|fossil|power='generator' generator:source='gas' or generator:source='coal'|Using the combustion of fuels to heat the water to in turn spin the generators turbine |
|power|power|power=* |All other types of power which is not defined as above|
|station|nuclear|power='generator' and generator:source='nuclear'|A nuclear power plant is a thermal power station in which the heat source is one or more nuclear reactors.|
|man_made|storage_tank|man_made='storage_tank' |A large holding tank, typically cylindrical.|
|man_made|wastewater_plant|man_made='wastewater_plant' |Facilities used to treat wastewater|
|station|station|power='generator' |A device used to convert power from one form to another. This contain all other power except the specifics below.|
|man_made|water_works|man_made='water_works' |Place where drinking water is found and applied to the local waterpipes network.|
|station|solar|(power='generator' and generator:source='solar') or power_source='photovoltaic'|Solar powerplant does conversion of sunlight into electricity, either directly using photovoltaics (PV), or indirectly using concentrated solar power (CSP).|
|tower|tower|power='tower' |For towers or pylons carrying high voltage electricity cables. Normally constructed from steel latticework but tubular or solid pylons are also commonly used.|
|station|wind|(power='generator' and generator:source='wind') or power_source='wind'|A wind turbine is a device that converts kinetic energy from the wind into mechanical energy. If the mechanical energy is used to produce electricity, the device may be called a wind generator.|
|station|hydro|(power='generator' and generator:source='water') or power_source='hydro'|Hydroelectricity is the term referring to electricity generated by hydropower; the production of electrical power through the use of the gravitational force of falling or flowing water. It is the most widely used form of renewable energy.|


## utility_p

 Values of attributes type  

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|pole|pole|power='pole' |For single (often wooden or concrete) poles carrying medium/low voltage electricity cables.|


## utility_l

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|operator|text|Which company is handling this utility_lines|operator=*|
|frequency|text|The frequency level the power line is running on|frequency=*|
|voltage|text|The voltage level the power line is running on|voltage=*|

 Values of attributes type  

|aggtype             |values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |
|man_made|pipeline|man_made='pipeline' |A pipe for carrying various fluids, such as water, gas, sewage.|
|power|minor_cable|power='minor_underground_cable' power='minor_cable'|A smaller line under earth|
|power|power|power=* |All other power line which is not specific.|
|power|cable|power='cable' |A high voltage earth cables|
|power|line|power='line' |A overground high voltage power line|
|power|minor_line|power='minor_line' |A smaller overhead line|


## water_a

 Values of attributes type  

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|spring|natural='spring' |A spring is a point where water naturally surfaces|
|weir|waterway='weir' |A barrier built across a river, sometimes to divert water for industrial purposes. Water can still flow over the top.|
|water|natural='water' |Used to mark body of standing water, such as a lake or pond.|
|slipway|leisure='slipway' |Boats can be launched here|
|reservoir_covered|man_made='reservoir_covered' |A covered reservoir is a large man-made tank for holding fresh water|
|dam|waterway='dam' |A wall built across a river or stream to impound the water. A dam normally does not have water flowing over the top of it.|
|marina|leisure='marina' |For mooring leisure yachts and motor boats|
|waterway|waterway=* |Rivers or other kind of waterways. This contains any other water traffic except the specifics below.|
|pier|man_made='pier' |A "bridge into the ocean", usually for recreation.|
|riverbank|natural='riverbank' |For tagging wide rivers which need to be defined by an area rather than just shown as a linear way.|


## water_p


 Values of attributes type  

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|pier|man_made='pier' |A "bridge into the ocean", usually for recreation.|
|spring|natural='spring' |A spring is a point where water naturally surfaces|
|weir|waterway='weir' |A barrier built across a river, sometimes to divert water for industrial purposes. Water can still flow over the top.|
|water|natural='water' |Used to mark body of standing water, such as a lake or pond.|
|slipway|leisure='slipway' |Boats can be launched here|
|waterfall|waterway='waterfall' |A waterfall is a place where water flows over a vertical drop in the course of a stream or river.|
|reservoir_covered|man_made='reservoir_covered' |A covered reservoir is a large man-made tank for holding fresh water|
|dam|waterway='dam' |A wall built across a river or stream to impound the water. A dam normally does not have water flowing over the top of it.|
|marina|leisure='marina' |For mooring leisure yachts and motor boats|
|waterway|waterway=* |Rivers or other kind of waterways. This contains any other water traffic except the specifics below.|
|lock_gate|man_made='pier' |A "bridge into the ocean", usually for recreation.|
|riverbank|natural='riverbank' |For tagging wide rivers which need to be defined by an area rather than just shown as a linear way.|


## water_l

|Attributes          |type                |Description                                                           |osm_tags            |
| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |
|width|int|The the measurement or extent of something from side to side; the lesser of two or the least of three dimensions of a body.|width=*|

 Values of attributes type  

|values              |osm_tags            |description                                                           |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
|canal|waterway='canal' |An artificial waterway constructed to allow the passage of boats or ships inland or to convey water for irrigation.|
|waterway|waterway=* |Other waterways which is user-defined|
|river|waterway='river' |A large natural stream of water flowing in a channel to the sea, a lake, or another river.|
|stream|waterway='stream' |A small and narrow river.|
|drain|waterway='drain' |A channel or pipe carrying off any excess liquid.|

