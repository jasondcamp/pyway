import pytest
import os
from strip_ansi import strip_ansi
from pyway.validate import Validate
from pyway.import_ import Import
from pyway.settings import ConfigFile

from mysqld_integration_test import Mysqld

VALIDATE_OUTPUT = """Validating --> V01_01__test1.sql
V01_01__test1.sql VALID
"""

@pytest.fixture
def mysqld_connect(autouse=True):
    mysqld = Mysqld()
    return mysqld.run()


@pytest.mark.validate_test
def test_pyway_table_validate(mysqld_connect):
    """ Import a file and validate that it matches """
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

    # Import file
    output = Import(config).run()
    output = Validate(config).run()
    assert strip_ansi(output) == VALIDATE_OUTPUT


@pytest.mark.validate_test
def test_pyway_table_validate_noschemasfound(mysqld_connect):
    """ Test to see what happens when we try to validate and no files are found """
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'empty')

    with pytest.raises(RuntimeError):
        output = Validate(config).run()

    assert True


@pytest.mark.validate_test
def test_pyway_table_validate_noschemasfound_skiperror(mysqld_connect):
    """ Test to see what happens when we try to validate and no files are found """
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'empty')

    output = Validate(config).run(skip_initial_check=True)
    assert output == ""


@pytest.mark.validate_test
def test_pyway_table_validate_nofilesfound(mysqld_connect):
    """ Test to see what happens when we try to validate and no files are found """
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

    # Change to an empty directory for local files
    config.database_migration_dir = os.path.join('tests', 'data', 'empty')

    with pytest.raises(RuntimeError):
        output = Validate(config).run()

    assert True


@pytest.mark.validate_test
def test_pyway_table_validate_diffname(mysqld_connect):
    """ Import a file and change the filename """
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

    # Import file
    output = Import(config).run()

    # Change the filename
    config.database_migration_dir = os.path.join('tests', 'data', 'schema_validate_diffname')   

    with pytest.raises(RuntimeError) as e:
        output = Validate(config).run()

    assert bool("with diff name of the database" in str(e.value))


@pytest.mark.validate_test
def test_pyway_table_validate_diffchecksum(mysqld_connect):
    """ Import a file and change the filename """
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

    # Import file
    output = Import(config).run()

    # Change the filename
    config.database_migration_dir = os.path.join('tests', 'data', 'schema_validate_diffchecksum')

    with pytest.raises(RuntimeError) as e:
        output = Validate(config).run()

    assert bool("with diff script" in str(e.value))


@pytest.mark.validate_test
def test_pyway_table_validate_diffchecksum_dos(mysqld_connect):
    """ Import a file and change the filename """
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

    # Import file
    output = Import(config).run()

    # Change the filename
    config.database_migration_dir = os.path.join('tests', 'data', 'schema_validate_diffchecksum_dos')

    with pytest.raises(RuntimeError) as e:
        output = Validate(config).run()

    assert bool("DOS" in str(e.value))


@pytest.mark.validate_test
def test_pyway_table_validate_outofdate(mysqld_connect):
    """ Import a file and remove that file """
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

    # Import file
    output = Import(config).run()

    # Import second file
    config.schema_file = "V01_02__test2.sql"
    output = Import(config).run()

    # Change to empty dir
    config.database_migration_dir = os.path.join('tests', 'data', 'schema_validate_outofdate')

    with pytest.raises(RuntimeError) as e:
       output = Validate(config).run()

    assert bool("Out of date" in str(e.value))
