import pytest
import os
from strip_ansi import strip_ansi
from pyway.info import Info
from pyway.settings import ConfigFile

from pyway.dbms.database import factory

INFO_OUTPUT = """+-----------+-------------+-------------------+------------+-------------------+
|   version | extension   | name              | checksum   | apply_timestamp   |
|-----------+-------------+-------------------+------------+-------------------|
|      1.01 | SQL         | V01_01__test1.sql | new        | new               |
|      1.02 | SQL         | V01_02__test2.sql | new        | new               |
|      1.03 | SQL         | V01_03__test3.sql | new        | new               |
+-----------+-------------+-------------------+------------+-------------------+"""


@pytest.fixture
def sqlite_connect(autouse: bool = True):
    # Delete any existing databases
    try:
        os.remove("./unittest-info.sqlite")
    except Exception:
        pass

    args = ConfigFile()
    args.database_type = "sqlite"
    args.database_name = "./unittest-info.sqlite"
    args.database_table = "pyway"

    return factory(args.database_type)(args)


@pytest.mark.info_test
@pytest.mark.sqlite_test
def test_pyway_info(sqlite_connect) -> None:
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-info.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-sqlite')
    tbl = Info(config).run()
    assert strip_ansi(tbl) == INFO_OUTPUT


@pytest.mark.info_test
@pytest.mark.sqlite_test
def test_pyway_info_nofiles(sqlite_connect) -> None:
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-info.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'empty')

    files = Info(config).get_new_local_migrations([], config.database_migration_dir)
    assert files == []
