import os
import sys

from pyway.log import logger
from pyway.migration import Migration
from pyway.dbms.database import factory
from pyway.helpers import Utils
from pyway.errors import VALID_NAME_ERROR


class Import():

    def __init__(self, args):
        self._db = factory(args.database_type)(args)
        self.migration_dir = args.database_migration_dir
        self.schema_file = args.schema_file
        self.args = args

    def run(self):
        if not self.schema_file:
            logger.error("Error, must specify --schema-file with import")
            sys.exit(1)

        if not os.path.exists(os.path.join(os.getcwd(), self.migration_dir, self.schema_file)):
            logger.error(f"Error, schema file '{self.migration_dir}/{self.schema_file}' does not exist!")
            sys.exit(1)

        if not Utils.is_file_name_valid(self.schema_file):
            logger.error(VALID_NAME_ERROR % (self.schema_file, Utils.expected_pattern()))
            sys.exit(1)

        # File exists, import it
        migration = Migration.from_name(self.schema_file, self.migration_dir)
        self._db.upgrade_version(migration)
        logger.info(f"{migration.name} Imported")
