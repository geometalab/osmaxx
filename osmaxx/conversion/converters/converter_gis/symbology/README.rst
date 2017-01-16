About the OSMaxx QGIS sample symbolization
==========================================


File format
-----------

Because it is (to our knowledge) currently the only way to preserve
layer order, the symbolization for QGIS is offered as QGIS project files.

Because `scale-dependent rules cannot keep half-open scale ranges`_ in
current QGIS versions, we provide a separate project file for each of the
supported scale ranges:

around 1:2'500 (M1)
    ``OSMaxx_M1.qgs``

around 1:10'000 (M3)
    ``OSMaxx_M3.qgs``

around 1:25'000 (M4)
    ``OSMaxx_M4.qgs``

.. _`scale-dependent rules cannot keep half-open scale ranges`: http://hub.qgis.org/issues/15512


Help us improve
---------------

Contributions are welcome via https://github.com/geometalab/osmaxx-symbology


Latinized labels
----------------

The sample symbolization was created with the use-case of Osmaxx' original
contracting body in mind, where it'd have been used mainly for creating maps
for internal use at a western entity engaged in humanitarian activities
abroad. Most of the users of the maps would have been unfamiliar with the
local scripts of the mapped regions and more familiar with latin(-based)
script(s).

Thus, the sample symbolization uses the OSMaxx ``label`` attribute that contains
a western or latinized (transliterated) name. (See
https://github.com/geometalab/osmaxx/blob/master/docs/osmaxx_data_schema.md#attribute-label
for details.)

You can easily change the attribute used for labeling project-wide: Simply set
the QGIS variable ``osmaxx_label_expression`` to a different value, e.g. to
``name`` for the value of the literal OpenStreetMap name tag. See
https://github.com/geometalab/osmaxx/blob/master/docs/osmaxx_data_schema.md#common-attributes
for other suitable attributes. In QGIS 2.x, open the OSMaxx.qgs project, then
go to menu "Project" > "Project Properties...", tab "Variables" to see and
edit the QGIS project variables.

Alternatively, if you want to label some layers differently, you may also
*override the project variable* for those layers by defining a QGIS
*layer variable* of the same name (``osmaxx_label_expression``) in the respective
layers' properties dialogs:
Context menu of the layer > "Properties", tab "Variables", then use the "+"-Button.
