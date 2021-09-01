from sqlalchemy import MetaData, Table, func, text
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.sql import select, insert, expression
from geoalchemy2 import Geometry, Geography
from osmaxx.conversion.converters.converter_gis.helper.default_postgres import (
    get_default_postgres_wrapper,
)

from osmaxx.conversion.conversion_settings import DBConfig


class OSMBoundariesImporter:
    def __init__(self, db_config: DBConfig):
        self._db_view_name = db_config.db_schema_tmp_view
        self._osm_boundaries_tables = ["coastline_l", "landmass_a", "sea_a"]

        _osm_boundaries_db_connection_parameters = dict(
            username=db_config.user,
            password=db_config.password,
            database=db_config.boundaries_db,
            host=db_config.host,
        )
        osm_boundaries_db_connection = URL(
            "postgresql", **_osm_boundaries_db_connection_parameters
        )
        self._osm_boundaries_db_engine = create_engine(osm_boundaries_db_connection)

        _local_db_connection_parameters = dict(
            username=db_config.user,
            password=db_config.password,
            database=db_config.db_name,
            host=db_config.host,
        )
        local_db_connection = URL("postgresql", **_local_db_connection_parameters)
        self._local_db_engine = create_engine(local_db_connection)

        assert (
            Geometry
        ), Geography  # assert classes needed for GIS-reflection are available
        self._db_meta_data = MetaData()
        self._table_metas = self._get_meta_tables()

    def _autoinspect_tables(self, tables, autoloader):
        return {
            table: Table(
                table, self._db_meta_data, autoload=True, autoload_with=autoloader
            )
            for table in tables
        }

    def _get_meta_tables(self):
        meta_boundaries = self._autoinspect_tables(
            tables=self._osm_boundaries_tables,
            autoloader=self._osm_boundaries_db_engine,
        )
        return meta_boundaries

    def load_area_specific_data(self, *, extent):
        self._create_tables_on_local_db()
        self._load_boundaries_tables(extent)

    def _create_tables_on_local_db(self):
        self._db_meta_data.create_all(self._local_db_engine)

    def _load_boundaries_tables(self, extent):
        multipolygon_cast = Geometry(geometry_type="MULTIPOLYGON", srid=4326)
        multilinestring_cast = Geometry(geometry_type="MULTILINESTRING", srid=4326)
        table_casts = {
            "sea_a": multipolygon_cast,
            "landmass_a": multipolygon_cast,
            "coastline_l": multilinestring_cast,
        }
        for table_name in self._osm_boundaries_tables:
            source_table_meta = self._table_metas[table_name]
            query = select(source_table_meta.c)
            query = query.where(
                func.ST_Intersects(source_table_meta.c.wkb_geometry, extent.ewkt)
            )
            self._execute_and_insert_into_local_db(
                query, source_table_meta, source_engine=self._osm_boundaries_db_engine
            )
            from sqlalchemy_views import CreateView

            selection = [c for c in source_table_meta.c]
            selection.append(
                expression.cast(
                    func.ST_Multi(
                        func.ST_Intersection(
                            source_table_meta.c.wkb_geometry, extent.ewkt
                        )
                    ),
                    table_casts[table_name],
                ).label("geom")
            )
            view_definition_query = select(selection).where(
                func.ST_Intersects(source_table_meta.c.wkb_geometry, extent.ewkt)
            )
            view_meta = MetaData()
            view = Table(table_name, view_meta, schema=self._db_view_name)

            from sqlalchemy.dialects import postgresql
            from sqlalchemy.sql import text

            query_defintion_string = str(
                view_definition_query.compile(
                    dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
                )
            )
            query_defintion_string = query_defintion_string.replace(
                "ST_AsEWKB(CAST", "CAST"
            )
            query_defintion_string = query_defintion_string.replace(
                "))) AS geom", ")) AS geom"
            )
            query_defintion_text = text(query_defintion_string)
            create_view = CreateView(view, query_defintion_text, or_replace=True)
            self._local_db_engine.execute(create_view)

    def _execute_and_insert_into_local_db(self, query, table_meta, source_engine=None):
        query_result = source_engine.execute(query)
        if query_result.rowcount > 0:
            results = query_result.fetchall()
            for result in results:
                self._local_db_engine.execute(insert(table_meta, values=result))
