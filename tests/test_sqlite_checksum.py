import pytest
import os
from pyway.checksum import Checksum
from pyway.migrate import Migrate
from pyway.settings import ConfigFile

from pyway.dbms.database import factory


@pytest.fixture
def sqlite_connect(autouse: bool = True):
    # Delete any existing databases
    try:
        os.remove("./unittest-checksum.sqlite")
    except Exception:
        pass

    args = ConfigFile()
    args.database_type = "sqlite"
    args.database_name = "./unittest-checksum.sqlite"
    args.database_table = "pyway"

    return factory(args.database_type)(args)


@pytest.mark.checksum_test
@pytest.mark.sqlite_test
def test_pyway_table_checksum(sqlite_connect) -> None:
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = "./unittest-checksum.sqlite"
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-sqlite')
    config.checksum_file = "V01_01__test1.sql"

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    name, checksum = Checksum(config).run()
    assert name == "V01_01__test1.sql"
    assert checksum == "9B8E1E62"


@pytest.mark.checksum_test
@pytest.mark.sqlite_test
def test_pyway_table_checksum_fileinvalid(sqlite_connect) -> None:
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-checksum.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-sqlite')

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    with pytest.raises(AttributeError):
        _, _ = Checksum(config).run()

    assert True


@pytest.mark.checksum_test
@pytest.mark.sqlite_test
def test_pyway_table_checksum_fullpath(sqlite_connect) -> None:
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-checksum.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-sqlite')
    config.checksum_file = "schema/V01_01__test1.sql"

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    name, checksum = Checksum(config).run()
    assert name == "V01_01__test1.sql"
    assert checksum == "9B8E1E62"


@pytest.mark.checksum_test
@pytest.mark.sqlite_test
def test_pyway_table_checksum_invalid_filename(sqlite_connect) -> None:
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-checksum.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-sqlite')
    config.checksum_file = "invalidfilename.sql"

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    with pytest.raises(FileNotFoundError):
        _, _ = Checksum(config).run()

    assert True
