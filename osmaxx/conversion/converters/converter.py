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


def start_format_extraction(
        *,
        conversion_format,
        area_name,
        osmosis_polygon_file_string,
        output_zip_file_path,
        filename_prefix,
        detail_level,
        out_srs
):
    converter = _format_converter[conversion_format]
    converter.perform_export(
        conversion_format=conversion_format,
        output_zip_file_path=output_zip_file_path,
        area_name=area_name,
        filename_prefix=filename_prefix,
        out_srs=out_srs,
        polyfile_string=osmosis_polygon_file_string,
        detail_level=detail_level,
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
    start_format_extraction(**params)
    return None
