import pytest
import os
from strip_ansi import strip_ansi
from pyway.migrate import Migrate
from pyway.settings import ConfigFile

from oracle_integration_test import Oracle, skip_if_oracle_unavailable

MIGRATE_OUTPUT = """Migrating --> V01_01__test1.sql
V01_01__test1.sql SUCCESS
Migrating --> V01_02__test2.sql
V01_02__test2.sql SUCCESS
Migrating --> V01_03__test3.sql
V01_03__test3.sql SUCCESS
"""


MIGRATE_OUTPUT_NOTHING = """Nothing to do
"""


@pytest.fixture
def oracle_connect(autouse: bool = True) -> Oracle:
    oracle = Oracle()
    return oracle.run()


@pytest.mark.migrate_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_migrate(oracle_connect: Oracle) -> None:
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

    output = Migrate(config).run()
    assert strip_ansi(output) == MIGRATE_OUTPUT


@pytest.mark.migrate_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_migrate_nothingtodo(oracle_connect: Oracle) -> None:
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

    # Run migration twice - second time should do nothing
    _ = Migrate(config).run()
    output = Migrate(config).run()
    assert strip_ansi(output) == MIGRATE_OUTPUT_NOTHING


@pytest.mark.migrate_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_migrate_wallet_authentication(oracle_connect: Oracle) -> None:
    """Test Oracle Wallet authentication."""
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

    output = Migrate(config).run()
    assert strip_ansi(output) == MIGRATE_OUTPUT


@pytest.mark.migrate_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_migrate_tns_names(oracle_connect: Oracle) -> None:
    """Test TNS Names connection."""
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_name = oracle_connect.database_name  # Use as TNS alias
    config.database_username = oracle_connect.username
    config.database_password = oracle_connect.password
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-oracle')
    
    if oracle_connect.oracle_client_lib_dir:
        config.oracle_client_lib_dir = oracle_connect.oracle_client_lib_dir

    output = Migrate(config).run()
    assert strip_ansi(output) == MIGRATE_OUTPUT


@pytest.mark.migrate_test
@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_pyway_migrate_full_dsn(oracle_connect: Oracle) -> None:
    """Test full DSN connection string."""
    config = ConfigFile()
    config.database_type = "oracle"
    # Create full DSN string
    config.database_name = f"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={oracle_connect.host})(PORT={oracle_connect.port}))(CONNECT_DATA=(SERVICE_NAME={oracle_connect.database_name})))"
    config.database_username = oracle_connect.username
    config.database_password = oracle_connect.password
    config.database_table = 'pyway_schema_history'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema-oracle')
    
    if oracle_connect.oracle_client_lib_dir:
        config.oracle_client_lib_dir = oracle_connect.oracle_client_lib_dir

    output = Migrate(config).run()
    assert strip_ansi(output) == MIGRATE_OUTPUT
