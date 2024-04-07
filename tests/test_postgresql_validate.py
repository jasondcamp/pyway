import pytest
import os
from strip_ansi import strip_ansi
from pyway.validate import Validate
from pyway.import_ import Import
from pyway.settings import ConfigFile

from postgresql_integration_test import PostgreSQL

VALIDATE_OUTPUT = """Validating --> V01_01__test1.sql
V01_01__test1.sql VALID
"""


@pytest.fixture
def postgresql_connect(autouse: bool = True) -> PostgreSQL:
    postgresql = PostgreSQL()
    return postgresql.run()


@pytest.mark.validate_test
@pytest.mark.postgresql_test
def test_pyway_table_validate(postgresql_connect: PostgreSQL) -> None:
    """ Import a file and validate that it matches """
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    config.schema_file = "V01_01__test1.sql"

    # Import file
    output = Import(config).run()
    output = Validate(config).run()
    assert strip_ansi(output) == VALIDATE_OUTPUT


@pytest.mark.validate_test
@pytest.mark.postgresql_test
def test_pyway_table_validate_noschemasfound(postgresql_connect: PostgreSQL) -> None:
    """ Test to see what happens when we try to validate and no files are found """
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'empty')

    with pytest.raises(RuntimeError):
        _ = Validate(config).run()

    assert True


@pytest.mark.validate_test
@pytest.mark.postgresql_test
def test_pyway_table_validate_noschemasfound_skiperror(postgresql_connect: PostgreSQL) -> None:
    """ Test to see what happens when we try to validate and no files are found """
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'empty')

    output = Validate(config).run(skip_initial_check=True)
    assert output == ""


@pytest.mark.validate_test
@pytest.mark.postgresql_test
def test_pyway_table_validate_nofilesfound(postgresql_connect: PostgreSQL) -> None:
    """ Test to see what happens when we try to validate and no files are found """
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    config.schema_file = "V01_01__test1.sql"

    _ = Import(config).run()

    # Change to an empty directory for local files
    config.database_migration_dir = os.path.join('tests', 'data', 'empty')

    with pytest.raises(RuntimeError):
        _ = Validate(config).run()

    assert True


@pytest.mark.validate_test
@pytest.mark.postgresql_test
def test_pyway_table_validate_diffname(postgresql_connect: PostgreSQL) -> None:
    """ Import a file and change the filename """
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    config.schema_file = "V01_01__test1.sql"

    # Import file
    _ = Import(config).run()

    # Change the filename
    config.database_migration_dir = os.path.join('tests', 'data', 'schema_validate_diffname')

    with pytest.raises(RuntimeError) as e:
        _ = Validate(config).run()

    assert bool("with diff name of the database" in str(e.value))


@pytest.mark.validate_test
@pytest.mark.postgresql_test
def test_pyway_table_validate_diffchecksum(postgresql_connect: PostgreSQL) -> None:
    """ Import a file and change the filename """
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-postgres')
    config.schema_file = "V01_01__test1.sql"

    # Import file
    _ = Import(config).run()

    # Change the filename
    config.database_migration_dir = os.path.join('tests', 'data', 'schema_validate_diffchecksum')

    with pytest.raises(RuntimeError) as e:
        _ = Validate(config).run()

    assert bool("with diff script" in str(e.value))


@pytest.mark.validate_test
@pytest.mark.postgresql_test
def test_pyway_table_validate_diffchecksum_dos(postgresql_connect: PostgreSQL) -> None:
    """ Import a file and change the filename """
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    config.schema_file = "V01_01__test1.sql"

    # Import file
    _ = Import(config).run()

    # Change the filename
    config.database_migration_dir = os.path.join('tests', 'data', 'schema_validate_diffchecksum_dos')

    with pytest.raises(RuntimeError) as e:
        _ = Validate(config).run()

    assert bool("DOS" in str(e.value))


@pytest.mark.validate_test
@pytest.mark.postgresql_test
def test_pyway_table_validate_outofdate(postgresql_connect: PostgreSQL) -> None:
    """ Import a file and remove that file """
    config = ConfigFile()
    config.database_type = "postgres"
    config.database_host = postgresql_connect.host
    config.database_username = postgresql_connect.username
    config.database_port = postgresql_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    config.schema_file = "V01_01__test1.sql"

    # Import file
    _ = Import(config).run()

    # Import second file
    config.schema_file = "V01_02__test2.sql"
    _ = Import(config).run()

    # Change to empty dir
    config.database_migration_dir = os.path.join('tests', 'data', 'schema_validate_outofdate')

    with pytest.raises(RuntimeError) as e:
        _ = Validate(config).run()

    assert bool("Out of date" in str(e.value))
