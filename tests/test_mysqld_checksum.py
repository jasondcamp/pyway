import pytest
import os
from pyway.checksum import Checksum
from pyway.migrate import Migrate
from pyway.settings import ConfigFile

from mysqld_integration_test import Mysqld


@pytest.fixture
def mysqld_connect(autouse: bool = True) -> Mysqld:
    mysqld = Mysqld()
    return mysqld.run()


@pytest.mark.checksum_test
@pytest.mark.mysqld_test
def test_pyway_table_checksum(mysqld_connect: Mysqld) -> None:
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    config.checksum_file = "V01_01__test1.sql"

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    name, checksum = Checksum(config).run()
    assert name == "V01_01__test1.sql"
    assert checksum == "8327AD7B"


@pytest.mark.checksum_test
@pytest.mark.mysqld_test
def test_pyway_table_checksum_fileinvalid(mysqld_connect: Mysqld) -> None:
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    with pytest.raises(AttributeError):
        _, _ = Checksum(config).run()

    assert True


@pytest.mark.checksum_test
@pytest.mark.mysqld_test
def test_pyway_table_checksum_fullpath(mysqld_connect: Mysqld) -> None:
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    config.checksum_file = "schema/V01_01__test1.sql"

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    name, checksum = Checksum(config).run()
    assert name == "V01_01__test1.sql"
    assert checksum == "8327AD7B"


@pytest.mark.checksum_test
@pytest.mark.mysqld_test
def test_pyway_table_checksum_invalid_filename(mysqld_connect: Mysqld) -> None:
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    config.checksum_file = "invalidfilename.sql"

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    with pytest.raises(FileNotFoundError):
        _, _ = Checksum(config).run()

    assert True
