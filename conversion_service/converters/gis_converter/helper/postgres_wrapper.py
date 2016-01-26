import logging
import psycopg2

logger = logging.getLogger()


class Postgres:
    def __init__(self, user, password, db_name, host=None, port=5432, connect_timeout=10):
        self._connection_parameters = {
            'user': user,
            'password': password,
            'port': port,
            'connect_timeout': connect_timeout,
            'dbname': db_name,
        }
        if host:
            self._connection_parameters['host'] = host

    def execute_sql_file(self, file_path, connection=None, autocommit=False, fetch_result=True):
        try:
            with open(file_path, 'r') as psql_command_file:
                return self.execute_sql_command(
                    psql_command_file.read(),
                    connection=connection,
                    autocommit=autocommit,
                    fetch_result=fetch_result
                )
        except:
            logger.error("exception caught while processing %s", file_path)
            raise

    def execute_sql_command(self, sql, connection=None, autocommit=False, fetch_result=True):
        if connection is None:
            connection = self._get_connection()
        if autocommit:
            connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor

    def create_db(self):
        create_db = "CREATE DATABASE {db_name} OWNER {user} ENCODING 'utf-8';".format(
            db_name=self.get_db_name(),
            user=self.get_user(),
        )
        connection_parameters = self._db_less_connection_params()
        connection = self._get_connection(connection_parameters)
        return self.execute_sql_command(create_db, connection=connection, autocommit=True)

    def create_extension(self, extension):
        create_extension = "CREATE EXTENSION IF NOT EXISTS {extension};".format(
            extension=extension,
            user=self.get_user(),
        )
        return self.execute_sql_command(create_extension, autocommit=True)

    def drop_db(self, if_exists=True):
        if if_exists:
            drop_db = "DROP DATABASE IF EXISTS {db_name};"
        else:
            drop_db = "DROP DATABASE {db_name};"
        drop_db = drop_db.format(
            db_name=self.get_db_name()
        )
        connection_parameters = self._db_less_connection_params()
        connection = self._get_connection(connection_parameters)
        return self.execute_sql_command(drop_db, connection=connection, autocommit=True)

    def get_db_name(self):
        return self._connection_parameters['dbname']

    def get_user(self):
        return self._connection_parameters['user']

    def _get_connection(self, connection_parameters=None):
        if connection_parameters is None:
            connection_parameters = self._connection_parameters
        return psycopg2.connect(**connection_parameters)

    def _db_less_connection_params(self):
        connection_params = self._connection_parameters.copy()
        connection_params.pop('dbname')
        return connection_params

    def _assemble_psql_call(self, call_args):
        call_base = ['psql', '-U', self.get_user(), 'ON_ERROR_STOP=1']
        call = call_base + call_args
        call += ['-d', self.get_db_name()]
        return call
