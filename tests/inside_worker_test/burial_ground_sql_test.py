from contextlib import contextmanager, closing

import pytest
import sqlalchemy
from sqlalchemy.sql.schema import Table as DbTable

from tests.inside_worker_test.conftest import slow
from tests.inside_worker_test.declarative_schema import osm_models


@slow
def test_osmaxx_data_model_processing_puts_amenity_grave_yard_with_religion_into_table_pow_a(data_import):
    data = dict(
        amenity='grave_yard',
        religion='any value will do, as long as one is present',
    )
    with data_import(data) as engine:
        t_pow_a = DbTable('pow_a', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_pow_a]))) as result:
            assert result.rowcount == 1


@pytest.fixture()
def data_import(osmaxx_functions, clean_osm_tables, monkeypatch):
    from osmaxx.converters.gis_converter.bootstrap.bootstrap import BootStrapper
    from tests.inside_worker_test.conftest import cleanup_osmaxx_schemas

    assert osmaxx_functions == clean_osm_tables  # same db-connection
    engine = osmaxx_functions
    monkeypatch.setattr(
        'osmaxx.converters.gis_converter.helper.postgres_wrapper.create_engine', lambda *_, **__: engine)

    class _BootStrapperWithoutPbfFile(BootStrapper):
        def __init__(self, data):
            super().__init__(pbf_file_path=None)
            self.data = data

        def _reset_database(self):
            pass  # Already taken care of by clean_osm_tables fixture.

        def _convert_osm_pbf_to_postgres(self):
            engine.execute(osm_models.t_osm_polygon.insert().values(**self.data).execution_options(autocommit=True))

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
