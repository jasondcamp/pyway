import pytest
import os
from pyway.import_ import Import
from pyway.settings import ConfigFile

from pyway.dbms.database import factory

INFO_OUTPUT = """+-----------+-------------+-------------------+------------+-------------------+
|   version | extension   | name              | checksum   | apply_timestamp   |
|-----------+-------------+-------------------+------------+-------------------|
|      1.01 | SQL         | V01_01__test1.sql | new        | new               |
|      1.02 | SQL         | V01_02__test2.sql | new        | new               |
|      1.03 | SQL         | V01_03__test3.sql | new        | new               |
+-----------+-------------+-------------------+------------+-------------------+"""

VALIDATE_OUTPUT = """Validating --> V01_01__test1.sql
V01_01__test1.sql VALID
"""


@pytest.fixture
def sqlite_connect(autouse: bool = True):
    # Delete any existing databases
    try:
        os.remove("./unittest-import.sqlite")
    except Exception:
        pass

    args = ConfigFile()
    args.database_type = "sqlite"
    args.database_name = "./unittest-import.sqlite"
    args.database_table = "pyway"

    return factory(args.database_type)(args)


@pytest.mark.import_test
@pytest.mark.sqlite_test
def test_pyway_table_import(sqlite_connect) -> None:
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-import.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-sqlite')
    config.schema_file = "V01_01__test1.sql"
    output = Import(config).run()
    assert output == "V01_01__test1.sql"


@pytest.mark.import_test
@pytest.mark.sqlite_test
def test_pyway_table_import_fullfilepath(sqlite_connect) -> None:
    """ Schema file is specified with path """
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-import.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-sqlite')
    config.schema_file = f"{config.database_migration_dir}/V01_01__test1.sql"
    output = Import(config).run()
    assert output == "V01_01__test1.sql"


@pytest.mark.import_test
@pytest.mark.sqlite_test
def test_pyway_table_import_noschema(sqlite_connect) -> None:
    """ schema_file is missing from arguments """
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-import.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-sqlite')
    with pytest.raises(AttributeError):
        _ = Import(config).run()
    assert True


@pytest.mark.import_test
@pytest.mark.sqlite_test
def test_pyway_table_import_filenotfound(sqlite_connect) -> None:
    """ Schema file specified does not exist in migration_dir """
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-import.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-sqlite')
    config.schema_file = "V01_01__test1notfound.sql"
    with pytest.raises(FileNotFoundError):
        _ = Import(config).run()
    assert True


@pytest.mark.import_test
@pytest.mark.sqlite_test
def test_pyway_table_import_invalidfilename(sqlite_connect) -> None:
    """ Schema file exists but is not named properly """
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-import.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema_invalid_file')
    config.schema_file = "invalidfilename.sql"
    with pytest.raises(ValueError):
        _ = Import(config).run()
    assert True
