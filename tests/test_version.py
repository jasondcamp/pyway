import pytest
from pyway.version import __version__


@pytest.mark.version_test
def test_version_isnotnone() -> None:
    assert __version__ is not None


@pytest.mark.version_test
def test_version_semver() -> None:
    assert len(__version__.split('.')) == 3
