from contextlib import contextmanager

import pytest
import sqlalchemy

from osmaxx.converters.gis_converter.bootstrap.bootstrap import BootStrapper
from tests.inside_worker_test.conftest import slow, cleanup_osmaxx_schemas
from tests.inside_worker_test.declarative_schema import osm_models


@pytest.fixture()
def data_import(osmaxx_functions, clean_osm_tables, monkeypatch):
    assert osmaxx_functions == clean_osm_tables  # same db-connection
    engine = osmaxx_functions
    monkeypatch.setattr(
        'osmaxx.converters.gis_converter.helper.postgres_wrapper.create_engine', lambda *_, **__: engine)

    class _BootStrapperWithoutPbfFile(BootStrapper):
        def __init__(self, data, pbf_file_path=None, *args, **kwargs):
            assert pbf_file_path is None
            super().__init__(pbf_file_path=pbf_file_path, *args, **kwargs)
            self.data = data

        def _reset_database(self):
            pass  # Already taken care of by clean_osm_tables fixture.

        def _convert_osm_pbf_to_postgres(self):
            engine.execute(osm_models.t_osm_polygon.insert().values(**self.data).execution_options(autocommit=True))

        def _setup_db_functions(self):
            pass  # Already taken care of by osmaxx_functions fixture.

    @contextmanager
    def import_data(**data):
        bootstrapper = _BootStrapperWithoutPbfFile(data)
        try:
            bootstrapper.bootstrap()
            yield
        finally:
            cleanup_osmaxx_schemas(bootstrapper._postgres._engine)
    import_data.engine = engine
    return import_data


@slow
def test_osmaxx_data_model_processing_puts_amenity_grave_yard_with_religion_into_table_pow_a(data_import):
    engine = data_import.engine

    with data_import(amenity='grave_yard', religion='any value will do, as long as one is present'):
        try:
            t_pow_a = sqlalchemy.sql.schema.Table('pow_a', osm_models.metadata, schema='osmaxx')
            result = engine.execute(sqlalchemy.select([t_pow_a]))
            assert result.rowcount == 1
        finally:
            try:
                # Remove the result, as it would otherwise block the dropping of SCHEMA "osmaxx"
                # during the cleanup in the finalizer of the `data_import` fixture.
                del result
            except NameError:
                pass
