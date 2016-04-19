from contextlib import contextmanager, closing

import pytest
import sqlalchemy
from sqlalchemy.sql.schema import Table as DbTable

from tests.conftest import area_polyfile_string
from tests.inside_worker_test.conftest import slow
from tests.inside_worker_test.declarative_schema import osm_models


@slow
def test_osmaxx_data_model_processing_puts_amenity_grave_yard_with_religion_into_table_pow_a(data_import):
    data = {
        osm_models.t_osm_polygon: dict(
            amenity='grave_yard',
            religion='any value will do, as long as one is present',
        ),
    }
    with data_import(data) as engine:
        t_pow_a = DbTable('pow_a', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_pow_a]))) as result:
            assert result.rowcount == 1


@pytest.fixture()
def data_import(osmaxx_schemas, clean_osm_tables, monkeypatch):
    from tests.inside_worker_test.conftest import cleanup_osmaxx_schemas
    from osmaxx.conversion.converters.converter_gis.bootstrap.bootstrap import BootStrapper

    assert osmaxx_schemas == clean_osm_tables  # same db-connection
    engine = osmaxx_schemas
    monkeypatch.setattr(
        'osmaxx.conversion.converters.converter_gis.helper.postgres_wrapper.create_engine', lambda *_, **__: engine)

    class _BootStrapperWithoutPbfFile(BootStrapper):
        def __init__(self, data):
            super().__init__(area_polyfile_string=area_polyfile_string())
            self.data = data

        def _reset_database(self):
            pass  # Already taken care of by clean_osm_tables fixture.

        def _import_from_world_db(self):
            for table, values in self.data.items():
                engine.execute(table.insert().execution_options(autocommit=True), values)

        def _setup_db_functions(self):
            pass  # Already taken care of by osmaxx_functions fixture.

    @contextmanager
    def import_data(data):
        bootstrapper = _BootStrapperWithoutPbfFile(data)
        try:
            bootstrapper.bootstrap()
            yield engine
        finally:
            cleanup_osmaxx_schemas(bootstrapper._postgres._engine)
    return import_data
