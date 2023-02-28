import os
import sys
from tabulate import tabulate

from .helpers import Utils
from .log import logger, bcolors
from .migration import Migration
from .dbms.database import factory
from .errors import MIGRATIONS_NOT_FOUND


class Import():

    def __init__(self, conf):
        self._migration_dir = conf.args.database_migration_dir
        self._db = factory(conf.args.database_type)(conf)
        self.schema_file = conf.args.schema_file

    def run(self):
        if not self.schema_file:
           logger.error("Error, must specify --schema-file with import")
           sys.exit(1)

        if not os.path.exists("/".join([self._migration_dir, self.schema_file])):
           logger.error(f"Error, schema file '{self._migration_dir}/{self.schema_file}' does not exist!")
           sys.exit(1)

        # File exists, import it
        migration = Migration.from_name(self.schema_file)
        self._db.upgrade_version(migration)
        logger.info(f"{migration.name} Imported") 
