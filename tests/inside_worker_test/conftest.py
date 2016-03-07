import os

import pytest
import sqlalchemy
from sqlalchemy.engine.url import URL as DBURL
from sqlalchemy_utils import functions as sql_alchemy_utils

from tests.conftest import postgres_container_userland_port
from tests.inside_worker_test.declarative_schema import osm_models

worker_only_test = pytest.mark.skipif(
    not os.environ.get("TEST_INSIDE_WORKER", False),
    reason="This tests only runs in special enviroment"
)

slow = pytest.mark.skipif(
    not pytest.config.getoption("--runslow"),
    reason="need --runslow option to run"
)

db_name = 'osmaxx_db'

gis_db_connection_kwargs = dict(username='postgres', password='postgres', database=db_name, host='127.0.0.1', port=postgres_container_userland_port)


@pytest.fixture(scope='session')
def test_file_dir():
    return os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope='session')
def initialize_db(request):
    engine = sqlalchemy.create_engine(DBURL('postgres', **gis_db_connection_kwargs))

    # create database
    if not sql_alchemy_utils.database_exists(engine.url):
        sql_alchemy_utils.create_database(engine.url)

    def cleanup_db():
        sql_alchemy_utils.drop_database(engine.url)
    request.addfinalizer(cleanup_db)

    return engine


@pytest.fixture(scope='session')
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


@pytest.fixture(scope='session')
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


@pytest.fixture(scope='session')
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
def clean_osm_tables(osm_tables):
    engine = osm_tables
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
        engine.execute(table.delete())
    return engine


@pytest.fixture
def osmaxx_schemas(osmaxx_functions, clean_osm_tables, request):
    assert osmaxx_functions == clean_osm_tables  # same db-connection
    engine = osmaxx_functions
    for schema in _osmaxx_schemas:
        engine.execute(sqlalchemy.text("CREATE SCHEMA {};".format(schema)))

    def _cleanup():
        cleanup_osmaxx_schemas(engine)
    request.addfinalizer(_cleanup)
    return engine

_osmaxx_schemas = [
    'view_osmaxx',
    'osmaxx',
]


def cleanup_osmaxx_schemas(engine):
    for schema in _osmaxx_schemas:
        engine.execute(sqlalchemy.text("DROP SCHEMA IF EXISTS {} CASCADE;".format(schema)))


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
