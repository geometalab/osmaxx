import logging

import sqlalchemy
from sqlalchemy import create_engine, event

from sqlalchemy.engine.url import URL
from sqlalchemy_utils import functions as sql_alchemy_utils

logger = logging.getLogger()


class Postgres:
    def __init__(
        self, user, password, db_name, host="localhost", port=5432, search_path=None
    ):
        self._connection_parameters = {
            "username": user,
            "password": password,
            "port": port,
            "database": db_name,
            "host": host,
        }
        connection_url = URL("postgresql", **self._connection_parameters)

        self._engine = create_engine(connection_url, echo=False)
        if search_path:

            @event.listens_for(self._engine, "connect", insert=True)
            def set_search_path(dbapi_connection, connection_record):
                existing_autocommit = dbapi_connection.autocommit
                dbapi_connection.autocommit = True
                cursor = dbapi_connection.cursor()
                cursor.execute("SET SESSION search_path='{search_path}'")
                cursor.close()
                dbapi_connection.autocommit = existing_autocommit

    def execute_sql_file(self, file_path):
        try:
            with open(file_path, "r") as psql_command_file:
                return self.execute_sql_command(psql_command_file.read())
        except:  # noqa: E722 do not use bare 'except'
            logger.error("exception caught while processing %s", file_path)
            raise

    def execute_sql_command(self, sql):
        # connection = self._engine.raw_connection()
        # try:
        #     cursor_obj = connection.cursor()
        #     result = cursor_obj.execute(sql)
        # finally:
        #     connection.close()
        with self._engine.begin() as connection:
            result = connection.execute(sqlalchemy.text(sql))
        return result

    def create_db(self):
        if not sql_alchemy_utils.database_exists(self._engine.url):
            sql_alchemy_utils.create_database(self._engine.url)

    def create_schema(self, schema_name):
        create_schema = f"CREATE SCHEMA IF NOT EXISTS {schema_name};"
        return self.execute_sql_command(create_schema)

    def create_extension(self, extension, schema=None):
        create_extension = f"CREATE EXTENSION IF NOT EXISTS {extension} CASCADE;"
        if schema:
            create_extension = f"CREATE EXTENSION IF NOT EXISTS {extension} WITH SCHEMA {schema} CASCADE;"

        return self.execute_sql_command(create_extension)

    def drop_db(self):
        if sql_alchemy_utils.database_exists(self._engine.url):
            sql_alchemy_utils.drop_database(self._engine.url)

    def drop_schema(self, schema_name):
        drop_schema = f"DROP SCHEMA IF EXISTS {schema_name};"
        return self.execute_sql_command(drop_schema)

    def get_db_name(self):
        return self._connection_parameters["database"]

    def get_user(self):
        return self._connection_parameters["username"]

    def get_host(self):
        return self._connection_parameters.get("host")

    def get_password(self):
        return self._connection_parameters.get("password")

    def get_port(self):
        return self._connection_parameters["port"]
