import os
from osmaxx.conversion.conversion_settings import DBConfig
import subprocess

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


def extract_to(*, to_format, output_dir, base_filename, out_srs, db_config: DBConfig):
    db_user = db_config.user
    db_pass = db_config.password
    db_name = db_config.db_name
    db_host = db_config.host
    db_view_name = db_config.db_schema_tmp_view

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
        f"PG:dbname={db_name} host={db_host} user={db_user} password={db_pass} schemas={db_view_name} connect_timeout=-1",
    ]
    ogr2ogr_command += extraction_options
    print(30 * "#")
    print(ogr2ogr_command)
    print(subprocess.run(ogr2ogr_command, check=True, capture_output=True))
    return output_path
