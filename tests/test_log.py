import pytest
from pyway.log import logger
from pyway.exceptions import InvalidLogLevel


@pytest.mark.log_test
def test_log_levelset_noexception() -> None:
    logger.setlevel('INFO')
    assert True


@pytest.mark.log_test
def test_log_levelset_info_noexception() -> None:
    logger.setlevel('INFO')
    assert True


@pytest.mark.log_test
def test_log_levelset_debug_noexception() -> None:
    logger.setlevel('DEBUG')
    assert True


@pytest.mark.log_test
def test_log_levelset_error_noexception() -> None:
    logger.setlevel('ERROR')
    assert True


@pytest.mark.log_test
def test_log_levelset_warn_noexception() -> None:
    logger.setlevel('WARN')
    assert True


@pytest.mark.log_test
def test_log_levelset_fail() -> None:
    with pytest.raises(InvalidLogLevel):
        logger.setlevel('FAKE')
    assert True


@pytest.mark.log_test
def test_log_debug_noexception() -> None:
    logger.debug("test")
    assert True


@pytest.mark.log_test
def test_log_info_noexception() -> None:
    logger.info("test")
    assert True


@pytest.mark.log_test
def test_log_error_noexception() -> None:
    logger.error("test")
    assert True


@pytest.mark.log_test
def test_log_success_noexception() -> None:
    logger.success("test")
    assert True
