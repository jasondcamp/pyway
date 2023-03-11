import pytest
from pyway.log import logger
from pyway.exceptions import InvalidLogLevel


@pytest.mark.log_test
def test_log_levelset_noexception():
    logger.setlevel('INFO')
    assert True


@pytest.mark.log_test
def test_log_levelset_info_noexception():
    logger.setlevel('INFO')
    assert True


@pytest.mark.log_test
def test_log_levelset_debug_noexception():
    logger.setlevel('DEBUG')
    assert True


@pytest.mark.log_test
def test_log_levelset_error_noexception():
    logger.setlevel('ERROR')
    assert True


@pytest.mark.log_test
def test_log_levelset_warn_noexception():
    logger.setlevel('WARN')
    assert True


@pytest.mark.log_test
def test_log_levelset_fail():
    with pytest.raises(InvalidLogLevel):
        logger.setlevel('FAKE')
    assert True


@pytest.mark.log_test
def test_log_debug_noexception():
    logger.debug("test")
    assert True


@pytest.mark.log_test
def test_log_info_noexception():
    logger.info("test")
    assert True


@pytest.mark.log_test
def test_log_error_noexception():
    logger.error("test")
    assert True


@pytest.mark.log_test
def test_log_success_noexception():
    logger.success("test")
    assert True
