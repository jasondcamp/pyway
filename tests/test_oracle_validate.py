import pytest
import os
from strip_ansi import strip_ansi
from pyway.validate import Validate
from pyway.import_ import Import
from pyway.settings import ConfigFile

from oracle_integration_test import Oracle, skip_if_oracle_unavailable

VALIDATE_OUTPUT = """Validating --> V01_01__test1.sql
V01_01__test1.sql VALID
"""


@pytest.fixture
def oracle_connect(autouse: bool = True) -> Oracle:
    oracle = Oracle()
    return oracle.run()


@pytest.mark.validate_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_table_validate(oracle_connect: Oracle) -> None:
    """ Import a file and validate that it matches """
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_host = oracle_connect.host
    config.database_username = oracle_connect.username
    config.database_password = oracle_connect.password
    config.database_port = oracle_connect.port
    config.database_name = oracle_connect.database_name
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-oracle')
    config.schema_file = "V01_01__test1.sql"
    
    # Configure Oracle-specific settings if available
    if oracle_connect.oracle_client_lib_dir:
        config.oracle_client_lib_dir = oracle_connect.oracle_client_lib_dir
    if oracle_connect.oracle_wallet_location:
        config.oracle_wallet_location = oracle_connect.oracle_wallet_location
    if oracle_connect.oracle_use_wallet:
        config.oracle_use_wallet = oracle_connect.oracle_use_wallet

    # Import file
    output = Import(config).run()
    output = Validate(config).run()
    assert strip_ansi(output) == VALIDATE_OUTPUT


@pytest.mark.validate_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_table_validate_noschemasfound(oracle_connect: Oracle) -> None:
    """ Test to see what happens when we try to validate and no files are found """
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

    with pytest.raises(RuntimeError, match="No migrations found"):
        Validate(config).run()


@pytest.mark.validate_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_table_validate_noschemasfound_skiperror(oracle_connect: Oracle) -> None:
    """ Test to see what happens when we try to validate and no files are found, skip initial check """
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

    output = Validate(config).run(skip_initial_check=True)
    assert "Nothing to do" in output


@pytest.mark.validate_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_table_validate_diffchecksum(oracle_connect: Oracle) -> None:
    """ Test validation when checksum differs """
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_host = oracle_connect.host
    config.database_username = oracle_connect.username
    config.database_password = oracle_connect.password
    config.database_port = oracle_connect.port
    config.database_name = oracle_connect.database_name
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema_validate_diffchecksum')
    
    # Configure Oracle-specific settings if available
    if oracle_connect.oracle_client_lib_dir:
        config.oracle_client_lib_dir = oracle_connect.oracle_client_lib_dir
    if oracle_connect.oracle_wallet_location:
        config.oracle_wallet_location = oracle_connect.oracle_wallet_location
    if oracle_connect.oracle_use_wallet:
        config.oracle_use_wallet = oracle_connect.oracle_use_wallet

    # This should raise an error due to checksum mismatch
    with pytest.raises(RuntimeError):
        Validate(config).run()


@pytest.mark.validate_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_table_validate_wallet_authentication(oracle_connect: Oracle) -> None:
    """ Test validation with Oracle Wallet authentication """
    if not oracle_connect.oracle_wallet_location:
        pytest.skip("Oracle Wallet not configured for testing")
        
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_name = oracle_connect.database_name
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-oracle')
    config.schema_file = "V01_01__test1.sql"
    config.oracle_use_wallet = True
    config.oracle_wallet_location = oracle_connect.oracle_wallet_location
    
    if oracle_connect.oracle_client_lib_dir:
        config.oracle_client_lib_dir = oracle_connect.oracle_client_lib_dir

    # Import file
    output = Import(config).run()
    output = Validate(config).run()
    assert strip_ansi(output) == VALIDATE_OUTPUT
