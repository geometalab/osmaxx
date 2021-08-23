import os
import subprocess

from osmaxx.conversion._settings import CONVERSION_SETTINGS
from osmaxx.conversion import output_format

FORMATS = {
    output_format.FGDB: {
        "ogr_name": "FileGDB",
        "extension": ".gdb",
        "extraction_options": [],
    },
    output_format.GPKG: {
        "ogr_name": "GPKG",
        "extension": ".gpkg",
        "extraction_options": [],
    },
    output_format.SHAPEFILE: {
        "ogr_name": "Esri Shapefile",
        "extension": ".shp",
        "extraction_options": ["-lco", "ENCODING=UTF-8"],
    },
    output_format.SPATIALITE: {
        "ogr_name": "SQLite",
        "extension": ".sqlite",
        "extraction_options": [
            "-dsco",
            "SPATIALITE=YES",
            "-nlt",
            "GEOMETRY",
        ],  # FIXME: Remove or change -nlt because of geometry reading problems
    },
}


def extract_to(*, to_format, output_dir, base_filename, out_srs):
    conversion_service_settings = CONVERSION_SETTINGS
    db_user = conversion_service_settings["GIS_CONVERSION_DB_USER"]
    db_pass = conversion_service_settings["GIS_CONVERSION_DB_PASSWORD"]
    db_host = CONVERSION_SETTINGS["GIS_CONVERSION_DB_HOST"]
    dbname = conversion_service_settings["GIS_CONVERSION_DB_NAME"]
    db_view_name = CONVERSION_SETTINGS["CONVERSION_SCHEMA_NAME_TMP_VIEW"]

    to_format_options = FORMATS[to_format]
    extraction_options = to_format_options["extraction_options"]
    ogr_name = to_format_options["ogr_name"]
    extension = to_format_options["extension"]

    output_path = os.path.join(output_dir, base_filename + extension)

    ogr2ogr_command = [
        "ogr2ogr",
        "-f",
        str(ogr_name),
        output_path,
        "-t_srs",
        out_srs,
        f"PG:dbname={dbname} host={db_host} user={db_user} password={db_pass} schemas={db_view_name}",
    ]
    ogr2ogr_command += extraction_options
    subprocess.check_output(ogr2ogr_command)
    return output_path
