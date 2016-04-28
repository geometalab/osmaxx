from osmaxx.conversion.converters.converter_garmin.garmin import Garmin
from osmaxx.conversion.converters.converter_gis.gis import GISConverter
from osmaxx.conversion.job_dispatcher.rq_dispatcher import rq_enqueue_with_settings
from osmaxx.conversion_api.formats import FGDB, SHAPEFILE, GPKG, SPATIALITE, GARMIN


class Conversion(object):
    def __init__(
            self,
            *,
            conversion_format,
            area_name,
            osmosis_polygon_file_string,
            output_zip_file_path,
            filename_prefix,
            out_srs=None
    ):
        self._conversion_format = conversion_format
        self._output_zip_file_path = output_zip_file_path
        self._area_name = area_name
        self._polyfile_string = osmosis_polygon_file_string
        self._name_prefix = filename_prefix
        self._out_srs = out_srs

        _format_process = {
            GARMIN: self._create_garmin_export,
            FGDB: self._extract_postgis_format,
            SHAPEFILE: self._extract_postgis_format,
            GPKG: self._extract_postgis_format,
            SPATIALITE: self._extract_postgis_format,
        }
        self._conversion_process = _format_process[conversion_format]

    def start_format_extraction(self):
        self._conversion_process()

    def _extract_postgis_format(self):
        gis = GISConverter(
            conversion_format=self._conversion_format,
            out_zip_file_path=self._output_zip_file_path,
            base_file_name=self._name_prefix,
            out_srs=self._out_srs,
            polyfile_string=self._polyfile_string,
        )
        gis.create_gis_export()

    def _create_garmin_export(self):
        garmin = Garmin(
            out_zip_file_path=self._output_zip_file_path,
            area_name=self._area_name,
            polyfile_string=self._polyfile_string,
        )
        garmin.create_garmin_export()


def convert(
        *, conversion_format, area_name, osmosis_polygon_file_string, output_zip_file_path, filename_prefix,
        out_srs, use_worker=False
):
    params = dict(
        conversion_format=conversion_format,
        area_name=area_name,
        osmosis_polygon_file_string=osmosis_polygon_file_string,
        output_zip_file_path=output_zip_file_path,
        filename_prefix=filename_prefix,
        out_srs=out_srs,
    )
    # TODO: find a cleaner way for this recursion magic!
    if use_worker:
        return rq_enqueue_with_settings(
            convert,
            use_worker=False,
            **params
        ).id
    conversion = Conversion(**params)
    conversion.start_format_extraction()
    return None
