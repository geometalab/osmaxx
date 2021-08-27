from sqlalchemy import MetaData, Table, func, text
from sqlalchemy.engine.url import URL
from sqlalchemy.sql import select, insert, expression
from geoalchemy2 import Geometry, Geography
from osmaxx.conversion.converters.converter_gis.helper.default_postgres import (
    get_default_postgres_wrapper,
)

from osmaxx.conversion._settings import CONVERSION_SETTINGS


class OSMBoundariesImporter:
    def __init__(self):
        self._osm_boundaries_tables = ["sea_a", "coastline_l", "landmass_a"]
        self._osm_boundaries_pgwrapper = get_default_postgres_wrapper(
            db_name=CONVERSION_SETTINGS["OSM_BOUNDARIES_DB_NAME"],
        )
        self._destination_db_wrapper = get_default_postgres_wrapper()

        assert (
            Geometry
        ), Geography  # assert classes needed for GIS-reflection are available
        self._db_meta_data = MetaData()
        self._table_metas = self._get_meta_tables()

    def _autoinspect_tables(self, tables, autoloader):
        return {
            table: Table(
                table,
                self._db_meta_data,
                autoload=True,
                autoload_with=autoloader,
            )
            for table in tables
        }

    def _get_meta_tables(self):
        meta_boundaries = self._autoinspect_tables(
            tables=self._osm_boundaries_tables,
            autoloader=self._osm_boundaries_pgwrapper._engine,
        )
        return meta_boundaries

    def load_area_specific_data(self, *, extent):
        self._create_tables_on_local_db()
        print("lading data tables")
        self._load_boundaries_tables(extent)

    def _create_tables_on_local_db(self):
        print("creating tables")
        # print(self._table_metas)
        with self._destination_db_wrapper._engine.connect() as conn:
            conn.execute(
                text('CREATE EXTENSION IF NOT EXISTS postgis SCHEMA "public";')
            )
            conn.commit()
            print(self._db_meta_data.create_all(conn))

    def _load_boundaries_tables(self, extent):
        multipolygon_cast = Geometry(geometry_type="MULTIPOLYGON", srid=4326)
        multilinestring_cast = Geometry(geometry_type="MULTILINESTRING", srid=4326)
        table_casts = {
            "sea_a": multipolygon_cast,
            "landmass_a": multipolygon_cast,
            "coastline_l": multilinestring_cast,
        }
        for table_name in self._osm_boundaries_tables:
            print(30 * "#", f"processing {table_name}")
            source_table_meta = self._table_metas[table_name]
            field_selection = source_table_meta.c
            query = select(field_selection)
            query = query.where(
                func.ST_Intersects(source_table_meta.c.wkb_geometry, extent.ewkt)
            )
            self._execute_and_insert_into_local_db(
                query,
                source_table_meta,
            )
            from sqlalchemy_views import CreateView

            field_selection = [c for c in source_table_meta.c]
            field_selection.append(
                expression.cast(
                    func.ST_Multi(
                        func.ST_Intersection(
                            source_table_meta.c.wkb_geometry, extent.ewkt
                        )
                    ),
                    table_casts[table_name],
                ).label("geom")
            )

            view_definition_query = select(field_selection).where(
                func.ST_Intersects(source_table_meta.c.wkb_geometry, extent.ewkt)
            )

            view_meta = MetaData()
            view = Table(
                table_name,
                view_meta,
                schema=CONVERSION_SETTINGS["CONVERSION_SCHEMA_NAME_TMP_VIEW"],
            )
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
            self._destination_db_wrapper.execute_sql_command(create_view)

    def _execute_and_insert_into_local_db(self, query, table_meta):
        query_result = self._osm_boundaries_pgwrapper.execute_sql_command(query)
        if query_result.rowcount > 0:
            results = query_result.fetchall()
            for result in results:
                self._destination_db_wrapper.execute_sql_command(
                    insert(table_meta, values=result)
                )
