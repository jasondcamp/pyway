import pytest
import os
from pyway.helpers import Utils

@pytest.fixture
def mysqld_connect(autouse=True):
    return Mysqld()


@pytest.fixture
def version_mariadb():
    return "mysqld  Ver 10.5.16-MariaDB for Linux on x86_64 (MariaDB Server)"


@pytest.fixture
def version_mysql():
    return "/usr/sbin/mysqld  Ver 8.0.32-0ubuntu0.20.04.2 for Linux on x86_64 ((Ubuntu))"


@pytest.mark.helpers_test
def test_get_local_files():
    files = Utils.get_local_files(os.path.join('tests', 'data'))

    assert len(files) == 3

