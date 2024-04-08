import pytest
import os
from strip_ansi import strip_ansi
from pyway.migrate import Migrate
from pyway.settings import ConfigFile

from pyway.dbms.database import factory

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
def sqlite_connect(autouse: bool = True):
    # Delete any existing databases
    try:
        os.remove("./unittest-migrate.sqlite")
    except Exception:
        pass

    args = ConfigFile()
    args.database_type = "sqlite"
    args.database_name = "./unittest-migrate.sqlite"
    args.database_table = "pyway"

    return factory(args.database_type)(args)


@pytest.mark.migrate_test
@pytest.mark.sqlite_test
def test_pyway_migrate(sqlite_connect) -> None:
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-migrate.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-sqlite')

    output = Migrate(config).run()
    assert strip_ansi(output) == MIGRATE_OUTPUT


@pytest.mark.migrate_test
@pytest.mark.sqlite_test
def test_pyway_migrate_nothingtodo(sqlite_connect) -> None:
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-migrate.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-sqlite')

    # Double migration to validate nothing
    output = Migrate(config).run()
    output = Migrate(config).run()

    assert strip_ansi(output) == MIGRATE_OUTPUT_NOTHING


@pytest.mark.migrate_test
@pytest.mark.sqlite_test
def test_pyway_migrate_no_local_files(sqlite_connect) -> None:
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-migrate.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-sqlite')
    config.schema_file = "V01_01__test1.sql"

    _ = Migrate(config).run()

    config.database_migration_dir = os.path.join('tests', 'data', 'empty')

    # Double migration to validate nothing
    with pytest.raises(RuntimeError) as e:
        _ = Migrate(config).run()

    assert bool("no local migration files found" in str(e.value))
