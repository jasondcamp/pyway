import os
from typing import Tuple

from pyway.helpers import Utils
from pyway.migration import Migration
from pyway.dbms.database import factory
from pyway.configfile import ConfigFile


class Checksum():
    def __init__(self, args: ConfigFile) -> None:
        self._db = factory(args.database_type)(args)
        self.migration_dir = args.database_migration_dir
        self.checksum_file = args.checksum_file
        self.args = args

    def run(self) -> Tuple[str, str]:
        if not self.checksum_file:
            raise AttributeError("Error, must specify --checksum-file with checksum")

        # If a path is specified, strip that off - all files should
        # be in the migration_dir directory
        if os.path.isabs(self.checksum_file) or os.sep in self.checksum_file:
            self.checksum_file = os.path.basename(self.checksum_file)

        if not os.path.exists(os.path.join(os.getcwd(), self.migration_dir, self.checksum_file)):
            raise FileNotFoundError(f"Error, schema file '{self.migration_dir}/{self.checksum_file}' does not exist!")

        # Generate new checksum
        version: str = Utils.get_version_from_name(self.checksum_file)
        migration: Migration = self._db.get_schema_migration(version)
        migration.checksum = Utils.load_checksum_from_name(self.checksum_file, self.migration_dir)

        self._db.update_checksum(migration)

        return self.checksum_file, migration.checksum
