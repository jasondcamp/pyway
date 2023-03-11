import pytest
from pyway.settings import ConfigFile
from pyway.settings import Settings


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
