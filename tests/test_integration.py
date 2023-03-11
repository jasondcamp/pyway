import pytest
import os
from strip_ansi import strip_ansi
from pyway.info import Info
# from pyway.migrate import Migrate
# from pyway.validate import Validate
from pyway.import_ import Import
# from pyway.settings import Settings
from pyway.settings import ConfigFile
# from pyway.migration import Migration
# from pyway.version import __version__

from mysqld_integration_test import Mysqld

INFO_OUTPUT = """+-----------+-------------+-------------------+------------+-------------------+
|   version | extension   | name              | checksum   | apply_timestamp   |
|-----------+-------------+-------------------+------------+-------------------|
|      1.01 | SQL         | V01_01__test1.sql | new        | new               |
|      1.02 | SQL         | V01_02__test2.sql | new        | new               |
|      1.03 | SQL         | V01_03__test3.sql | new        | new               |
+-----------+-------------+-------------------+------------+-------------------+"""


@pytest.fixture
def mysqld_connect(autouse=True):
    mysqld = Mysqld()
    return mysqld.run()


@pytest.mark.integration_test
def test_pyway_table_creation(mysqld_connect):
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    tbl = Info(config).run()
    assert strip_ansi(tbl) == INFO_OUTPUT


@pytest.mark.integration_test
def test_pyway_table_import(mysqld_connect):
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
    output = Import(config).run()
    assert output == "V01_01__test1.sql"


@pytest.mark.integration_test
def test_pyway_table_import_noschema(mysqld_connect):
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    with pytest.raises(Exception):
        _ = Import(config).run()
    assert True


@pytest.mark.integration_test
def test_pyway_table_import_invalidfile(mysqld_connect):
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    config.schema_file = "V01_01__test1notfound.sql"
    with pytest.raises(Exception):
        _ = Import(config).run()
    assert True


@pytest.mark.integration_test
def test_pyway_table_import_filenotfound(mysqld_connect):
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    config.schema_file = "test1notfound.sql"
    with pytest.raises(Exception):
        _ = Import(config).run()
    assert True
