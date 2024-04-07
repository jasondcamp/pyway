import pytest
import os
from strip_ansi import strip_ansi
from pyway.info import Info
from pyway.settings import ConfigFile

from postgresql_integration_test import PostgreSQL

INFO_OUTPUT = """+-----------+-------------+-------------------+------------+-------------------+
|   version | extension   | name              | checksum   | apply_timestamp   |
|-----------+-------------+-------------------+------------+-------------------|
|      1.01 | SQL         | V01_01__test1.sql | new        | new               |
|      1.02 | SQL         | V01_02__test2.sql | new        | new               |
|      1.03 | SQL         | V01_03__test3.sql | new        | new               |
+-----------+-------------+-------------------+------------+-------------------+"""


@pytest.fixture
def postgresql_connect(autouse=True) -> PostgreSQL:
    postgresql = PostgreSQL()
    return postgresql.run()


@pytest.mark.info_test
@pytest.mark.postgresql_test
def test_pyway_info(postgresql_connect: PostgreSQL) -> None:
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'public.pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    tbl = Info(config).run()
    assert strip_ansi(tbl) == INFO_OUTPUT


@pytest.mark.info_test
@pytest.mark.postgresql_test
def test_pyway_info_nofiles(postgresql_connect: PostgreSQL) -> None:
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'public.pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'empty')

    files = Info(config).get_new_local_migrations([], config.database_migration_dir)
    assert files == []
