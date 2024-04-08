import pytest
import os
from strip_ansi import strip_ansi
from pyway.validate import Validate
from pyway.import_ import Import
from pyway.settings import ConfigFile

from pyway.dbms.database import factory

VALIDATE_OUTPUT = """Validating --> V01_01__test1.sql
V01_01__test1.sql VALID
"""


@pytest.fixture
def sqlite_connect(autouse: bool = True):
    # Delete any existing databases
    try:
        os.remove("./unittest-validate.sqlite")
    except Exception:
        pass

    args = ConfigFile()
    args.database_type = "sqlite"
    args.database_name = "./unittest-validate.sqlite"
    args.database_table = "pyway"

    return factory(args.database_type)(args)


@pytest.mark.validate_test
@pytest.mark.sqlite_test
def test_pyway_table_validate(sqlite_connect) -> None:
    """ Import a file and validate that it matches """
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-validate.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-sqlite')
    config.schema_file = "V01_01__test1.sql"

    # Import file
    output = Import(config).run()
    output = Validate(config).run()
    assert strip_ansi(output) == VALIDATE_OUTPUT


@pytest.mark.validate_test
@pytest.mark.sqlite_test
def test_pyway_table_validate_noschemasfound(sqlite_connect) -> None:
    """ Test to see what happens when we try to validate and no files are found """
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-validate.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'empty')

    with pytest.raises(RuntimeError):
        _ = Validate(config).run()

    assert True


@pytest.mark.validate_test
@pytest.mark.sqlite_test
def test_pyway_table_validate_noschemasfound_skiperror(sqlite_connect) -> None:
    """ Test to see what happens when we try to validate and no files are found """
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-validate.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'empty')

    output = Validate(config).run(skip_initial_check=True)
    assert output == ""


@pytest.mark.validate_test
@pytest.mark.sqlite_test
def test_pyway_table_validate_nofilesfound(sqlite_connect) -> None:
    """ Test to see what happens when we try to validate and no files are found """
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-validate.sqlite'
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
@pytest.mark.sqlite_test
def test_pyway_table_validate_diffname(sqlite_connect) -> None:
    """ Import a file and change the filename """
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-validate.sqlite'
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
@pytest.mark.sqlite_test
def test_pyway_table_validate_diffchecksum(sqlite_connect) -> None:
    """ Import a file and change the filename """
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-validate.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    config.schema_file = "V01_01__test1.sql"

    # Import file
    _ = Import(config).run()

    # Change the filename
    config.database_migration_dir = os.path.join('tests', 'data', 'schema_validate_diffchecksum')

    with pytest.raises(RuntimeError) as e:
        _ = Validate(config).run()

    assert bool("with diff script" in str(e.value))


@pytest.mark.validate_test
@pytest.mark.sqlite_test
def test_pyway_table_validate_diffchecksum_dos(sqlite_connect) -> None:
    """ Import a file and change the filename """
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-validate.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-sqlite')
    config.schema_file = "V01_01__test1.sql"

    # Import file
    _ = Import(config).run()

    # Change the filename
    config.database_migration_dir = os.path.join('tests', 'data', 'schema_validate_diffchecksum_dos')

    with pytest.raises(RuntimeError) as e:
        _ = Validate(config).run()

    assert bool("DOS" in str(e.value))


@pytest.mark.validate_test
@pytest.mark.sqlite_test
def test_pyway_table_validate_outofdate(sqlite_connect) -> None:
    """ Import a file and remove that file """
    config = ConfigFile()
    config.database_type = "sqlite"
    config.database_name = './unittest-validate.sqlite'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-sqlite')
    config.schema_file = "V01_01__test1.sql"

    # Import file
    _ = Import(config).run()

    # Import second file
    config.schema_file = "V01_02__test2.sql"
    _ = Import(config).run()

    config.database_migration_dir = os.path.join('tests', 'data', 'schema_validate_outofdate-sqlite')

    with pytest.raises(RuntimeError) as e:
        _ = Validate(config).run()

    assert bool("Out of date" in str(e.value))
