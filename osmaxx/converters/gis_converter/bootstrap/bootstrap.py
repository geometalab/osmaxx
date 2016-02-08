import glob
import subprocess

import os

from osmaxx.converters.gis_converter.helper.default_postgres import get_default_postgres_wrapper
from osmaxx.utils import changed_dir


def boostrap(pbf_file_path):
    with changed_dir(os.path.dirname(__file__)):
        bootstrapper = BootStrapper(pbf_file_path=pbf_file_path)
        bootstrapper.bootstrap()


class BootStrapper:
    def __init__(self, pbf_file_path, limit_ram_usage=True):
        self._pbf_file_path = pbf_file_path
        self._postgres = get_default_postgres_wrapper()
        self._limit_ram_usage = limit_ram_usage
        self._script_base_dir = os.path.abspath(os.path.dirname(__file__))
        self._terminal_style_path = os.path.join(self._script_base_dir, 'styles', 'terminal.style')
        self._style_path = os.path.join(self._script_base_dir, 'styles', 'style.lua')

    def bootstrap(self):
        self._reset_database()
        self._convert_osm_pbf_to_postgres()
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

    def _convert_osm_pbf_to_postgres(self):
        db_name = self._postgres.get_db_name()
        postgres_user = self._postgres.get_user()

        osm_2_pgsql_command = [
            'osm2pgsql',
            '--create',
            '--extra-attributes',
            '--database', db_name,
            '--prefix', 'osm',
            '--style', self._terminal_style_path,
            '--tag-transform-script', self._style_path,
            '--number-processes', '8',
            '--username', postgres_user,
            '--hstore-all',
            '--input-reader', 'pbf',
            self._pbf_file_path,
        ]

        if self._limit_ram_usage:
            insert_pos = osm_2_pgsql_command.index('--extra-attributes')
            osm_2_pgsql_command.insert(insert_pos, '--slim')

        subprocess.check_call(osm_2_pgsql_command)

    def _setup_db_functions(self):
        self._execute_sql_scripts_in_folder(os.path.join(self._script_base_dir, 'sql', 'functions'))

    def _harmonize_database(self):
        cleanup_sql_path = os.path.join(self._script_base_dir, 'sql', 'sweeping_data.sql')
        self._postgres.execute_sql_file(cleanup_sql_path)

    def _filter_data(self):
        filter_sql_script_folders = [
            'drop_and_recreate',
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
