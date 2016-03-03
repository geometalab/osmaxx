import os

import pytest
import sqlalchemy
from sqlalchemy.engine.url import URL as DBURL
from sqlalchemy_utils import functions as sql_alchemy_utils

from tests.inside_worker_test.declarative_schema import osm_models

worker_only_test = pytest.mark.skipif(
    not os.environ.get("TEST_INSIDE_WORKER", False),
    reason="This tests only runs in special enviroment"
)

db_name = 'osmaxx_db'

gis_db_connection_kwargs = dict(username='postgres', password='postgres', database=db_name)


@pytest.fixture
def test_file_dir():
    return os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def initialize_db(request):
    engine = sqlalchemy.create_engine(DBURL('postgres', **gis_db_connection_kwargs))

    # create database
    if not sql_alchemy_utils.database_exists(engine.url):
        sql_alchemy_utils.create_database(engine.url)

    def cleanup_db():
        sql_alchemy_utils.drop_database(engine.url)
    request.addfinalizer(cleanup_db)

    return engine


@pytest.fixture
def extensions(initialize_db, request):
    engine = initialize_db
    extensions = ['postgis', 'hstore']
    for extension in extensions:
        engine.execute(sqlalchemy.text("CREATE EXTENSION IF NOT EXISTS {};".format(extension)))

    def cleanup_extensions():
        for extension in extensions:
            engine.execute(sqlalchemy.text("DROP EXTENSION IF EXISTS {} CASCADE;".format(extension)))

    request.addfinalizer(cleanup_extensions)

    return engine


@pytest.fixture
def osm_tables(extensions, request):
    engine = extensions
    tables = [
        osm_models.t_osm_line,
        osm_models.t_osm_point,
        osm_models.t_osm_polygon,
        osm_models.t_osm_roads,
        osm_models.OsmNode.__table__,
        osm_models.OsmRel.__table__,
        osm_models.OsmWay.__table__,
    ]
    for table in tables:
        table.create(engine)

    def cleanup_tables():
        for table in tables:
            table.drop(engine)
    request.addfinalizer(cleanup_tables)
    return engine


@pytest.fixture
def osmaxx_functions(osm_tables):
    function_scripts = [
        'sql/functions/0010_cast_to_positive_integer.sql',
        'sql/functions/0020_building_height.sql',
        'sql/functions/0030_transliterate.sql',
        'sql/functions/0040_interpolate_addresses.sql',
        'sql/functions/0050_cast_to_int.sql',
    ]
    engine = osm_tables
    for function_script in function_scripts:
        engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(function_script)).execution_options(autocommit=True))
    return engine


@pytest.fixture
def osm_cleaned(osmaxx_functions):
    engine = osmaxx_functions
    address_script_setup = 'sql/sweeping_data.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)))
    return engine


@pytest.fixture
def osmaxx_schemas(osm_cleaned, request):
    engine = osm_cleaned
    osmaxx_schemas = [
        'view_osmaxx',
        'osmaxx',
    ]
    for schema in osmaxx_schemas:
        engine.execute(sqlalchemy.text("CREATE SCHEMA {};".format(schema)))

    def cleanup_osmaxx_schemas():
        for schema in osmaxx_schemas:
            engine.execute(sqlalchemy.text("DROP SCHEMA {} CASCADE;".format(schema)))
    request.addfinalizer(cleanup_osmaxx_schemas)
    return engine


def sql_from_bootstrap_relative_location(file_name):
    """
    SQL Statement from a script relative to the bootstrap folder.

    Args:
        file_name: relative path to a sql script

    Returns: a sql statement as string
    """
    from osmaxx.converters.gis_converter import bootstrap
    script_path = os.path.join(os.path.abspath(os.path.dirname(bootstrap.__file__)), file_name)
    content = open(script_path, 'r').read()
    return content
