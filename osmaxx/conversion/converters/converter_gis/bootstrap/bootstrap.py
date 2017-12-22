import glob
import os

from memoize import mproperty

from osmaxx.conversion.converters.converter_gis.detail_levels import DETAIL_LEVEL_ALL, DETAIL_LEVEL_TABLES
from osmaxx.conversion.converters.converter_gis.helper.default_postgres import get_default_postgres_wrapper
from osmaxx.conversion.converters.converter_gis.helper.osm_boundaries_importer import OSMBoundariesImporter
from osmaxx.conversion.converters.converter_pbf.to_pbf import cut_pbf_along_polyfile
from osmaxx.conversion.converters.utils import logged_check_call
from osmaxx.utils import polyfile_helpers


class BootStrapper:
    def __init__(self, area_polyfile_string, *, detail_level=DETAIL_LEVEL_ALL):
        self.area_polyfile_string = area_polyfile_string
        self._postgres = get_default_postgres_wrapper()
        self._script_base_dir = os.path.abspath(os.path.dirname(__file__))
        self._terminal_style_path = os.path.join(self._script_base_dir, 'styles', 'terminal.style')
        self._style_path = os.path.join(self._script_base_dir, 'styles', 'style.lua')
        self._pbf_file_path = os.path.join('/tmp', 'pbf_cutted.pbf')
        self._detail_level = DETAIL_LEVEL_TABLES[detail_level]

    def bootstrap(self):
        self._reset_database()
        cut_pbf_along_polyfile(self.area_polyfile_string, self._pbf_file_path)
        self._import_boundaries()
        self._import_pbf()
        self._setup_db_functions()
        self._harmonize_database()
        self._filter_data()
        self._create_views()

    @mproperty
    def geom(self):
        return polyfile_helpers.parse_poly_string(self.area_polyfile_string)

    def _reset_database(self):
        self._postgres.drop_db()
        self._postgres.create_db()
        self._setup_db()

    def _setup_db(self):
        extensions = ['hstore', 'postgis', 'unaccent', 'fuzzystrmatch', 'osml10n']
        for extension in extensions:
            self._postgres.create_extension(extension)
        drop_and_recreate_script_folder = os.path.join(self._script_base_dir, 'sql', 'drop_and_recreate')
        self._execute_sql_scripts_in_folder(drop_and_recreate_script_folder)

    def _import_boundaries(self):
        osm_importer = OSMBoundariesImporter()
        osm_importer.load_area_specific_data(extent=self.geom)

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
        ]
        base_dir = os.path.join(self._script_base_dir, 'sql', 'filter')
        for script_folder in filter_sql_script_folders:
            script_folder_path = os.path.join(base_dir, script_folder)
            self._execute_sql_scripts_in_folder(script_folder_path)

    def _create_views(self):
        create_view_sql_script_folder = os.path.join(self._script_base_dir, 'sql', 'create_view')

        def filter_script_names(sql_file_path):
            file_name = os.path.basename(sql_file_path)
            if any(table_name in file_name for table_name in self._detail_level['included_layers']):
                return True
            return False

        self._execute_sql_scripts_in_folder(create_view_sql_script_folder, filter_function=filter_script_names)

    def _level_adapted_script_path(self, script_path):
        script_directory = os.path.dirname(script_path)
        script_name = os.path.basename(script_path)
        level_folder_name = self._detail_level['level_folder_name']
        if level_folder_name:
            level_script_path = os.path.join(script_directory, level_folder_name, script_name)
            if os.path.exists(level_script_path):
                return level_script_path
        return script_path

    def _execute_sql_scripts_in_folder(self, folder_path, *, filter_function=lambda x: True):
        sql_scripts_in_folder = filter(filter_function, glob.glob(os.path.join(folder_path, '*.sql')))
        for script_path in sorted(sql_scripts_in_folder, key=os.path.basename):
            script_path = self._level_adapted_script_path(script_path)
            self._postgres.execute_sql_file(script_path)

    def _import_pbf(self):
        db_name = self._postgres.get_db_name()
        postgres_user = self._postgres.get_user()

        osm_2_pgsql_command = [
            'osm2pgsql',
            '--create',
            '--extra-attributes',
            '--slim',
            '--latlon',
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
        logged_check_call(osm_2_pgsql_command)
