import uuid
from collections import OrderedDict

from django.utils.translation import gettext as _

FGDB, SHAPEFILE, GPKG, SPATIALITE, GARMIN = 'fgdb', 'shapefile', 'gpkg', 'spatialite', 'garmin'


class OutputFormat:
    def __init__(self, *, long_identifier, verbose_name, archive_file_name_identifier, abbreviations, is_white_box):
        self._long_identifier = long_identifier
        self._verbose_name = verbose_name
        self._archive_file_name_identifier = archive_file_name_identifier
        self._abbreviations = abbreviations
        self._is_white_box = is_white_box

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

    def unique_archive_name(self):
        return "{}_{}.zip".format(uuid.uuid4(), self.archive_file_name_identifier)

    def crs_change_available(self):
        return self._is_white_box

    def detail_level_available(self):
        return self._is_white_box


FORMAT_DEFINITIONS = OrderedDict([
    (FGDB, OutputFormat(
        long_identifier='ESRI File Geodatabase',
        verbose_name=_('ESRI File Geodatabase'),
        archive_file_name_identifier='FileGDB',
        abbreviations=['FileGDB', 'FGDB'],
        is_white_box=True,
    )),
    (SHAPEFILE, OutputFormat(
        long_identifier='ESRI Shapefile',
        verbose_name=_('ESRI Shapefile'),
        archive_file_name_identifier='Shapefile',
        abbreviations=[],
        is_white_box=True,
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
])

FORMAT_CHOICES = tuple((key, definition.verbose_name) for key, definition in FORMAT_DEFINITIONS.items())
