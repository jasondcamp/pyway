import pytest
import os
from strip_ansi import strip_ansi
from pyway.info import Info
from pyway.settings import ConfigFile

from oracle_integration_test import Oracle, skip_if_oracle_unavailable

INFO_OUTPUT = """+-----------+-------------+-------------------+------------+-------------------+
|   version | extension   | name              | checksum   | apply_timestamp   |
|-----------+-------------+-------------------+------------+-------------------|
|      1.01 | SQL         | V01_01__test1.sql | new        | new               |
|      1.02 | SQL         | V01_02__test2.sql | new        | new               |
|      1.03 | SQL         | V01_03__test3.sql | new        | new               |
+-----------+-------------+-------------------+------------+-------------------+"""


@pytest.fixture
def oracle_connect(autouse=True) -> Oracle:
    oracle = Oracle()
    return oracle.run()


@pytest.mark.info_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_info(oracle_connect: Oracle) -> None:
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_host = oracle_connect.host
    config.database_username = oracle_connect.username
    config.database_password = oracle_connect.password
    config.database_port = oracle_connect.port
    config.database_name = oracle_connect.database_name
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-oracle')
    
    # Configure Oracle-specific settings if available
    if oracle_connect.oracle_client_lib_dir:
        config.oracle_client_lib_dir = oracle_connect.oracle_client_lib_dir
    if oracle_connect.oracle_wallet_location:
        config.oracle_wallet_location = oracle_connect.oracle_wallet_location
    if oracle_connect.oracle_use_wallet:
        config.oracle_use_wallet = oracle_connect.oracle_use_wallet
        
    tbl = Info(config).run()
    assert strip_ansi(tbl) == INFO_OUTPUT


@pytest.mark.info_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_info_nofiles(oracle_connect: Oracle) -> None:
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_host = oracle_connect.host
    config.database_username = oracle_connect.username
    config.database_password = oracle_connect.password
    config.database_port = oracle_connect.port
    config.database_name = oracle_connect.database_name
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'empty')
    
    # Configure Oracle-specific settings if available
    if oracle_connect.oracle_client_lib_dir:
        config.oracle_client_lib_dir = oracle_connect.oracle_client_lib_dir
    if oracle_connect.oracle_wallet_location:
        config.oracle_wallet_location = oracle_connect.oracle_wallet_location
    if oracle_connect.oracle_use_wallet:
        config.oracle_use_wallet = oracle_connect.oracle_use_wallet

    files = Info(config).get_new_local_migrations([], config.database_migration_dir)
    assert files == []


@pytest.mark.info_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_info_wallet_authentication(oracle_connect: Oracle) -> None:
    """Test Oracle Wallet authentication with info."""
    if not oracle_connect.oracle_wallet_location:
        pytest.skip("Oracle Wallet not configured for testing")
        
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_name = oracle_connect.database_name
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-oracle')
    config.oracle_use_wallet = True
    config.oracle_wallet_location = oracle_connect.oracle_wallet_location
    
    if oracle_connect.oracle_client_lib_dir:
        config.oracle_client_lib_dir = oracle_connect.oracle_client_lib_dir

    tbl = Info(config).run()
    assert strip_ansi(tbl) == INFO_OUTPUT
