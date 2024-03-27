import pytest
import os
from strip_ansi import strip_ansi
from pyway.info import Info
from pyway.migrate import Migrate
from pyway.validate import Validate
from pyway.import_ import Import
from pyway.settings import ConfigFile
from pyway.version import __version__

from mysqld_integration_test import Mysqld

MIGRATE_OUTPUT = """Migrating --> V01_01__test1.sql
V01_01__test1.sql SUCCESS
Migrating --> V01_02__test2.sql
V01_02__test2.sql SUCCESS
Migrating --> V01_03__test3.sql
V01_03__test3.sql SUCCESS
"""


MIGRATE_OUTPUT_NOTHING = f"""Nothing to do
"""

@pytest.fixture
def mysqld_connect(autouse=True):
    mysqld = Mysqld()
    return mysqld.run()


@pytest.mark.migrate_test
def test_pyway_migrate(mysqld_connect):
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')


    output = Migrate(config).run()
    assert strip_ansi(output) == MIGRATE_OUTPUT


@pytest.mark.migrate_test
def test_pyway_migrate_nothingtodo(mysqld_connect):
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')

    # Double migration to validate nothing
    output = Migrate(config).run()
    output = Migrate(config).run()

    assert strip_ansi(output) == MIGRATE_OUTPUT_NOTHING

@pytest.mark.migrate_test
def test_pyway_migrate_no_local_files(mysqld_connect):
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    config.schema_file = "V01_01__test1.sql"

    output = Migrate(config).run()

    config.database_migration_dir = os.path.join('tests', 'data', 'empty')

    # Double migration to validate nothing
    with pytest.raises(RuntimeError) as e:
        output = Migrate(config).run()

    assert bool("no local migration files found" in str(e.value))


