#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Oracle integration test helper.
This module provides Oracle database connection configuration for testing PyWay Oracle functionality.

Note: Unlike MySQL and PostgreSQL which have dedicated integration test packages
that start temporary database instances, Oracle requires an existing database
instance to be available for testing. This helper provides connection configuration
following the same interface pattern as other database integration tests.
"""

import os
from typing import Optional


class Oracle:
    """Oracle database connection helper for testing."""
    
    def __init__(self, 
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 database_name: Optional[str] = None,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 oracle_client_lib_dir: Optional[str] = None,
                 oracle_wallet_location: Optional[str] = None,
                 oracle_use_wallet: bool = False):
        """
        Initialize Oracle test connection.
        
        Parameters can be overridden via environment variables:
        - ORACLE_TEST_HOST
        - ORACLE_TEST_PORT  
        - ORACLE_TEST_DATABASE
        - ORACLE_TEST_USERNAME
        - ORACLE_TEST_PASSWORD
        - ORACLE_TEST_CLIENT_LIB_DIR
        - ORACLE_TEST_WALLET_LOCATION
        - ORACLE_TEST_USE_WALLET
        """
        # Default values for testing
        self.host = host or os.getenv('ORACLE_TEST_HOST', 'testhost')
        self.port = port or int(os.getenv('ORACLE_TEST_PORT', '1521'))
        self.database_name = database_name or os.getenv('ORACLE_TEST_DATABASE', 'TESTDB')
        self.username = username or os.getenv('ORACLE_TEST_USERNAME', 'testuser')
        self.password = password or os.getenv('ORACLE_TEST_PASSWORD', 'testpass')
        self.oracle_client_lib_dir = oracle_client_lib_dir or os.getenv('ORACLE_TEST_CLIENT_LIB_DIR')
        self.oracle_wallet_location = oracle_wallet_location or os.getenv('ORACLE_TEST_WALLET_LOCATION')
        self.oracle_use_wallet = oracle_use_wallet or os.getenv('ORACLE_TEST_USE_WALLET', '').lower() == 'true'
        
    def run(self) -> 'Oracle':
        """Start/configure Oracle connection (returns self for compatibility with other helpers)."""
        return self
        
    def stop(self) -> None:
        """Stop Oracle connection (placeholder for compatibility)."""
        pass
        
    def is_available(self) -> bool:
        """Check if Oracle connection is available for testing."""
        try:
            import oracledb
            # Try a simple connection test
            if self.oracle_use_wallet:
                # Test wallet connection
                conn = oracledb.connect(dsn=self.database_name)
            else:
                # Test regular connection
                dsn = f"{self.host}:{self.port}/{self.database_name}"
                conn = oracledb.connect(user=self.username, password=self.password, dsn=dsn)
            conn.close()
            return True
        except Exception:
            return False


def create_test_oracle() -> Oracle:
    """Create a test Oracle instance with default configuration."""
    return Oracle()


def skip_if_oracle_unavailable():
    """Pytest skip decorator for Oracle tests when Oracle is not available."""
    import pytest
    oracle = create_test_oracle()
    return pytest.mark.skipif(
        not oracle.is_available(),
        reason="Oracle Database not available for testing"
    )
