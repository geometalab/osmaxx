import logging

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy_utils import functions as sql_alchemy_utils

logger = logging.getLogger()


class Postgres:
    def __init__(self, user, password, db_name, host=None, port=5432):
        self._connection_parameters = {
            'username': user,
            'password': password,
            'port': port,
            'database': db_name,
        }
        if host:
            self._connection_parameters['host'] = host
        connection_url = URL('postgresql', **self._connection_parameters)
        self._engine = create_engine(connection_url)

    def execute_sql_file(self, file_path):
        try:
            with open(file_path, 'r') as psql_command_file:
                return self.execute_sql_command(psql_command_file.read())
        except:  # noqa: E722 do not use bare 'except'
            logger.error("exception caught while processing %s", file_path)
            raise

    def execute_sql_command(self, sql):
        connection = self._engine.connect()
        with connection.begin():
            result = connection.execute(sqlalchemy.text(sql))
        return result

    def create_db(self):
        if not sql_alchemy_utils.database_exists(self._engine.url):
            sql_alchemy_utils.create_database(self._engine.url)

    def create_extension(self, extension):
        create_extension = "CREATE EXTENSION IF NOT EXISTS {extension};".format(
            extension=extension
        )
        return self.execute_sql_command(create_extension)

    def drop_db(self):
        if sql_alchemy_utils.database_exists(self._engine.url):
            sql_alchemy_utils.drop_database(self._engine.url)

    def get_db_name(self):
        return self._connection_parameters['database']

    def get_user(self):
        return self._connection_parameters['username']
