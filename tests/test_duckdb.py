#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import pytest

from pyway.configfile import ConfigFile
from pyway.dbms.database import factory
from pyway.dbms import duckdb
from pyway.migration import Migration


@pytest.mark.duckdb_test
def test_factory() -> None:
    args = ConfigFile()
    args.database_type = "duckdb"
    args.database_name = "./unittest.duckdb"
    args.database_table = "pyway"
    db: duckdb.Duckdb = factory(args.database_type)(args)

    assert db.connect().sql(
        f"select 1 from information_schema.tables where table_name = '{args.database_table}'"
    ).fetchone() is not None

    db.disconnect()


@pytest.mark.duckdb_test
def test_migrations() -> None:
    args = ConfigFile()
    args.database_type = "duckdb"
    args.database_name = "./unittest.duckdb"
    args.database_table = "pyway"
    db: duckdb.Duckdb = factory(args.database_type)(args)

    db.execute(f"truncate table {args.database_table}")

    migrations = db.get_all_schema_migrations()
    assert migrations == []

    mig = Migration(
        version="01.01", extension="SQL",
        name="V01_01__test1.sql",
        checksum="8327AD7B",
        apply_timestamp="new"
    )

    db.upgrade_version(mig)

    migrations = db.get_all_schema_migrations()
    assert len(migrations) == 1
    assert migrations[0].checksum == mig.checksum

    updated = Migration(
        version="01.01", extension="SQL",
        name="V01_01__test1.sql",
        checksum="FACB0AE4",
        apply_timestamp="new"
    )

    db.update_checksum(updated)
    migrations = db.get_all_schema_migrations()
    assert len(migrations) == 1
    assert migrations[0].checksum == updated.checksum

    fetched = db.get_schema_migration(updated.version)
    assert fetched.version == updated.version
    assert fetched.name == updated.name
    assert fetched.checksum == updated.checksum
    assert fetched.extension == updated.extension

    db.disconnect()
