from osmaxx.conversion import output_format
from osmaxx.conversion.converters import converter_garmin
from osmaxx.conversion.converters import converter_gis
from osmaxx.conversion.converters import converter_pbf
from osmaxx.conversion.job_dispatcher.rq_dispatcher import rq_enqueue_with_settings
from osmaxx.utils.frozendict import frozendict

_format_converter = frozendict(
    {
        output_format.GARMIN: converter_garmin,
        output_format.PBF: converter_pbf,
        output_format.FGDB: converter_gis,
        output_format.SHAPEFILE: converter_gis,
        output_format.GPKG: converter_gis,
        output_format.SPATIALITE: converter_gis,
    }
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
    converter = _format_converter[conversion_format]
    converter.perform_export(**params)
    return None
