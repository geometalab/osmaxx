<Image:>

<Image:>

**Osmaxx Data Model**

**Stefan F. Keller und Eugene J. Phua**

**Version 2 - March 2015**

**Technical Report**

**Geometa Lab at Institute of SoftwareUniversity of Applied Sciences Rapperswil (FHO)**

**CH-8649 Rapperswil**

<Image:>

Table of Contents
=================

[\#\_\_RefHeading\_\_11454\_1447038746 Table of Contents2]

[\#\_\_RefHeading\_\_12090\_1447038746 1.Introduction4]

[\#\_\_RefHeading\_\_12094\_1447038746 1.1.Credits and legal issues4]

[\#\_\_RefHeading\_\_9281\_2087439466 1.2.Goal, scope and limits4]

[\#\_\_RefHeading\_\_9283\_2087439466 1.3.Status of this document and future releases4]

[\#\_\_RefHeading\_\_9303\_2087439466 1.4.How OSM data is being curated (discussion)5]

[\#\_\_RefHeading\_\_12098\_1447038746 2.Specification6]

[\#\_\_RefHeading\_\_12100\_1447038746 2.1.Identifiers6]

[\#\_\_RefHeading\_\_10858\_2068603004 2.2.Metadata6]

[\#\_\_RefHeading\_\_12102\_1447038746 2.3.File Names6]

[\#\_\_RefHeading\_\_12104\_1447038746 2.4.Layer Specification Headers7]

[\#\_\_RefHeading\_\_12106\_1447038746 2.5.Common Attributes7]

[\#\_\_RefHeading\_\_12108\_1447038746 3.Layer Overview9]

[\#\_\_RefHeading\_\_12110\_1447038746 4.Layer Specification11]

[\#\_\_RefHeading\_\_11873\_1266607206 4.1.address\_p11]

[\#\_\_RefHeading\_\_12112\_1447038746 4.2.adminarea\_a11]

[\#\_\_RefHeading\_\_12114\_1447038746 4.3.adminunit\_a12]

[\#\_\_RefHeading\_\_12116\_1447038746 4.4.boundary\_l12]

[\#\_\_RefHeading\_\_12118\_1447038746 4.5.building\_a13]

[\#\_\_RefHeading\_\_11875\_1266607206 4.6.geoname\_l13]

[\#\_\_RefHeading\_\_12136\_1447038746 4.7.geoname\_p13]

[\#\_\_RefHeading\_\_12122\_1447038746 4.8.landuse\_a14]

[\#\_\_RefHeading\_\_12124\_1447038746 4.9.military\_a16]

[\#\_\_RefHeading\_\_12126\_1447038746 4.10.military\_p16]

[\#\_\_RefHeading\_\_11877\_1266607206 4.11.misc\_l17]

[\#\_\_RefHeading\_\_12128\_1447038746 4.12.natural\_a19]

[\#\_\_RefHeading\_\_12130\_1447038746 4.13.natural\_p20]

[\#\_\_RefHeading\_\_12132\_1447038746 4.14.nonop\_l21]

[\#\_\_RefHeading\_\_11879\_1266607206 4.15.poi\_a21]

[\#\_\_RefHeading\_\_12144\_1447038746 4.16.poi\_p21]

[\#\_\_RefHeading\_\_11881\_1266607206 4.17.pow\_a35]

[\#\_\_RefHeading\_\_12140\_1447038746 4.18.pow\_p36]

[\#\_\_RefHeading\_\_12156\_1447038746 4.19.railway\_l37]

[\#\_\_RefHeading\_\_12158\_1447038746 4.20.road\_l39]

[\#\_\_RefHeading\_\_12160\_1447038746 4.21.route\_l45]

[\#\_\_RefHeading\_\_12162\_1447038746 4.22.traffic\_a46]

[\#\_\_RefHeading\_\_12164\_1447038746 4.23.traffic\_p46]

[\#\_\_RefHeading\_\_11883\_1266607206 4.24.transport\_a50]

[\#\_\_RefHeading\_\_12154\_1447038746 4.25.transport\_p51]

[\#\_\_RefHeading\_\_11885\_1266607206 4.26.utility\_a52]

[\#\_\_RefHeading\_\_12148\_1447038746 4.27.utility\_p54]

[\#\_\_RefHeading\_\_12150\_1447038746 4.28.utility\_l55]

[\#\_\_RefHeading\_\_12166\_1447038746 4.29.water\_a56]

[\#\_\_RefHeading\_\_9285\_2087439466 4.30.water\_p56]

[\#\_\_RefHeading\_\_12168\_1447038746 4.31.water\_l57]

[\#\_\_RefHeading\_\_12170\_1447038746 5.Appendix59]

[\#\_\_RefHeading\_\_9305\_2087439466 5.1.Glossary59]This technical report is published under the license of CC-BY-CA and edited by LibreOffice and Arial font.

Contact: Prof. Stefan Keller, sfkeller-at-hsr-dot-ch

Revision History:

-   2015-02-13 V.1 Draft
-   2015-03-15V.2

Introduction
============

Credits and legal issues
------------------------

Credits go to OpenSteetMap and to Geofabrik.

This document is licensed under CC-BY-SA.

The data referred to is from OpenStreetMap planet file licensed under ODbL 1.0.

Goal, scope and limits
----------------------

Notes regarding limits, quality and out of scope of the data model and the related datasets.

Goal and scope: Das Osmaxx-Datenmodell ist zur möglichst breiten Nutzung ausgelegt (Kartendarstellung, Orientierung, POI-Suche und räumliche Analyse und später Routing). D.h. es wird versucht, so viele Informationen (Tabellen, Attribute und Wertebereiche) wie möglich aus OSM herauszuholen, die einigermassen konsistent erfasst werden bzw. die sich filtern („Cleansing“ und Homogenisierung) oder aus den Daten herleiten lassen („Data Curation“). Das ist zwangsläufig mehr, als beispielsweise für die (gedruckte) Kartendarstellung eines topografischen Landschaftsmodells nötig ist.

These are known limits, omissions and bugs:

1.  Current data export exports POLYGON instead of MULTPOLYGON
2.  Statistics is missing
3.  Missing tables: coastline\_l, adminunit\_a
4.  tbd.

Tbd.

Status of this document and future releases
-------------------------------------------

This document and the project just started and thus is in e pre-mature state.

These are possible enhancements in next releases

-   File STATISTICS.txt which contains a report about tables, attributes and it's rows and values.
-   Final data model (V.3?)
-   Adding attribute height to tables like poi\_p from external digital terrain model data like SRTM3.
-   Routing (see e.g. table route\_l)

How OSM data is being curated (discussion)
------------------------------------------

Semicolons in tag values:

-   Data value will be changed to ‘others’ for such events

Data Cleaning:

-   Spelling errors
-   Upper case errors
-   Values singular and plural
-   Handling values which contains words

Elevation: Elevation values will not be set in this release.

Type='others'. Data value will be change to ‘others’ as it cannot be categorized. This is introduced to ensure values that are misspelled, concatenated, illegible or user defined are sorted accordingly into their table. Seeing this type of value given to some feature is due to a few reasons. 1) Data is not in the list of core value to be considered. 2) Value is being given by users where we might know understand the value significance.

Grouping of features. unable to group features like airports and power station as buildings are not defined to specific areas to be able to group them together.

Multiple Table. There are instances where different table can contain the same feature. e.g. buildings\_a and poi\_a (like campus areas or school areas) where it can overlap one another. This have not been resolve, therefore, users do take note of double entry.

'Refer to *table*'. This is to keep the documentation short and not allowing it to repeat the common attribute value which is similar to other table.

Administrative boundary extracted on the fly and placed into boundary\_l table but these are without warranty to be consistent. There exist other sources with validated boundaries including country borders and coastlines.

Landcover contains partial landuse elements while some landcover elements are put into natural or water.

Building addresses are not yet handled due to the complexity of this issue.

Specification
=============

Identifiers
-----------

The original OSM schema contains an id (type bigint) for every element node,way and relation. This OSM id is mapped to attribute osm\_id (see chapter “Common Attributes”). The id in OSM is not stable but often the only one, one can work with. During transformation I can happen that thie osm\_id is being changed or duplicated:

-   osm2pgsql generates areas/polygons out of ways and relations. These objects get negative values of the way or the relation.
-   osm2pgsql splits ways which are too long
-   tags can contain many values separated by semicolon (e.g. “shop=a;b”); this object may be split into two for each shop-value (“shop=a” and “shop=b”) while the osm\_id os maintained.

Metadata
--------

-   -   Datum (coordinate reference system) of data: WGS84 (EPSG: 4326)
    -   Character Encoding: UTF-8

File Names
----------

1.  Base file names are formed according to following template:
     osm\_tablename\_g\_vNN (example: osm\_building\_a\_v01.gpkg)
     ... with following meaning:

-   -   osm\_: Prefix
    -   tablename: A table name from the data model.
    -   \_g: layer geometry type (g is a char out of “p”, “l” or “a”, meaning point, linestring, area/polygon)
    -   vNN: Version of the data model

1.  For some roads and other tables of geometry type (Multi-)Linestring, there will be tables with generalized geometry, called \_gen0, \_gen1 as follows (gen= generalized):

-   -   \_gen0: smoothed for highest zoom level
    -   \_gen1: simplified
    -   \_gen2: more simplified

1.  example: osm\_building\_a\_gen1\_v01.gpkg

Layer Specification Headers
---------------------------

|-------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Additional Attribute                      | This is the addition attribute that is introduce to the table to provide more information on top of the Common Layer Attributes.                                                       |
| Values of attributes 'type'               | Tells what the database values might contain based on the description of the tables under 3. Layer Overview. It also helps to defined the value meanings to remove unwanted vagueness. |
| Values of attributes 'aggtype' and 'type' | Same as the above but this table includes the aggregrate values which is to group the 'type' with more specific grouping                                                               |

Common Attributes
-----------------

These attributes are common to all tables (eventually except table from external sources).

|------------|--------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| Attribute  | Data Type                      | Description                                                                                                                                                                                                                                                                                                                                             | Osm Tags                                                 |
| osm\_id    | bigint                         | The id taken over from OSM elements node, way or relationship. The uniqueness is only within an OSM element. OSM does not guarantee uniqueness. But its often the only id one can get from the origin. osm2pgsql generates negative osm\_ids when areas are created from relations. And osm2pgsql creates sometimes duplicates by splitting large ways. | osm\_id=\*                                               |
| lastchange | timestamp without time zone    | The timestamp of the last time the feature was changed (UTC)                                                                                                                                                                                                                                                                                            | osm\_lastchange=\*                                       |
| geomtype   | varchar(1)                     | This will define weather it is a node (“N”), a way (“W”) or a relation (“R”). Self derivitive not from OSM database.                                                                                                                                                                                                                                    | (n/a)                                                    |
| geom       | geometry(\<<geometry>\>, 4326) | The “\<<geometry>\>” of the feature can be POINT, MULTILINESTRING or MULTIPOLYGON                                                                                                                                                                                                                                                                       | way=\*                                                   |
| type       | text (Enum)                    | This will define the feature type                                                                                                                                                                                                                                                                                                                       |                                                          |
| name       | text                           | The name which is in general use (which means cyrillic, arabic etc.)                                                                                                                                                                                                                                                                                    | name=\*                                                  |
| name\_intl | text                           | The name which is written in english, international                                                                                                                                                                                                                                                                                                     | Coalesce(name:en,int\_name,name:fr,name:es,name:de,name) |
| name\_fr   | text                           | The name which is written in french                                                                                                                                                                                                                                                                                                                     | name:fr=\*                                               |
| name\_es   | text                           | The name which is written in spanish                                                                                                                                                                                                                                                                                                                    | name:es=\*                                               |
| name\_de   | text                           | The name which is written in german                                                                                                                                                                                                                                                                                                                     | name:de=\*                                               |
| name\_int  | text                           | The international name of the feature                                                                                                                                                                                                                                                                                                                   | int\_name=\*                                             |
| label      | text                           | Translated name through transliterated                                                                                                                                                                                                                                                                                                                  |                                                          |
| tags       | text                           | Translate the hstore tags into string                                                                                                                                                                                                                                                                                                                   | tags=\*                                                  |

1.  

Layer Overview
==============

See file name conventions above about the meaning of “\_a” etc.

|--------------|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Tables       | Geometry Type   | Description                                                                                                                                                                                                                                     |
| address\_p   | POINT           | Stores address information regarding a place or building.                                                                                                                                                                                       |
| adminarea\_a | MULTIPOLYGON    | Administrative boundaries range from large groups of nation states right down to small administrative districts and suburbs, with an indication of this size/level of importance.                                                               |
| boundary\_l  | MULTILINESTRING | The boundary is used to mark the borders of areas, mostly political, but possibly also of other administrative areas.                                                                                                                           |
| building\_a  | MULTIPOLYGON    | To mark the outline of the area of buildings                                                                                                                                                                                                    |
| geoname\_l   | MULTILINESTRING | The boarder of a settlement which is marked around the node and to mark the specific type of settlement. Eg. City, town, village, etc.                                                                                                          |
| geoname\_p   | POINT           | It is to mark the centre of a named settlement and the specific type of settlement. Eg. City, town, village, etc.                                                                                                                               |
| landuse\_a   | MULTIPOLYGON    | Landuse describes the human use of land, for example fields and pastures.                                                                                                                                                                       |
| military\_a  | MULTIPOLYGON    | See military\_p                                                                                                                                                                                                                                 |
| military\_p  | POINT           | The military is for buildings and area used by the military.                                                                                                                                                                                    |
| misc\_l      | MULTILINESTRING | This contains elements could not be categorized into specific tables. E.g barrier and cliffs.                                                                                                                                                   |
| natural\_a   | MULTIPOLYGON    | see natural\_p                                                                                                                                                                                                                                  |
| natural\_p   | POINT           | Used to describes natural physical land features, including small modification by humans. E.g glacier, volcano, mud, etc.                                                                                                                       |
| nonop\_l     | MULTILINESTRING | non-op./planned infrastructure not usable for traffic or transport                                                                                                                                                                              |
| poi\_a       | MULTIPOLYGON    | Points of interest features of a generic place, like shops, amenities, leisure, accomondation, pitches etc.                                                                                                                                     |
| poi\_p       | POINT           | Points of interest features of a generic place, like shops, amenities, leisure, accomondation, etc.                                                                                                                                             |
| pow\_a       | MULTIPOLYGON    | See pow\_p                                                                                                                                                                                                                                      |
| pow\_p       | POINT           | This it a place of worship where people of different religion can go. e.g. church, temples(buddist, taoist, etc.), mosque(muslims)                                                                                                              |
| railway\_l   | MULTILINESTRING | All forms of transport using metal rails, including mainline services, subways, heritage lines and trams.                                                                                                                                       |
| road\_l      | MULTILINESTRING | Any road, route, way, or thoroughfare on land which connects one location to another and has been paved or otherwise improved to allow travel by some conveyance, including motorised vehicles, cyclists, pedestrians, horse riders, and others |
| route\_l     | MULTILINESTRING | A route is a customary or regular line of passage or travel, often predetermined and publicized. Routes consist of paths taken repeatedly by people and vehicles.                                                                               |
| traffic\_a   | MULTIPOLYGON    | See traffic\_p                                                                                                                                                                                                                                  |
| traffic\_p   | POINT           | It contains information regarding the rules of the road. Which allow better flow of traffic. E.g. Road signs, traffic calming, etc.                                                                                                             |
| transport\_a | MULTIPOLYGON    | See transport\_p                                                                                                                                                                                                                                |
| transport\_p | POINT           | Features which mark out points or location where it enable transporting anyone from one place to another. E.g. Bus stops, train station, etc.                                                                                                   |
| utility\_a   | MULTIPOLYGON    | See utility\_l                                                                                                                                                                                                                                  |
| utility\_p   | POINT           | See utility\_l                                                                                                                                                                                                                                  |
| utility\_l   | MULTILINESTRING | All features which are part of the utility body. E.g. Power structure (powerlines, power building), pipelines (oil, water, gas etc.), etc..                                                                                                     |
| water\_a     | MULTIPOLYGON    | See water\_l                                                                                                                                                                                                                                    |
| water\_p     | POINT           | See water\_l                                                                                                                                                                                                                                    |
| water\_l     | MULTILINESTRING | All features which are part of the waterbody. E.g. Dams, river, etc.                                                                                                                                                                            |

Layer Specification
===================

address\_p
----------

|----------------------|
| Additional Attribute |
| Attribute            |
| street               |
| housenumber          |
| postcode             |
| place                |

|-----------------------------|
| Values of attributes 'type' |
| value                       |
| b                           |
| e                           |
| i                           |
| p                           |

adminarea\_a
------------

|-----------------------------|
| Values of attributes 'type' |
| value                       |
| admin\_level1               |
| national                    |
| admin\_level3               |
| admin\_level4               |
| admin\_level5               |
| admin\_level6               |
| admin\_level7               |
| admin\_level8               |
| admin\_level9               |
| admin\_level10              |
| admin\_level11              |
| administrative              |
| national\_park              |
| protected\_area             |

adminunit\_a
------------

Tbd.

boundary\_l
-----------

|-----------------------------|
| Values of attributes 'type' |
| value                       |
| admin\_level1               |
| national                    |
| admin\_level3               |
| admin\_level4               |
| admin\_level5               |
| admin\_level6               |
| admin\_level7               |
| admin\_level8               |
| admin\_level9               |
| admin\_level10              |
| admin\_level11              |
| administrative              |
| national\_park              |
| protected\_area             |

building\_a
-----------

|----------------------|
| Additional Attribute |
| Attribute            |
| height               |

|-----------------------------|
| Values of attributes 'type' |
| value                       |
| building                    |

geoname\_l
----------

Refer to geoname\_p.

geoname\_p
----------

|----------------------|
| Additional Attribute |
| Attribute            |
| population           |
| wikipedia            |

|-----------------------------|
| Values of attributes 'type' |
| value                       |
| city                        |
| town                        |
| village                     |
| hamlet                      |
| suburb                      |
| island                      |
| farm                        |
| isolated\_dwelling          |
| locality                    |
| islet                       |
| neighbourhood               |
| county                      |
| region                      |
| state                       |
| municipality                |
| named\_place                |
| place                       |

landuse\_a
----------

|-----------------------------|
| Values of attributes 'type' |
| value                       |
| allotments                  |
| brownfield                  |
| commercial                  |
| farm                        |
| farmyard                    |
| fishfarm                    |
| grass                       |
| greenhouse                  |
| industrial                  |
| forest                      |
| meadow                      |
| military                    |
| nature\_reserve             |
| orchard                     |
| park                        |
| port                        |
| plant\_nursery              |
| quarry                      |
| railway                     |
| recreation\_ground          |
| residential                 |
| retail                      |
| vineyard                    |
| reservoir                   |
| basin                       |
| landfill                    |
| landuse                     |

military\_a
-----------

Refer to military\_a

military\_p
-----------

|-----------------------------|
| Values of attributes 'type' |
| value                       |
| airfield                    |
| barracks                    |
| bunker                      |
| checkpoint                  |
| danger\_area                |
| naval\_base                 |
| nuclear\_site               |
| obstacle\_course            |
| range                       |
| training\_area              |
| military                    |

misc\_l
-------

|-------------------------------------------|
| Values of attributes 'aggtype' and 'type' |
| value                                     |
| barrier                                   |
| barrier                                   |
| barrier                                   |
| barrier                                   |
| barrier                                   |
| barrier                                   |
| barrier                                   |
| barrier                                   |
| natural                                   |
| traffic\_calming                          |
| traffic\_calming                          |
| traffic\_calming                          |
| traffic\_calming                          |
| traffic\_calming                          |
| traffic\_calming                          |
| air\_traffic                              |
| air\_traffic                              |
| air\_traffic                              |

natural\_a
----------

|-----------------------------|
| Values of attributes 'type' |
| value                       |
| bare\_rock                  |
| beach                       |
| cave\_entrance              |
| fell                        |
| grassland                   |
| heath                       |
| moor                        |
| mud                         |
| sand                        |
| scree                       |
| scrub                       |
| sinkhole                    |
| stone                       |
| wood                        |
| glacier                     |
| wetland                     |
| natural                     |

natural\_p
----------

|-----------------------------|
| Values of attributes 'type' |
| value                       |
| beach                       |
| cave\_entrance              |
| fell                        |
| grassland                   |
| heath                       |
| moor                        |
| mud                         |
| peak                        |
| rock                        |
| saddle                      |
| sand                        |
| scrub                       |
| sinkhole                    |
| stone                       |
| tree                        |
| volcano                     |
| wood                        |
| glacier                     |
| wetland                     |
| natural                     |

nonop\_l
--------

|----------------------|
| Additional Attribute |
| Attribute            |
| ref                  |
| z\_order             |
| status               |

|-----------------------------|
| Values of attributes 'type' |
| value                       |
| highway                     |
| railway                     |

poi\_a
------

Refer to poi\_p.

poi\_p
------

|----------------------|
| Additional Attribute |
| Attribute            |
| aggtype              |
| website              |
| wikipedia            |
| phone                |
| contact\_phone       |
| opening\_hours       |
| cuisine              |
| access               |
| brand                |
| tower\_type          |

|-------------------------------------------|
| Values of attributes 'aggtype' and 'type' |
| aggtype value                             |
| public                                    |
| public                                    |
| public                                    |
| public                                    |
| public                                    |
| public                                    |
| public                                    |
| public                                    |
| public                                    |
| public                                    |
| public                                    |
| public                                    |
| public                                    |
| public                                    |
| public                                    |
| public                                    |
| public                                    |
| recycling                                 |
| recycling                                 |
| recycling                                 |
| recycling                                 |
| recycling                                 |
| education                                 |
| education                                 |
| education                                 |
| education                                 |
| education                                 |
| health                                    |
| health                                    |
| health                                    |
| health                                    |
| health                                    |
| health                                    |
| health                                    |
| leisure                                   |
| leisure                                   |
| leisure                                   |
| leisure                                   |
| leisure                                   |
| leisure                                   |
| leisure                                   |
| leisure                                   |
| leisure                                   |
| leisure                                   |
| leisure                                   |
| leisure                                   |
| leisure                                   |
| leisure                                   |
| leisure                                   |
| leisure                                   |
| leisure                                   |
| leisure                                   |
| catering                                  |
| catering                                  |
| catering                                  |
| catering                                  |
| catering                                  |
| catering                                  |
| catering                                  |
| accommodation\_in                         |
| accommodation\_in                         |
| accommodation\_in                         |
| accommodation\_in                         |
| accommodation\_in                         |
| accommodation\_out                        |
| accommodation\_out                        |
| accommodation\_out                        |
| accommodation\_out                        |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| shop                                      |
| vending                                   |
| vending                                   |
| vending                                   |
| money                                     |
| money                                     |
| money                                     |
| tourism                                   |
| tourism                                   |
| tourism                                   |
| tourism                                   |
| destination                               |
| destination                               |
| destination                               |
| destination                               |
| destination                               |
| destination                               |
| destination                               |
| destination                               |
| destination                               |
| destination                               |
| destination                               |
| destination                               |
| destination                               |
| destination                               |
| destination                               |
| destination                               |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| miscpoi                                   |
| tourism                                   |
| leisure                                   |
| sport                                     |
| man\_made                                 |
| shop                                      |
| historic                                  |
| amenity                                   |

pow\_a
------

Refer to pow\_p.

pow\_p
------

|----------------------|
| Additional Attribute |
| Attribute            |
| aggtype              |
| website              |
| wikipedia            |
| phone                |
| contact\_phone       |
| opening\_hours       |
| access               |

|-------------------------------------------|
| Values of attributes 'aggtype' and 'type' |
| aggtype value                             |
| buddhist                                  |
| christian                                 |
| christian                                 |
| christian                                 |
| christian                                 |
| christian                                 |
| christian                                 |
| christian                                 |
| christian                                 |
| christian                                 |
| christian                                 |
| christian                                 |
| hindu                                     |
| jewish                                    |
| muslim                                    |
| muslim                                    |
| muslim                                    |
| shinto                                    |
| sikh                                      |
| taoist                                    |
| place\_of\_worship                        |

railway\_l
----------

|----------------------|
| Additional Attribute |
| Attribute            |
| aggtype              |
| z\_order             |
| bridge               |
| tunnel               |
| voltage              |
| frequency            |

|-------------------------------------------|
| Values of attributes 'aggtype' and 'type' |
| value                                     |
| railway                                   |
| railway                                   |
| railway                                   |
| railway                                   |
| railway                                   |
| railway                                   |
| railway                                   |
| railway                                   |
| railway                                   |
| aerialway                                 |
| aerialway                                 |
| aerialway                                 |
| aerialway                                 |
| aerialway                                 |
| aerialway                                 |
| aerialway                                 |
| aerialway                                 |
| aerialway                                 |
| aerialway                                 |
| aerialway                                 |
| aerialway                                 |
| aerialway                                 |

road\_l
-------

|----------------------|
| Additional Attribute |
| Attribute            |
| aggtype              |
| ref                  |
| oneway               |
| maxspeed             |
| z\_order             |
| bridge               |
| tunnel               |

|-------------------------------------------|
| Values of attributes 'aggtype' and 'type' |
| aggtype value                             |
| major\_road                               |
| major\_road                               |
| major\_road                               |
| major\_road                               |
| major\_road                               |
| minor\_road                               |
| minor\_road                               |
| minor\_road                               |
| minor\_road                               |
| highway\_links                            |
| highway\_links                            |
| highway\_links                            |
| highway\_links                            |
| small\_road                               |
| track                                     |
| track                                     |
| track                                     |
| track                                     |
| track                                     |
| track                                     |
| no\_large\_vehicle                        |
| no\_large\_vehicle                        |
| no\_large\_vehicle                        |
| no\_large\_vehicle                        |
| no\_large\_vehicle                        |
| unclassified                              |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |
| roundabout                                |

route\_l
--------

|-----------------------------|
| Values of attributes 'type' |
| value                       |
| bicycle                     |
| bus                         |
| inline\_skates              |
| campe                       |
| detour                      |
| ferry                       |
| hiking                      |
| horse                       |
| light\_rail                 |
| mtb                         |
| nordic\_walking             |
| pipeline                    |
| piste                       |
| power                       |
| railway                     |
| road                        |
| running                     |
| ski                         |
| train                       |
| tram                        |
| route                       |

traffic\_a
----------

|----------------------|
| Additional Attribute |
| Attribute            |
| aggtype              |
| access               |

|-------------------------------------------|
| Values of attributes 'aggtype' and 'type' |
| aggtype value                             |
| fuel                                      |
| parking                                   |
| parking                                   |
| parking                                   |
| parking                                   |
| parking                                   |

traffic\_p
----------

|----------------------|
| Additional Attribute |
| Attribute            |
| aggtype              |
| access               |

|-------------------------------------------|
| Values of attributes 'aggtype' and 'type' |
| aggtype value                             |
| general\_traffic                          |
| general\_traffic                          |
| general\_traffic                          |
| general\_traffic                          |
| general\_traffic                          |
| general\_traffic                          |
| general\_traffic                          |
| general\_traffic                          |
| general\_traffic                          |
| general\_traffic                          |
| general\_traffic                          |
| barrier                                   |
| barrier                                   |
| barrier                                   |
| barrier                                   |
| barrier                                   |
| barrier                                   |
| barrier                                   |
| barrier                                   |
| barrier                                   |
| barrier                                   |
| barrier                                   |
| barrier                                   |
| traffic\_calming                          |
| traffic\_calming                          |
| traffic\_calming                          |
| traffic\_calming                          |
| traffic\_calming                          |
| traffic\_calming                          |
| fuel                                      |
| service                                   |
| parking                                   |
| parking                                   |
| parking                                   |
| parking                                   |
| parking                                   |

transport\_a
------------

|-------------------------------------------|
| Values of attributes 'aggtype' and 'type' |
| aggtype value                             |
| railway                                   |
| railway                                   |
| bus                                       |
| bus                                       |
| taxi                                      |
| air\_traffic                              |
| air\_traffic                              |
| air\_traffic                              |
| air\_traffic                              |
| air\_traffic                              |
| water\_traffic                            |
| other\_traffic                            |
| aeroway                                   |
| aerialway                                 |
| public\_transport                         |
| public\_transport                         |

transport\_p
------------

|-------------------------------------------|
| Values of attributes 'aggtype' and 'type' |
| aggtype value                             |
| railway                                   |
| railway                                   |
| tram                                      |
| bus                                       |
| bus                                       |
| taxi                                      |
| air\_traffic                              |
| air\_traffic                              |
| air\_traffic                              |
| air\_traffic                              |
| air\_traffic                              |
| water\_traffic                            |
| other\_traffic                            |
| aeroway                                   |
| aerialway                                 |
| public\_transport                         |
| public\_transport                         |

utility\_a
----------

|----------------------|
| Additional Attribute |
| Attribute            |
| aggtype              |

|-------------------------------------------|
| Values of attributes 'aggtype' and 'type' |
| value                                     |
| tower                                     |
| station                                   |
| station                                   |
| station                                   |
| station                                   |
| station                                   |
| station                                   |
| substation                                |
| transformer                               |
| man\_made                                 |
| man\_made                                 |
| man\_made                                 |
| power                                     |

utility\_p
----------

|----------------------|
| Additional Attribute |
| Attribute            |
| aggtype              |

|-------------------------------------------|
| Values of attributes 'aggtype' and 'type' |
| value                                     |
| tower                                     |
| pole                                      |
| station                                   |
| station                                   |
| station                                   |
| station                                   |
| station                                   |
| station                                   |
| substation                                |
| transformer                               |
| man\_made                                 |
| man\_made                                 |
| man\_made                                 |
| power                                     |

utility\_l
----------

|----------------------|
| Additional Attribute |
| Attribute            |
| operator             |
| voltage              |
| frequency            |

|-------------------------------------------|
| Values of attributes 'aggtype' and 'type' |
| aggtype value                             |
| power                                     |
| power                                     |
| power                                     |
| power                                     |
| man\_made                                 |
| power                                     |

water\_a
--------

|-----------------------------|
| Values of attributes 'type' |
| value                       |
| water                       |
| spring                      |
| riverbank                   |
| slipway                     |
| marina                      |
| pier                        |
| reservoir\_covered          |
| dam                         |
| weir                        |
| waterway                    |

water\_p
--------

|-----------------------------|
| Values of attributes 'type' |
| value                       |
| water                       |
| spring                      |
| riverbank                   |
| slipway                     |
| marina                      |
| pier                        |
| reservoir\_covered          |
| dam                         |
| waterfall                   |
| lock\_gate                  |
| weir                        |
| waterway                    |

water\_l
--------

|----------------------|
| Additional Attribute |
| Attribute            |
| width                |
| bridge               |
| tunnel               |

|-----------------------------|
| Values of attributes 'type' |
| value                       |
| river                       |
| stream                      |
| canal                       |
| drain                       |
| waterway                    |

Appendix
========

Glossary
--------

-   -   Table: tbd.
    -   Layer: tbd.
    -   Type: human-understandable name of a modeled entity (e.g. church, forest).
    -   Feature: Instance (record) of a feature class).
    -   Feature Class: same as table with one geometry attribute.
    -   Symbology: tbd.
    -   View: tbd.
    -   Data Curation: Filtering, cleaning, aggregating/categorizing and homogenizing data.

