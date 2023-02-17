import logging
import os

from attr import dataclass
from django.contrib.gis.geos.geometry import GEOSGeometry
from osmaxx.conversion.converters.converter_gis.gis import (
    QGIS_DISPLAY_SRID,
    GISConverter,
)
from osmaxx.conversion.converters.converter_gis.bootstrap.bootstrap import BootStrapper
import tempfile
from pathlib import Path

from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.db import connection
from osmaxx.clipping_area.to_polyfile import create_poly_file_string
from osmaxx.conversion.conversion_settings import CONVERSION_SETTINGS
from osmaxx.conversion.constants import output_format
from osmaxx.conversion.converters.converter_garmin.garmin import Garmin
from osmaxx.conversion.converters.converter_pbf.to_pbf import produce_pbf
from osmaxx.conversion.converters.utils import logged_check_call
from osmaxx.excerptexport.excerpt_settings import RESULT_FILE_AVAILABILITY_DURATION
from osmaxx.excerptexport.models import Export, OutputFile
from osmaxx.excerptexport.models.output_file import uuid_directory_path
from osmaxx.utils.frozendict import frozendict

logger = logging.getLogger(__name__)


class ConversionHelper:
    def __init__(self, geometry: GEOSGeometry) -> None:
        self._pbf_source_path = CONVERSION_SETTINGS["PBF_PLANET_FILE_PATH"]
        self._polyfile_string = create_poly_file_string(geometry)

    def __enter__(self):
        self._pbf = tempfile.NamedTemporaryFile(suffix=".pbf")
        return self

    def __exit__(self, *args, **kwargs):
        self._pbf.close()

    @property
    def _converter(self):
        return frozendict(
            {
                output_format.GARMIN: self.create_garmin,
                output_format.PBF: self.create_pbf,
                output_format.FGDB: self.create_gis_export,
                output_format.SHAPEFILE: self.create_gis_export,
                output_format.GPKG: self.create_gis_export,
                output_format.SPATIALITE: self.create_gis_export,
            }
        )

    def cut_pbf(self):
        with tempfile.NamedTemporaryFile(suffix=".poly", mode="w+") as polyfile:
            polyfile.write(self._polyfile_string)
            polyfile.flush()
            os.fsync(polyfile)
            self._cut_pbf_along_polyfile(polyfile.name)

    def create_export(self, export_id):
        # this looks funny, but because processing takes so long,
        # we need to refetch the objects otherwise the database
        # connection is already closed
        export = Export.objects.get(pk=export_id)
        of = OutputFile.objects.create(
            export=export,
            mime_type="application/zip",
        )
        (
            self._zip_result_path,
            self._relative_zip_result_path,
        ) = self._create_zip_file_path(export=export, output_file=of)
        of_id = of.id

        now = timezone.now()
        unzipped_size = None
        try:
            # force connetion close, since this can take very long
            connection.close()
            unzipped_size = self._converter[export.file_format](export)
            of = OutputFile.objects.get(pk=of_id)
            of.file.name = self._relative_zip_result_path
            of.file_removal_at = now + RESULT_FILE_AVAILABILITY_DURATION
            of.save()
        finally:
            export = Export.objects.get(pk=export_id)
            export.unzipped_result_size = unzipped_size
            export.finished_at = now
            export.save()

    def create_pbf(self, export, *args, **kwargs):
        unzpped_size = produce_pbf(
            output_zip_file_path=self._zip_result_path,
            resulting_fname=f"{export.create_filename_base()}.pbf",
            cutted_pbf_file=self._pbf.name,
        )
        return unzpped_size

    def create_garmin(self, export: Export, *args, **kwargs):
        with tempfile.NamedTemporaryFile(suffix=".poly", mode="w+") as polyfile:
            polyfile.write(self._polyfile_string)
            polyfile.flush()
            os.fsync(polyfile)
            self._cut_pbf_along_polyfile(polyfile.name)
            garmin = Garmin(
                area_name=slugify(export.extraction_order.excerpt_name),
                polyfile_path=polyfile.name,
                cutted_pbf_file=self._pbf.name,
                output_zip_file_path=self._zip_result_path,
            )
            unzipped_size = garmin.create_garmin_export()
        return unzipped_size

    def create_gis_export(self, export: Export, *args, **kwargs):
        detail_level = export.extraction_order.detail_level

        with BootStrapper(
            area_polyfile_string=self._polyfile_string,
            cutted_pbf_file=self._pbf.name,
            detail_level=detail_level,
        ) as bootstrapper:
            bootstrapper.bootstrap()
            geom_srs_corrected = bootstrapper.geom.transform(
                QGIS_DISPLAY_SRID, clone=True
            )
            db_config = bootstrapper.db_config
            concrete_gis_converter = GISConverter(
                conversion_format=export.file_format,
                output_zip_file_path=self._zip_result_path,
                base_file_name=self._relative_zip_result_path,
                out_srs=export.extraction_order.epsg,
                detail_level=detail_level,
                db_config=db_config,
            )
            size = concrete_gis_converter.create_gis_export(geom_srs_corrected)
        return size

    def _create_zip_file_path(self, export, output_file):
        zip_file_name = f"{export.create_filename_base()}.zip"
        _relative_zip_result_path = uuid_directory_path(
            instance=output_file,
            filename=zip_file_name,
        )
        _zip_result_path = Path(settings.MEDIA_ROOT) / _relative_zip_result_path
        os.makedirs(os.path.dirname(_zip_result_path), exist_ok=True)
        return _zip_result_path, _relative_zip_result_path

    def _cut_pbf_along_polyfile(self, polyfile_path):
        # we need --overwrite since the file has been created by tempfile
        command = [
            "osmium",
            "extract",
            "-v",
            "--overwrite",
            "--output-format=pbf",
            "-s",
            "complete_ways",
            "--polygon",
            f"{polyfile_path}",
            f"{self._pbf_source_path}",
            "-o",
            f"{self._pbf.name}",
        ]
        logged_check_call(command)
        return self._pbf.name
