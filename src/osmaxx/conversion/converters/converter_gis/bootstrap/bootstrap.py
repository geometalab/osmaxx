import random
import string
import glob
import os
import jinja2

from memoize import mproperty

from osmaxx.conversion.converters.converter_gis.detail_levels import (
    DETAIL_LEVEL_ALL,
    DETAIL_LEVEL_TABLES,
)
from osmaxx.conversion.converters.converter_gis.helper.default_postgres import (
    get_default_postgres_wrapper,
)
from osmaxx.conversion.converters.converter_gis.helper.osm_boundaries_importer import (
    OSMBoundariesImporter,
)
from osmaxx.conversion.converters.utils import logged_check_call
from osmaxx.utils import polyfile_helpers
from osmaxx.conversion.conversion_settings import DBConfig, WORKER_CACHE_MEGABYTES


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class BootStrapper:
    def __init__(
        self, area_polyfile_string, *, cutted_pbf_file, detail_level=DETAIL_LEVEL_ALL
    ):

        self.area_polyfile_string = area_polyfile_string
        self._pbf_file_path = cutted_pbf_file
        self._detail_level = DETAIL_LEVEL_TABLES[detail_level]
        tmp_name = get_random_string(20)
        self.db_config = DBConfig(db_name=f"osmaxx_{tmp_name}")
        self._postgres = get_default_postgres_wrapper(
            db_name=self.db_config.db_name,
        )

        self._script_base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "templates")
        )
        self._terminal_style_path = os.path.join(
            self._script_base_dir, "styles", "terminal.style"
        )
        self._style_path = os.path.join(self._script_base_dir, "styles", "style.lua")

    def __enter__(self):
        self._postgres.create_db()
        return self

    def __exit__(self, *args, **kwargs):
        self._postgres.drop_db()

    def bootstrap(self):
        print("Bootstrap", "#" * 30)
        # print("resetting database/views")
        # self._reset_database()
        print("setup database")
        self._setup_db()
        print("import boundaries")
        self._import_boundaries()
        print("import pbf")
        self._import_pbf()
        print("setup db functions")
        self._setup_db_functions()
        print("harmonize db")
        self._harmonize_database()
        print("filter data")
        self._filter_data()
        print("create views")
        self._create_views()

    @mproperty
    def geom(self):
        return polyfile_helpers.parse_poly_string(self.area_polyfile_string)

    def _reset_database(self):
        self._postgres.drop_db()
        self._postgres.create_db()
        self._setup_db()

    def _setup_db(self):
        drop_and_recreate_script_folder = os.path.join(
            self._script_base_dir, "sql", "drop_and_recreate"
        )
        self._execute_sql_scripts_in_folder(drop_and_recreate_script_folder)
        extensions = [
            "postgis",
            "hstore",
            "unaccent",
            "fuzzystrmatch",
            "osml10n",
            "osml10n_thai_transcript",
        ]
        for extension in extensions:
            print(30 * "#")
            print(extension)
            self._postgres.create_extension(extension)
            self._postgres.create_extension(
                extension, schema=self.db_config.db_schema_tmp
            )
            self._postgres.create_extension(
                extension, schema=self.db_config.db_schema_tmp_view
            )

    def _import_boundaries(self):
        osm_importer = OSMBoundariesImporter(db_config=self.db_config)
        osm_importer.load_area_specific_data(extent=self.geom)

    def _setup_db_functions(self):
        self._execute_sql_scripts_in_folder(
            os.path.join(self._script_base_dir, "sql", "functions")
        )

    def _harmonize_database(self):
        cleanup_sql_path = os.path.join(
            self._script_base_dir, "sql", "sweeping_data.sql.jinja2"
        )
        sql = self._compile_template(
            cleanup_sql_path, temp_table=f"tmp_{self.db_config.db_name}_harmonize"
        )
        print(self._postgres.execute_sql_command(sql))

    def _filter_data(self):
        self._postgres = get_default_postgres_wrapper(
            db_name=self.db_config.db_name,
        )
        filter_sql_script_folders = [
            "address",
            "adminarea_boundary",
            "building",
            "landuse",
            "military",
            "natural",
            "nonop",
            "geoname",
            "pow",
            "poi",
            "misc",
            "transport",
            "railway",
            "road",
            "route",
            "traffic",
            "utility",
            "water",
        ]
        base_dir = os.path.join(self._script_base_dir, "sql", "filter")
        for script_folder in filter_sql_script_folders:
            script_folder_path = os.path.join(base_dir, script_folder)
            self._execute_sql_scripts_in_folder(script_folder_path)

    def _create_views(self):
        create_view_sql_script_folder = os.path.join(
            self._script_base_dir, "sql", "create_view"
        )

        def filter_script_names(sql_file_path):
            file_name = os.path.basename(sql_file_path)
            if any(
                table_name in file_name
                for table_name in self._detail_level["included_layers"]
            ):
                return True
            return False

        self._execute_sql_scripts_in_folder(
            create_view_sql_script_folder, filter_function=filter_script_names
        )

    def _level_adapted_script_path(self, script_path):
        script_directory = os.path.dirname(script_path)
        script_name = os.path.basename(script_path)
        level_folder_name = self._detail_level["level_folder_name"]
        if level_folder_name:
            level_script_path = os.path.join(
                script_directory, level_folder_name, script_name
            )
            if os.path.exists(level_script_path):
                return level_script_path
        return script_path

    def _execute_sql_scripts_in_folder(
        self,
        folder_path,
        *,
        filter_function=lambda x: True,
    ):
        sql_scripts_in_folder = filter(
            filter_function, glob.glob(os.path.join(folder_path, "*.sql.jinja2"))
        )
        for script_path in sorted(sql_scripts_in_folder, key=os.path.basename):
            script_path = self._level_adapted_script_path(script_path)
            print(script_path)
            compiled_sql = self._compile_template(script_path)
            self._postgres.execute_sql_command(compiled_sql)

    def _compile_template(self, script_path, **kwargs):
        with open(script_path, "r") as _f:
            template = jinja2.Template(_f.read(), autoescape=False)
        return template.render(
            schema_name=self.db_config.db_schema_tmp,
            view_schema_name=self.db_config.db_schema_tmp_view,
            **kwargs,
        )

    def _import_pbf(self):
        db_name = self._postgres.get_db_name()
        db_host = self._postgres.get_host()
        db_port = self._postgres.get_port()
        db_user = self._postgres.get_user()

        osm_2_pgsql_command = [
            "osm2pgsql",
            "--database",
            f"{db_name}",
            "--username",
            f"{db_user}",
            "--host",
            f"{db_host}",
            "--port",
            f"{db_port}",
            "--cache",
            f"{WORKER_CACHE_MEGABYTES}",
            "--create",
            "--extra-attributes",
            "--slim",
            "--latlon",
            "--prefix=osm",
            "--log-level=debug",
            "--log-sql",
            f"--style={self._terminal_style_path}",
            f"--tag-transform-script={self._style_path}",
            "--number-processes=4",
            "--hstore-all",
            "--input-reader",
            "pbf",
            self._pbf_file_path,
        ]
        logged_check_call(command=osm_2_pgsql_command)
