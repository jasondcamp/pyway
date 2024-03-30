import pytest
import os
from strip_ansi import strip_ansi
from pyway.info import Info
from pyway.settings import ConfigFile

from mysqld_integration_test import Mysqld

INFO_OUTPUT = """+-----------+-------------+-------------------+------------+-------------------+
|   version | extension   | name              | checksum   | apply_timestamp   |
|-----------+-------------+-------------------+------------+-------------------|
|      1.01 | SQL         | V01_01__test1.sql | new        | new               |
|      1.02 | SQL         | V01_02__test2.sql | new        | new               |
|      1.03 | SQL         | V01_03__test3.sql | new        | new               |
+-----------+-------------+-------------------+------------+-------------------+"""


@pytest.fixture
def mysqld_connect(autouse=True) -> Mysqld:
    mysqld = Mysqld()
    return mysqld.run()


@pytest.mark.info_test
@pytest.mark.mysqld_test
def test_pyway_info(mysqld_connect: Mysqld) -> None:
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


@pytest.mark.info_test
@pytest.mark.mysqld_test
def test_pyway_info_nofiles(mysqld_connect: Mysqld) -> None:
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'empty')

    files = Info(config).get_new_local_migrations([], config.database_migration_dir)
    assert files == []
