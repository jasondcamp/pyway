import os
from tabulate import tabulate
from typing import List

from pyway.helpers import Utils
from pyway.log import bcolors
from pyway.migration import Migration
from pyway.dbms.database import factory
from pyway.configfile import ConfigFile
from pyway.errors import (MIGRATIONS_MISSING)


class Info():
    def __init__(self, config: ConfigFile) -> None:
        self.migration_dir = config.database_migration_dir
        self._db = factory(config.database_type)(config)
        self.headers = ["version", "extension", "name", "checksum", "apply_timestamp"]
        self.tablefmt = "psql"
        self.config = config

    def run(self) -> str:
        return tabulate(Utils.flatten_migrations(self.get_table_info()), headers="keys",
                        tablefmt=self.tablefmt, floatfmt=".2f")

    def get_table_info(self) -> List:
        # Get remote migrations (and validate that the files exist)
        db_migrations = self._db.get_all_schema_migrations()
        for m in db_migrations:
            if not os.path.exists(os.path.join(self.config.database_migration_dir, m.name)):
                raise RuntimeError(MIGRATIONS_MISSING % m.name)

        # Get any new local migrations
        local_migrations = self.get_new_local_migrations(db_migrations, self.migration_dir)

        return db_migrations + local_migrations

    def get_new_local_migrations(self, db_migrations: List, migration_dir: str) -> List:
        local_files = Utils.get_local_files(migration_dir)
        if not local_files:
            return []

        new_local_migrations = [self.structure_migration(local_file) for local_file in local_files
                                if local_file not in [db_migration.name for db_migration in db_migrations]]

        return Utils.sort_migrations_list(new_local_migrations)

    def structure_migration(self, name: str) -> Migration:
        checksum = "%snew%s" % (bcolors.OKGREEN, bcolors.OKBLUE)
        apply_timestamp = "%snew%s" % (bcolors.OKGREEN, bcolors.OKBLUE)
        return Migration.from_name(name, self.migration_dir, checksum=checksum, apply_timestamp=apply_timestamp)
