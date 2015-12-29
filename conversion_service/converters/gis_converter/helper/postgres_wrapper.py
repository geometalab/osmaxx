import subprocess

import psycopg2


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

    def execute_raw(self, sql, connection=None, autocommit=False):
        if connection is None:
            connection = self._get_connection()
        if autocommit:
            connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        return cursor.execute(sql)

    def execute_psql(self, sql=None, sql_file_path=None, extra_args=None):
        assert sql or sql_file_path is not None
        call = ['psql', '-U', self.get_user(), 'ON_ERROR_STOP=1']
        if sql:
            call += ['-c', sql]
        else:
            call += ['-f', sql_file_path]
        if extra_args:
            call += extra_args
        call += ['-d', self.get_db_name()]
        subprocess.check_call(call)

    def create_db(self):
        create_db = "CREATE DATABASE {db_name} OWNER {user} ENCODING 'utf-8';".format(
            db_name=self.get_db_name(),
            user=self.get_user(),
        )
        connection_parameters = self._db_less_connection_params()
        connection = self._get_connection(connection_parameters)
        return self.execute_raw(create_db, connection=connection, autocommit=True)

    def create_extension(self, extension):
        create_extension = "CREATE EXTENSION IF NOT EXISTS {extension};".format(
            extension=extension,
            user=self.get_user(),
        )
        return self.execute_raw(create_extension, autocommit=True)

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
        return self.execute_raw(drop_db, connection=connection, autocommit=True)

    def get_db_name(self):
        return self._connection_parameters['dbname']

    def get_user(self):
        return self._connection_parameters['user']

    def _get_connection(self, connection_parameters=None):
        if connection_parameters is None:
            connection_parameters = self._connection_parameters
            psycopg2.connect(**connection_parameters)
        return psycopg2.connect(**connection_parameters)

    def _db_less_connection_params(self):
        connection_params = self._connection_parameters.copy()
        connection_params.pop('dbname')
        return connection_params
