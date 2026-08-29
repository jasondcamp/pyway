import pytest
import os
from pyway.import_ import Import
from pyway.settings import ConfigFile

from oracle_integration_test import Oracle, skip_if_oracle_unavailable

INFO_OUTPUT = """+-----------+-------------+-------------------+------------+-------------------+
|   version | extension   | name              | checksum   | apply_timestamp   |
|-----------+-------------+-------------------+------------+-------------------|
|      1.01 | SQL         | V01_01__test1.sql | new        | new               |
|      1.02 | SQL         | V01_02__test2.sql | new        | new               |
|      1.03 | SQL         | V01_03__test3.sql | new        | new               |
+-----------+-------------+-------------------+------------+-------------------+"""

VALIDATE_OUTPUT = """Validating --> V01_01__test1.sql
V01_01__test1.sql VALID
"""


@pytest.fixture
def oracle_connect(autouse: bool = True) -> Oracle:
    oracle = Oracle()
    return oracle.run()


@pytest.mark.import_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_table_import(oracle_connect: Oracle) -> None:
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
        
    output = Import(config).run()
    assert output == "V01_01__test1.sql"


@pytest.mark.import_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_table_import_fullfilepath(oracle_connect: Oracle) -> None:
    """ Schema file is specified with path """
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_host = oracle_connect.host
    config.database_username = oracle_connect.username
    config.database_password = oracle_connect.password
    config.database_port = oracle_connect.port
    config.database_name = oracle_connect.database_name
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-oracle')
    config.schema_file = f"{config.database_migration_dir}/V01_01__test1.sql"
    
    # Configure Oracle-specific settings if available
    if oracle_connect.oracle_client_lib_dir:
        config.oracle_client_lib_dir = oracle_connect.oracle_client_lib_dir
    if oracle_connect.oracle_wallet_location:
        config.oracle_wallet_location = oracle_connect.oracle_wallet_location
    if oracle_connect.oracle_use_wallet:
        config.oracle_use_wallet = oracle_connect.oracle_use_wallet
        
    output = Import(config).run()
    assert output == "V01_01__test1.sql"


@pytest.mark.import_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_table_import_fileinvalid(oracle_connect: Oracle) -> None:
    """ Schema file doesn't exist """
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_host = oracle_connect.host
    config.database_username = oracle_connect.username
    config.database_password = oracle_connect.password
    config.database_port = oracle_connect.port
    config.database_name = oracle_connect.database_name
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-oracle')
    config.schema_file = "V01_99__nonexistent.sql"
    
    # Configure Oracle-specific settings if available
    if oracle_connect.oracle_client_lib_dir:
        config.oracle_client_lib_dir = oracle_connect.oracle_client_lib_dir
    if oracle_connect.oracle_wallet_location:
        config.oracle_wallet_location = oracle_connect.oracle_wallet_location
    if oracle_connect.oracle_use_wallet:
        config.oracle_use_wallet = oracle_connect.oracle_use_wallet

    with pytest.raises(RuntimeError):
        Import(config).run()


@pytest.mark.import_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_table_import_wallet_authentication(oracle_connect: Oracle) -> None:
    """ Test import with Oracle Wallet authentication """
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
        
    output = Import(config).run()
    assert output == "V01_01__test1.sql"


@pytest.mark.import_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_table_import_tns_names(oracle_connect: Oracle) -> None:
    """ Test import with TNS Names """
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_name = oracle_connect.database_name  # Use as TNS alias
    config.database_username = oracle_connect.username
    config.database_password = oracle_connect.password
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-oracle')
    config.schema_file = "V01_01__test1.sql"
    
    if oracle_connect.oracle_client_lib_dir:
        config.oracle_client_lib_dir = oracle_connect.oracle_client_lib_dir
        
    output = Import(config).run()
    assert output == "V01_01__test1.sql"

