import subprocess

import os

import pytest
import sqlalchemy
from sqlalchemy import orm

from osmaxx.converters.gis_converter.bootstrap import bootstrap
from osmaxx.converters.gis_converter.helper.postgres_wrapper import Postgres

worker_only_test = pytest.mark.skipif(
    not os.environ.get("TEST_INSIDE_WORKER", False),
    reason="This tests only runs in special enviroment"
)

db_name = 'osmaxx_db'

gis_db_connection_kwargs = dict(user='postgres', password='postgres', db_name=db_name)


class DB:
    def __init__(self):
        pg = Postgres(**gis_db_connection_kwargs)
        self.connection = pg._engine.connect()

    def begin(self):
        self.trans = self.connection.begin()
        self.session = orm.Session(bind=self.connection)

    def execute(self, sql):
        return self.session.execute(sqlalchemy.text(sql))

    def rollback(self):
        self.session.commit()
        self.session.close()
        self.trans.rollback()
        self.connection.close()


@pytest.fixture
def test_file_dir():
    return os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope="session", autouse=True)
def initialize_db(request):
    pg = Postgres(**gis_db_connection_kwargs)
    pg.create_db()

    def cleanup_db():
        pg.drop_db()
    request.addfinalizer(cleanup_db)
    return db_name


@pytest.fixture
def load_data_v1(initialize_db, test_file_dir):
    dev_null = open(os.devnull, 'w')
    db_name = initialize_db
    db_dump_location = os.path.join(test_file_dir, 'dumps', 'sql', 'zuerich.osm.dump.sql.bz2')
    subprocess.check_call("/bin/bunzip2 -c {0} | psql -U postgres {1}".format(db_dump_location, db_name), shell=True, stdout=dev_null)
    return db_name


@pytest.fixture
def load_data_v2(initialize_db, test_file_dir):
    db_name = initialize_db
    # prepare database from osm excerpt(s)
    pbfs = [
        'dumps/pbf/monaco/monaco-latest.osm.pbf',
    ]
    for pbf in pbfs:
        pbf_path = os.path.join(test_file_dir, pbf)
        bootstrapper = bootstrap.BootStrapper(pbf_file_path=pbf_path)
        bootstrapper._postgres = Postgres(**gis_db_connection_kwargs)
        bootstrapper._reset_database()
        bootstrapper._convert_osm_pbf_to_postgres()
        bootstrapper._setup_db_functions()
        bootstrapper._harmonize_database()
        bootstrapper._postgres.execute_sql_command(sql_from_bootstrap_relative_location('sql/filter/drop_and_recreate/drop_and_recreate.sql'))
    return db_name


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


@worker_only_test
def test_label_translated_correctly_v2(load_data_v2):
    db = DB()
    db.begin()
    address_script_setup = 'sql/filter/address/000_setup-drop_and_recreate_table.sql'
    db.execute(sql_from_bootstrap_relative_location(address_script_setup))

    address_script = 'sql/filter/address/010_address.sql'
    result = db.execute(sql_from_bootstrap_relative_location(address_script))
    assert len(result) > 0
    for row in result:
        assert row['label'] is not None
    db.rollback()


@worker_only_test
def test_label_translated_correctly_v1(load_data_v1, run_in_transaction):
    address_script_setup = 'sql/filter/address/000_setup-drop_and_recreate_table.sql'
    run_in_transaction(sql_from_bootstrap_relative_location(address_script_setup))

    address_script = 'sql/filter/address/010_address.sql'
    result = run_in_transaction(sql_from_bootstrap_relative_location(address_script))
    assert len(result) > 0
