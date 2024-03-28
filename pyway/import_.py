import os

from pyway.migration import Migration
from pyway.dbms.database import factory
from pyway.helpers import Utils
from pyway.errors import VALID_NAME_ERROR
from pyway.configfile import ConfigFile


class Import():

    def __init__(self, args: ConfigFile) -> None:
        self._db = factory(args.database_type)(args)
        self.migration_dir = args.database_migration_dir
        self.schema_file = args.schema_file
        self.args = args

    def run(self) -> str:
        if not self.schema_file:
            raise AttributeError("Error, must specify --schema-file with import")

        # If a path is specified, strip that off - all files should
        # be in the migration_dir directory
        if os.path.isabs(self.schema_file) or os.sep in self.schema_file:
            self.schema_file = os.path.basename(self.schema_file)

        if not os.path.exists(os.path.join(os.getcwd(), self.migration_dir, self.schema_file)):
            raise FileNotFoundError(f"Error, schema file '{self.migration_dir}/{self.schema_file}' does not exist!")

        if not Utils.is_file_name_valid(self.schema_file):
            raise ValueError(VALID_NAME_ERROR % (self.schema_file, Utils.expected_pattern()))

        # File exists, import it
        migration = Migration.from_name(self.schema_file, self.migration_dir)
        self._db.upgrade_version(migration)
        return (migration.name)
