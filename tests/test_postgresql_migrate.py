import pytest
import os
from strip_ansi import strip_ansi
from pyway.migrate import Migrate
from pyway.settings import ConfigFile

from postgresql_integration_test import PostgreSQL

MIGRATE_OUTPUT = """Migrating --> V01_01__test1.sql
V01_01__test1.sql SUCCESS
Migrating --> V01_02__test2.sql
V01_02__test2.sql SUCCESS
Migrating --> V01_03__test3.sql
V01_03__test3.sql SUCCESS
"""


MIGRATE_OUTPUT_NOTHING = """Nothing to do
"""


@pytest.fixture
def postgresql_connect(autouse: bool = True) -> PostgreSQL:
    postgresql = PostgreSQL()
    return postgresql.run()


@pytest.mark.migrate_test
@pytest.mark.postgresql_test
def test_pyway_migrate(postgresql_connect: PostgreSQL) -> None:
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'public.pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-postgres')

    output = Migrate(config).run()
    assert strip_ansi(output) == MIGRATE_OUTPUT


@pytest.mark.migrate_test
@pytest.mark.postgresql_test
def test_pyway_migrate_nothingtodo(postgresql_connect: PostgreSQL) -> None:
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'public.pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-postgres')

    # Double migration to validate nothing
    output = Migrate(config).run()
    output = Migrate(config).run()

    assert strip_ansi(output) == MIGRATE_OUTPUT_NOTHING


@pytest.mark.migrate_test
@pytest.mark.postgresql_test
def test_pyway_migrate_no_local_files(postgresql_connect: PostgreSQL) -> None:
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'public.pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-postgres')
    config.schema_file = "V01_01__test1.sql"

    _ = Migrate(config).run()

    config.database_migration_dir = os.path.join('tests', 'data', 'empty')

    # Double migration to validate nothing
    with pytest.raises(RuntimeError) as e:
        _ = Migrate(config).run()

    assert bool("no local migration files found" in str(e.value))
