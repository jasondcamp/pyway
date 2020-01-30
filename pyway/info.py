from tabulate import tabulate

from .helpers import Utils
from .log import logger, bcolors
from .migration import Migration
from .dbms.database import factory
from .errors import MIGRATIONS_NOT_FOUND


class Info():

    def __init__(self, conf):
        self._database_connection = "%s:%s/%s" % (conf.DATABASE_URL, conf.DATABASE_PORT, conf.DATABASE_NAME)
        self._migration_dir = conf.DATABASE_MIGRATION_DIR
        self._db = factory(conf.DBMS)(conf)
        self.headers = ["version", "extension", "name", "checksum"]
        self.tablefmt = "fancy_grid"

    def run(self):
        logger.success("\nDATABASE CONNECTION: %s\n" % self._database_connection)
        logger.info(tabulate(self.get_table_info(), headers="keys", tablefmt=self.tablefmt))

    def get_table_info(self):
        db_migrations = self._db.get_all_schema_migrations()
        local_migrations = self.get_new_local_migrations(db_migrations)
        if db_migrations and not local_migrations:
            logger.error(MIGRATIONS_NOT_FOUND % self._migration_dir)
        return db_migrations + local_migrations

    def get_new_local_migrations(self, db_migrations):
        local_files = Utils.get_local_files()
        if not local_files:
            return []
        new_local_migrations = [self.structure_migration(local_file) for local_file in local_files
                                if local_file not in [db_migration.name for db_migration in db_migrations]]
        return Utils.sort_migrations_list(new_local_migrations)

    def structure_migration(self, name):
        checksum = "%snew%s" % (bcolors.OKGREEN, bcolors.OKBLUE)
        return Migration.from_name(name, checksum=checksum).__dict__
