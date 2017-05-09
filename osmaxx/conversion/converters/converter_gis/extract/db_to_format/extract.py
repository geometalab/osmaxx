import os
import subprocess

from osmaxx.conversion._settings import CONVERSION_SETTINGS
from osmaxx.conversion.constants.output_format import FGDB, SHAPEFILE, GPKG, SPATIALITE

FORMATS = {
    FGDB: {
        'ogr_name': 'FileGDB',
        'extension': '.gdb',
        'extraction_options': [],
    },
    GPKG: {
        'ogr_name': 'GPKG',
        'extension': '.gpkg',
        'extraction_options': [],
    },
    SHAPEFILE: {
        'ogr_name': 'Esri Shapefile',
        'extension': '.shp',
        'extraction_options': ['-lco', 'ENCODING=UTF-8'],
    },
    SPATIALITE: {
        'ogr_name': 'SQLite',
        'extension': '.sqlite',
        'extraction_options': ['-dsco', 'SPATIALITE=YES', '-nlt', 'GEOMETRY']  # FIXME: Remove or change -nlt because of geometry reading problems
    },
}


def extract_to(*, to_format, output_dir, base_filename, out_srs):
    conversion_service_settings = CONVERSION_SETTINGS
    db_name = conversion_service_settings['GIS_CONVERSION_DB_NAME']
    db_user = conversion_service_settings['GIS_CONVERSION_DB_USER']
    db_pass = conversion_service_settings['GIS_CONVERSION_DB_PASSWORD']

    to_format_options = FORMATS[to_format]
    extraction_options = to_format_options['extraction_options']
    ogr_name = to_format_options['ogr_name']
    extension = to_format_options['extension']

    output_path = os.path.join(output_dir, base_filename + extension)

    ogr2ogr_command = [
        'ogr2ogr', '-f', str(ogr_name), output_path,
        '-t_srs', out_srs,
        'PG:dbname={dbname} user={user} password={password} schemas=view_osmaxx'.format(
            dbname=db_name,
            user=db_user,
            password=db_pass,
        ),
    ]
    ogr2ogr_command += extraction_options
    subprocess.check_output(ogr2ogr_command)
    return output_path
