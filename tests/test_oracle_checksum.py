import pytest
import os
from pyway.checksum import Checksum
from pyway.migrate import Migrate
from pyway.settings import ConfigFile

from oracle_integration_test import Oracle, skip_if_oracle_unavailable


@pytest.fixture
def oracle_connect(autouse: bool = True) -> Oracle:
    oracle = Oracle()
    return oracle.run()


@pytest.mark.checksum_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_table_checksum(oracle_connect: Oracle) -> None:
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_host = oracle_connect.host
    config.database_username = oracle_connect.username
    config.database_password = oracle_connect.password
    config.database_port = oracle_connect.port
    config.database_name = oracle_connect.database_name
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-oracle')
    config.checksum_file = "V01_01__test1.sql"
    
    # Configure Oracle-specific settings if available
    if oracle_connect.oracle_client_lib_dir:
        config.oracle_client_lib_dir = oracle_connect.oracle_client_lib_dir
    if oracle_connect.oracle_wallet_location:
        config.oracle_wallet_location = oracle_connect.oracle_wallet_location
    if oracle_connect.oracle_use_wallet:
        config.oracle_use_wallet = oracle_connect.oracle_use_wallet

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    name, checksum = Checksum(config).run()
    assert name == "V01_01__test1.sql"
    # Oracle SQL will have different checksum than PostgreSQL
    assert checksum is not None
    assert len(checksum) == 8  # Should be 8-character hex string


@pytest.mark.checksum_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_table_checksum_fileinvalid(oracle_connect: Oracle) -> None:
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_host = oracle_connect.host
    config.database_username = oracle_connect.username
    config.database_password = oracle_connect.password
    config.database_port = oracle_connect.port
    config.database_name = oracle_connect.database_name
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-oracle')
    config.checksum_file = "V01_99__nonexistent.sql"
    
    # Configure Oracle-specific settings if available
    if oracle_connect.oracle_client_lib_dir:
        config.oracle_client_lib_dir = oracle_connect.oracle_client_lib_dir
    if oracle_connect.oracle_wallet_location:
        config.oracle_wallet_location = oracle_connect.oracle_wallet_location
    if oracle_connect.oracle_use_wallet:
        config.oracle_use_wallet = oracle_connect.oracle_use_wallet

    with pytest.raises(RuntimeError):
        Checksum(config).run()


@pytest.mark.checksum_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_table_checksum_fullpath(oracle_connect: Oracle) -> None:
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_host = oracle_connect.host
    config.database_username = oracle_connect.username
    config.database_password = oracle_connect.password
    config.database_port = oracle_connect.port
    config.database_name = oracle_connect.database_name
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-oracle')
    config.checksum_file = f"{config.database_migration_dir}/V01_01__test1.sql"
    
    # Configure Oracle-specific settings if available
    if oracle_connect.oracle_client_lib_dir:
        config.oracle_client_lib_dir = oracle_connect.oracle_client_lib_dir
    if oracle_connect.oracle_wallet_location:
        config.oracle_wallet_location = oracle_connect.oracle_wallet_location
    if oracle_connect.oracle_use_wallet:
        config.oracle_use_wallet = oracle_connect.oracle_use_wallet

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    name, checksum = Checksum(config).run()
    assert name == "V01_01__test1.sql"
    assert checksum is not None
    assert len(checksum) == 8


@pytest.mark.checksum_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_table_checksum_invalid_filename(oracle_connect: Oracle) -> None:
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_host = oracle_connect.host
    config.database_username = oracle_connect.username
    config.database_password = oracle_connect.password
    config.database_port = oracle_connect.port
    config.database_name = oracle_connect.database_name
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-oracle')
    config.checksum_file = "invalid_filename.sql"
    
    # Configure Oracle-specific settings if available
    if oracle_connect.oracle_client_lib_dir:
        config.oracle_client_lib_dir = oracle_connect.oracle_client_lib_dir
    if oracle_connect.oracle_wallet_location:
        config.oracle_wallet_location = oracle_connect.oracle_wallet_location
    if oracle_connect.oracle_use_wallet:
        config.oracle_use_wallet = oracle_connect.oracle_use_wallet

    with pytest.raises(RuntimeError):
        Checksum(config).run()


@pytest.mark.checksum_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_table_checksum_wallet_authentication(oracle_connect: Oracle) -> None:
    """ Test checksum with Oracle Wallet authentication """
    if not oracle_connect.oracle_wallet_location:
        pytest.skip("Oracle Wallet not configured for testing")
        
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_name = oracle_connect.database_name
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-oracle')
    config.checksum_file = "V01_01__test1.sql"
    config.oracle_use_wallet = True
    config.oracle_wallet_location = oracle_connect.oracle_wallet_location
    
    if oracle_connect.oracle_client_lib_dir:
        config.oracle_client_lib_dir = oracle_connect.oracle_client_lib_dir

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    name, checksum = Checksum(config).run()
    assert name == "V01_01__test1.sql"
    assert checksum is not None
    assert len(checksum) == 8


@pytest.mark.checksum_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_table_checksum_thin_mode(oracle_connect: Oracle) -> None:
    """ Test checksum using Oracle Thin mode (without client library) """
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_host = oracle_connect.host
    config.database_username = oracle_connect.username
    config.database_password = oracle_connect.password
    config.database_port = oracle_connect.port
    config.database_name = oracle_connect.database_name
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-oracle')
    config.checksum_file = "V01_01__test1.sql"
    # Explicitly don't set oracle_client_lib_dir to force Thin mode

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    name, checksum = Checksum(config).run()
    assert name == "V01_01__test1.sql"
    assert checksum is not None
    assert len(checksum) == 8

