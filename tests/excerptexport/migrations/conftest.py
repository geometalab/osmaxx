import pytest
from django.core.management import call_command
from django.db import connection
from django.db.migrations.executor import MigrationExecutor


@pytest.yield_fixture
def migrate(_executor, transactional_db):
    def _migrate(app_name, migration_name):
        migration = [(app_name, migration_name)]
        # For whatever reason, `executor.migrate(migration)` doesn't work in this context.
        # So we use the manage.py command instead:
        call_command('migrate', app_name, migration_name)
        apps_at_state = _executor.loader.project_state(migration).apps
        return apps_at_state

    yield _migrate

    # Back to latest state for following tests:
    call_command('migrate')


@pytest.fixture
def _executor():
    return MigrationExecutor(connection)
