import uuid
from collections import OrderedDict

from django.utils.translation import gettext as _

FGDB, SHAPEFILE, GPKG, SPATIALITE, GARMIN, PBF = 'fgdb', 'shapefile', 'gpkg', 'spatialite', 'garmin', 'pbf'


class OutputFormat:
    def __init__(
            self, *, long_identifier, verbose_name, archive_file_name_identifier, abbreviations, is_white_box,
            layer_filename_extension=None
    ):
        self._long_identifier = long_identifier
        self._verbose_name = verbose_name
        self._archive_file_name_identifier = archive_file_name_identifier
        self._abbreviations = abbreviations
        self._is_white_box = is_white_box
        self._layer_filename_extension = layer_filename_extension

    @property
    def long_identifier(self):
        return self._long_identifier

    @property
    def verbose_name(self):
        return self._verbose_name

    @property
    def archive_file_name_identifier(self):
        return self._archive_file_name_identifier

    @property
    def abbreviations(self):
        return self._abbreviations

    @property
    def layer_filename_extension(self):
        return self._layer_filename_extension

    @property
    def qgis_datasource_separator(self):
        """
        The string used to separate the dataset path (collections of layers) from the individual layer in a QGIS project
        file's ``<datasource>`` element referring to data in this format.
        """
        return '/' if self._layer_filename_extension is not None else '|layername='

    def unique_archive_name(self):
        return "{}_{}.zip".format(uuid.uuid4(), self.archive_file_name_identifier)

    def crs_change_available(self):
        return self._is_white_box

    def detail_level_available(self):
        return self._is_white_box


FORMAT_DEFINITIONS = OrderedDict([
    (FGDB, OutputFormat(
        long_identifier='Esri File Geodatabase',
        verbose_name=_('Esri File Geodatabase'),
        archive_file_name_identifier='FileGDB',
        abbreviations=['FileGDB', 'FGDB'],
        is_white_box=True,
    )),
    (SHAPEFILE, OutputFormat(
        long_identifier='Esri Shapefile',
        verbose_name=_('Esri Shapefile'),
        archive_file_name_identifier='Shapefile',
        abbreviations=[],
        is_white_box=True,
        layer_filename_extension='.shp',
    )),
    (GPKG, OutputFormat(
        long_identifier='GeoPackage',
        verbose_name=_('GeoPackage'),
        archive_file_name_identifier='GeoPackage',
        abbreviations=['GPKG'],
        is_white_box=True,
    )),
    (SPATIALITE, OutputFormat(
        long_identifier='SpatiaLite',
        verbose_name=_('SpatiaLite'),
        archive_file_name_identifier='SpatiaLite',
        abbreviations=[],
        is_white_box=True,
    )),
    (GARMIN, OutputFormat(
        long_identifier='Garmin navigation & map data',
        verbose_name=_('Garmin navigation & map data'),
        archive_file_name_identifier='Garmin',
        abbreviations=[],
        is_white_box=False,
    )),
    (PBF, OutputFormat(
        long_identifier='OSM Protocolbuffer Binary Format',
        verbose_name=_('OSM Protocolbuffer Binary Format'),
        archive_file_name_identifier='pbf',
        abbreviations=[],
        is_white_box=False,
    )),
])

FORMAT_CHOICES = tuple((key, definition.verbose_name) for key, definition in FORMAT_DEFINITIONS.items())
ALL = FORMAT_DEFINITIONS.keys()
