from osmaxx.conversion.converters import converter_garmin
from osmaxx.conversion.converters import converter_gis
from osmaxx.conversion.converters import converter_pbf
from osmaxx.conversion.job_dispatcher.rq_dispatcher import rq_enqueue_with_settings
from osmaxx.conversion_api.formats import FGDB, SHAPEFILE, GPKG, SPATIALITE, GARMIN, PBF
from osmaxx.utils.frozendict import frozendict

_format_converter = frozendict(
    {
        GARMIN: converter_garmin,
        PBF: converter_pbf,
        FGDB: converter_gis,
        SHAPEFILE: converter_gis,
        GPKG: converter_gis,
        SPATIALITE: converter_gis,
    }
)


class Conversion(object):
    def __init__(
            self,
            *,
            conversion_format,
            area_name,
            osmosis_polygon_file_string,
            output_zip_file_path,
            filename_prefix,
            detail_level,
            out_srs=None
    ):
        self._conversion_format = conversion_format
        self._output_zip_file_path = output_zip_file_path
        self._area_name = area_name
        self._polyfile_string = osmosis_polygon_file_string
        self._name_prefix = filename_prefix
        self._out_srs = out_srs
        self._detail_level = detail_level
        self._converter = _format_converter[conversion_format]

    def start_format_extraction(self):
        self._converter.perform_export(
            conversion_format=self._conversion_format,
            output_zip_file_path=self._output_zip_file_path,
            area_name=self._area_name,
            filename_prefix=self._name_prefix,
            out_srs=self._out_srs,
            polyfile_string=self._polyfile_string,
            detail_level=self._detail_level,
        )


def convert(
        *, conversion_format, area_name, osmosis_polygon_file_string, output_zip_file_path, filename_prefix,
        out_srs, detail_level, use_worker=False, queue_name='default'
):
    params = dict(
        conversion_format=conversion_format,
        area_name=area_name,
        osmosis_polygon_file_string=osmosis_polygon_file_string,
        output_zip_file_path=output_zip_file_path,
        filename_prefix=filename_prefix,
        detail_level=detail_level,
        out_srs=out_srs,
    )

    # TODO: find a cleaner way for this recursion magic!
    if use_worker:
        return rq_enqueue_with_settings(
            convert,
            use_worker=False,
            queue_name=queue_name,
            **params
        ).id
    conversion = Conversion(**params)
    conversion.start_format_extraction()
    return None
