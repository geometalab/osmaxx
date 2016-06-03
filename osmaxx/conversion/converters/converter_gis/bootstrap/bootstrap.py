import glob
import os

from osmaxx.conversion.converters.converter_gis.helper.default_postgres import get_default_postgres_wrapper
from osmaxx.conversion.converters.converter_gis.helper.osm_importer import OSMImporter
from osmaxx.utils import polyfile_helpers


def boostrap(area_polyfile_string):
    bootstrapper = BootStrapper(area_polyfile_string)
    bootstrapper.bootstrap()


class BootStrapper:
    def __init__(self, area_polyfile_string):
        self._postgres = get_default_postgres_wrapper()
        self._script_base_dir = os.path.abspath(os.path.dirname(__file__))
        self._terminal_style_path = os.path.join(self._script_base_dir, 'styles', 'terminal.style')
        self._style_path = os.path.join(self._script_base_dir, 'styles', 'style.lua')
        self._extent = polyfile_helpers.parse_poly_string(area_polyfile_string)

    def bootstrap(self):
        self._reset_database()
        self._import_from_world_db()
        self._setup_db_functions()
        self._harmonize_database()
        self._filter_data()

    def _reset_database(self):
        self._postgres.drop_db()
        self._postgres.create_db()
        self._setup_db()

    def _setup_db(self):
        self._postgres.create_extension("hstore")
        self._postgres.create_extension("postgis")
        drop_and_recreate_script_folder = os.path.join(self._script_base_dir, 'sql', 'drop_and_recreate')
        self._execute_sql_scripts_in_folder(drop_and_recreate_script_folder)

    def _import_from_world_db(self):
        osm_importer = OSMImporter()
        osm_importer.load_area_specific_data(extent=self._extent)

    def _setup_db_functions(self):
        self._execute_sql_scripts_in_folder(os.path.join(self._script_base_dir, 'sql', 'functions'))

    def _harmonize_database(self):
        cleanup_sql_path = os.path.join(self._script_base_dir, 'sql', 'sweeping_data.sql')
        self._postgres.execute_sql_file(cleanup_sql_path)

    def _filter_data(self):
        filter_sql_script_folders = [
            'address',
            'adminarea_boundary',
            'building',
            'landuse',
            'military',
            'natural',
            'nonop',
            'geoname',
            'pow',
            'poi',
            'misc',
            'transport',
            'railway',
            'road',
            'route',
            'traffic',
            'utility',
            'water',
            'create_view',
        ]
        base_dir = os.path.join(self._script_base_dir, 'sql', 'filter')
        for script_folder in filter_sql_script_folders:
            script_folder_path = os.path.join(base_dir, script_folder)
            self._execute_sql_scripts_in_folder(script_folder_path)

    def _execute_sql_scripts_in_folder(self, folder_path):
        sql_scripts_in_folder = glob.glob(os.path.join(folder_path, '*.sql'))
        for script_path in sorted(sql_scripts_in_folder, key=os.path.basename):
            self._postgres.execute_sql_file(script_path)
