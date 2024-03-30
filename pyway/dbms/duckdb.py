#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import List

import duckdb

from pyway.migration import Migration
from pyway.configfile import ConfigFile

CREATE_VERSION_MIGRATIONS_SEQ = "create sequence if not exists migration_seq;"
CREATE_VERSION_MIGRATIONS = "create table if not exists %s ("\
    "installed_rank UBIGINT NOT NULL PRIMARY KEY DEFAULT nextval('migration_seq'),"\
    "version varchar(20) NOT NULL,"\
    "extension varchar(20) NOT NULL,"\
    "name varchar(125) NOT NULL,"\
    "checksum varchar(25) NOT NULL,"\
    "apply_timestamp timestamp DEFAULT NOW()"\
    ");"
SELECT_FIELDS = ("version", "extension", "name", "checksum", "apply_timestamp")
ORDER_BY_FIELD_ASC = "installed_rank"
ORDER_BY_FIELD_DESC = "installed_rank desc"
INSERT_VERSION_MIGRATE = "insert into %s (version, extension, name, checksum) values ('%s', '%s', '%s', '%s');"
UPDATE_CHECKSUM = "update %s set checksum='%s' where version='%s';"


class Duckdb():

    def __init__(self, args: ConfigFile) -> None:
        self.args = args
        self.version_table = args.database_table
        self._db = duckdb.connect(f"{self.args.database_name}")
        self.create_version_table_if_not_exists()

    def connect(self) -> duckdb.DuckDBPyConnection:
        return self._db.cursor()  # noqa: E501

    def disconnect(self) -> None:
        self._db.close()

    def create_version_table_if_not_exists(self) -> None:
        self.execute(CREATE_VERSION_MIGRATIONS_SEQ)
        self.execute(CREATE_VERSION_MIGRATIONS % self.version_table)

    def execute(self, script: str) -> None:
        cur = self.connect()
        cur.begin()
        cur.execute(script)
        cur.commit()

    def get_all_schema_migrations(self) -> List[Migration]:
        cursor = self.connect()
        cursor.execute(f"SELECT {','.join(SELECT_FIELDS)} FROM {self.version_table} ORDER BY {ORDER_BY_FIELD_ASC}")
        migrations = []
        for row in cursor.fetchall():
            migrations.append(Migration(row[0], row[1], row[2], row[3], row[4]))
        cursor.close()
        return migrations

    def get_schema_migration(self, version: str) -> Migration:
        cursor = self.connect()
        cursor.execute(f"SELECT {','.join(SELECT_FIELDS)} FROM {self.version_table} WHERE version=?", [version])
        row = cursor.fetchone()
        if row is not None:
            migration = Migration(row[0], row[1], row[2], row[3], row[4])
        cursor.close()
        return migration

    def upgrade_version(self, migration: Migration) -> None:
        self.execute(INSERT_VERSION_MIGRATE % (self.version_table, migration.version,
                                               migration.extension, migration.name,
                                               migration.checksum))

    def update_checksum(self, migration: Migration) -> None:
        self.execute(UPDATE_CHECKSUM % (self.version_table, migration.checksum, migration.version))
