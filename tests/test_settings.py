import pytest
import os
import sys
from pyway.settings import ConfigFile
from pyway.settings import Settings
from pyway.settings import ARGS
from pyway.configfile import MockConfig
from pyway.configfile import MockArgs


# Make sure config options exists and check some defaults
@pytest.mark.settings_test
def test_settings_database_migration_dir() -> None:
    config = ConfigFile()
    assert config.database_migration_dir == 'resources'


@pytest.mark.settings_test
def test_settings_database_table() -> None:
    config = ConfigFile(database_table='public.pyway')
    assert config.database_table == 'public.pyway'


@pytest.mark.settings_test
def test_settings_database_type() -> None:
    config = ConfigFile(database_type='postgres')
    assert config.database_type == 'postgres'


@pytest.mark.settings_test
def test_settings_database_host() -> None:
    config = ConfigFile(database_host='localhost')
    assert config.database_host == 'localhost'


@pytest.mark.settings_test
def test_settings_database_port() -> None:
    config = ConfigFile(database_port='5432')
    assert config.database_port == '5432'


@pytest.mark.settings_test
def test_settings_database_name() -> None:
    config = ConfigFile(database_name='postgres')
    assert config.database_name == 'postgres'


@pytest.mark.settings_test
def test_settings_database_username() -> None:
    config = ConfigFile(database_username='postgres')
    assert config.database_username == 'postgres'


@pytest.mark.settings_test
def test_settings_database_password() -> None:
    config = ConfigFile(database_password='password')
    assert config.database_password == 'password'


@pytest.mark.settings_test
def test_settings_schema_file() -> None:
    config = ConfigFile()
    assert config.schema_file is None


@pytest.mark.settings_test
def test_settings_config() -> None:
    config = ConfigFile()
    assert config.config == '.pyway.conf'


@pytest.mark.settings_test
def test_settings_version() -> None:
    config = ConfigFile()
    assert config.version is False


@pytest.mark.settings_test
def test_settings_cmd() -> None:
    config = ConfigFile()
    assert config.cmd is None


@pytest.mark.settings_test
def test_parse_config_file() -> None:
    config = ConfigFile()
    config.config = 'tests/data/pyway.conf'
    config = Settings.parse_config_file(config)
    assert config.database_username == "unittest"


@pytest.mark.settings_test
def test_parse_args() -> None:

    # Setup mock config and args
    config = MockConfig()
    args = MockArgs()

    # Set attributes on args for testing
    for arg in ARGS:
        setattr(args, arg, f"test_{arg}")

    # Call your function
    Settings.parse_args(config, args)

    # Assert that config is updated correctly
    for arg in ARGS:
        assert getattr(config, arg) == f"test_{arg}"


@pytest.mark.settings_test
def test_parse_arguments() -> None:
    class MockConfig:
        pass

    # Create a mock config object
    config = MockConfig()

    test_args = [
        'script_name',
        '--database-migration-dir', 'migrations',
        '--database-table', 'pyway_meta',
        '--database-type', 'postgres',
        '--database-host', 'localhost'
    ]

    _ = sys.argv
    sys.argv = test_args

    Settings.parse_arguments(config)

    assert config.database_migration_dir == 'migrations'
    assert config.database_table == 'pyway_meta'
    assert config.database_type == 'postgres'
    assert config.database_host == 'localhost'


@pytest.mark.settings_test
def test_env_var_interpolation() -> None:
    # Set an env var
    os.environ['TEST_VAR'] = 'sometest'

    config = ConfigFile()
    config.config = 'tests/data/pyway_variable.conf'
    config = Settings.parse_config_file(config)
    assert config.database_username == "unittest_sometest"
