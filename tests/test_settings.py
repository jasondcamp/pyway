import pytest
import sys
from pyway.settings import ConfigFile
from pyway.settings import Settings
from pyway.settings import ARGS

class MockConfig:
    pass

class MockArgs:
    pass

# Make sure config options exists and check some defaults
@pytest.mark.settings_test
def test_settings_database_migration_dir():
    config = ConfigFile()
    assert config.database_migration_dir == 'resources'


@pytest.mark.settings_test
def test_settings_database_table():
    config = ConfigFile()
    assert config.database_table == 'public.pyway'


@pytest.mark.settings_test
def test_settings_database_type():
    config = ConfigFile()
    assert config.database_type == 'postgres'


@pytest.mark.settings_test
def test_settings_database_host():
    config = ConfigFile()
    assert config.database_host == 'localhost'


@pytest.mark.settings_test
def test_settings_database_port():
    config = ConfigFile()
    assert config.database_port == '5432'


@pytest.mark.settings_test
def test_settings_database_name():
    config = ConfigFile()
    assert config.database_name == 'postgres'


@pytest.mark.settings_test
def test_settings_database_username():
    config = ConfigFile()
    assert config.database_username == 'postgres'


@pytest.mark.settings_test
def test_settings_database_password():
    config = ConfigFile()
    assert config.database_password == 'password'


@pytest.mark.settings_test
def test_settings_schema_file():
    config = ConfigFile()
    assert config.schema_file is None


@pytest.mark.settings_test
def test_settings_config():
    config = ConfigFile()
    assert config.config == '.pyway.conf'


@pytest.mark.settings_test
def test_settings_version():
    config = ConfigFile()
    assert config.version is False


@pytest.mark.settings_test
def test_settings_cmd():
    config = ConfigFile()
    assert config.cmd is None


@pytest.mark.settings_test
def test_parse_config_file():
    config = ConfigFile()
    config.config = 'tests/data/pyway.conf'
    config = Settings.parse_config_file(config)
    assert config.database_username == "unittest"


@pytest.mark.settings_test
def test_parse_args():

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
def test_parse_arguments():
    class MockConfig:
        pass

    # Create a mock config object
    config = MockConfig()

#    config = ConfigFile()
#    (config, parser) = Settings.parse_arguments(config)

    test_args = [
        'script_name',
        '--database-migration-dir', 'migrations',
        '--database-table', 'pyway_meta',
        '--database-type', 'postgres',
        '--database-host', 'localhost'
    ]

    original_argv = sys.argv
    sys.argv = test_args


    Settings.parse_arguments(config)

    assert config.database_migration_dir == 'migrations'
    assert config.database_table == 'pyway_meta'
    assert config.database_type == 'postgres'
    assert config.database_host == 'localhost'
