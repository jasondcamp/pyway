import pytest
import os
from pyway.import_ import Import
from pyway.settings import ConfigFile
# from pyway.migration import Migration

from mysqld_integration_test import Mysqld

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
def mysqld_connect(autouse: bool = True) -> Mysqld:
    mysqld = Mysqld()
    return mysqld.run()


@pytest.mark.import_test
@pytest.mark.mysqld_test
def test_pyway_table_import(mysqld_connect: Mysqld) -> None:
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


@pytest.mark.import_test
@pytest.mark.mysqld_test
def test_pyway_table_import_fullfilepath(mysqld_connect: Mysqld) -> None:
    """ Schema file is specified with path """
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    config.schema_file = f"{config.database_migration_dir}/V01_01__test1.sql"
    output = Import(config).run()
    assert output == "V01_01__test1.sql"


@pytest.mark.import_test
@pytest.mark.mysqld_test
def test_pyway_table_import_noschema(mysqld_connect: Mysqld) -> None:
    """ schema_file is missing from arguments """
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    with pytest.raises(AttributeError):
        _ = Import(config).run()
    assert True


@pytest.mark.import_test
@pytest.mark.mysqld_test
def test_pyway_table_import_filenotfound(mysqld_connect: Mysqld) -> None:
    """ Schema file specified does not exist in migration_dir """
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
    with pytest.raises(FileNotFoundError):
        _ = Import(config).run()
    assert True


@pytest.mark.import_test
@pytest.mark.mysqld_test
def test_pyway_table_import_invalidfilename(mysqld_connect: Mysqld) -> None:
    """ Schema file exists but is not named properly """
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema_invalid_file')
    config.schema_file = "invalidfilename.sql"
    with pytest.raises(ValueError):
        _ = Import(config).run()
    assert True
