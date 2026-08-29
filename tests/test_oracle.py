#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import pytest
import os

from pyway.dbms.database import factory
from pyway.dbms import oracle
from pyway.settings import ConfigFile
from oracle_integration_test import Oracle, skip_if_oracle_unavailable


@pytest.mark.oracle_test
def test_oracle_factory() -> None:
    """Test that the Oracle database adapter can be loaded by the factory."""
    cls = factory('oracle')
    assert cls is not None
    assert cls == oracle.Oracle


@pytest.mark.oracle_test
def test_oracle_config_creation() -> None:
    """Test Oracle configuration creation."""
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_host = "testhost"
    config.database_port = 1521
    config.database_name = "TESTDB"
    config.database_username = "testuser"
    config.database_password = "testpass"
    config.database_table = "pyway_schema_history"
    
    assert config.database_type == "oracle"
    assert config.database_host == "testhost"
    assert config.database_port == 1521
    assert config.database_name == "TESTDB"


@pytest.mark.oracle_test
def test_oracle_wallet_config() -> None:
    """Test Oracle Wallet configuration."""
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_name = "TEST_WALLET_DB"
    config.database_table = "pyway_schema_history"
    config.oracle_use_wallet = True
    config.oracle_wallet_location = "/path/to/test/wallet"
    config.oracle_client_lib_dir = "/path/to/test/instantclient"
    
    assert config.oracle_use_wallet == True
    assert config.oracle_wallet_location == "/path/to/test/wallet"
    assert config.oracle_client_lib_dir == "/path/to/test/instantclient"


@pytest.mark.oracle_test
def test_oracle_dsn_config() -> None:
    """Test Oracle DSN configuration."""
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_name = "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=testserver.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=testdb)))"
    config.database_username = "testuser"
    config.database_password = "testpass"
    config.database_table = "pyway_schema_history"
    
    assert "DESCRIPTION" in config.database_name
    assert "PROTOCOL=TCP" in config.database_name


@pytest.mark.oracle_test
@skip_if_oracle_unavailable()
def test_oracle_connection_basic() -> None:
    """Test basic Oracle connection."""
    oracle_instance = Oracle()
    oracle_connect = oracle_instance.run()
    
    config = ConfigFile()
    config.database_type = "oracle"
    config.database_host = oracle_connect.host
    config.database_username = oracle_connect.username
    config.database_password = oracle_connect.password
    config.database_port = oracle_connect.port
    config.database_name = oracle_connect.database_name
    config.database_table = "pyway_schema_history"
    
    # This should not raise an exception
    oracle_db = oracle.Oracle(config)
    assert oracle_db is not None
    assert oracle_db.version_table == "pyway_schema_history"

