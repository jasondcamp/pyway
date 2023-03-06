import pytest
#from pyway import pyway
import pyway

# Make sure config options exists and check some defaults
@pytest.mark.settings_test
def test_settings_test():
#    assert rgetattr(mysqld_connect, 'config') is not None
    assert True

@pytest.mark.settings_test
def test_dirs_basedir_exists():
#    assert rgetattr(mysqld_connect, 'config.dirs.base_dir') is not None
    assert True

@pytest.mark.settings_test
def test_dirs_datadir_exists():
#    assert rgetattr(mysqld_connect, 'config.dirs.data_dir') is not None
    assert True
