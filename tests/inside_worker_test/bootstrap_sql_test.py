import os

import pytest
import sqlalchemy
from sqlalchemy import orm

from osmaxx.converters.gis_converter.helper.postgres_wrapper import Postgres
from tests.inside_worker_test.conftest import sql_from_bootstrap_relative_location

worker_only_test = pytest.mark.skipif(
    not os.environ.get("TEST_INSIDE_WORKER", False),
    reason="This tests only runs in special enviroment"
)

db_name = 'osmaxx_db'

gis_db_connection_kwargs = dict(username='postgres', password='postgres', database=db_name)


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


@worker_only_test
def test_label_translated_correctly(osmaxx_schemas):
    no_row_operation = -1
    no_row_affected = 0
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/address/000_setup-drop_and_recreate_table.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))
    assert result.rowcount == no_row_operation

    address_script = 'sql/filter/address/010_address.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == no_row_affected
    # for row in result:
    #     assert row['label'] is not None
    # db.rollback()
