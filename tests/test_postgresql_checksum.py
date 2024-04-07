import pytest
import os
from pyway.checksum import Checksum
from pyway.migrate import Migrate
from pyway.settings import ConfigFile

from postgresql_integration_test import PostgreSQL


@pytest.fixture
def postgresql_connect(autouse: bool = True) -> PostgreSQL:
    postgresql = PostgreSQL()
    return postgresql.run()


@pytest.mark.checksum_test
@pytest.mark.postgresql_test
def test_pyway_table_checksum(postgresql_connect: PostgreSQL) -> None:
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'public.pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-postgres')
    config.checksum_file = "V01_01__test1.sql"

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    name, checksum = Checksum(config).run()
    assert name == "V01_01__test1.sql"
    assert checksum == "B78E2BE3"


@pytest.mark.checksum_test
@pytest.mark.postgresql_test
def test_pyway_table_checksum_fileinvalid(postgresql_connect: PostgreSQL) -> None:
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'public.pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-postgres')

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    with pytest.raises(AttributeError):
        _, _ = Checksum(config).run()

    assert True


@pytest.mark.checksum_test
@pytest.mark.postgresql_test
def test_pyway_table_checksum_fullpath(postgresql_connect: PostgreSQL) -> None:
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'public.pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-postgres')
    config.checksum_file = "schema/V01_01__test1.sql"

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    name, checksum = Checksum(config).run()
    assert name == "V01_01__test1.sql"
    assert checksum == "B78E2BE3"


@pytest.mark.checksum_test
@pytest.mark.postgresql_test
def test_pyway_table_checksum_invalid_filename(postgresql_connect: PostgreSQL) -> None:
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'public.pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-postgres')
    config.checksum_file = "invalidfilename.sql"

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    with pytest.raises(FileNotFoundError):
        _, _ = Checksum(config).run()

    assert True
