from tabulate import tabulate

from .helpers import Utils
from .log import logger, bcolors
from .migration import Migration
from .dbms.database import factory
from .errors import MIGRATIONS_NOT_FOUND


class Info():

    def __init__(self, conf):
        self._database_connection = "%s:%s/%s" % (conf.args.database_host, conf.args.database_port, conf.args.database_name)
        self._migration_dir = conf.args.database_migration_dir
        self._db = factory(conf.args.database_type)(conf)
        self.headers = ["version", "extension", "name", "checksum", "apply_timestamp"]
        self.tablefmt = "psql"

    def run(self):
        logger.info(tabulate(Utils.flatten_migrations(self.get_table_info()), headers="keys", tablefmt=self.tablefmt))

    def get_table_info(self):
        db_migrations = self._db.get_all_schema_migrations()
        local_migrations = self.get_new_local_migrations(db_migrations)
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
        apply_timestamp = "%snew%s" % (bcolors.OKGREEN, bcolors.OKBLUE)
        return Migration.from_name(name, checksum=checksum, apply_timestamp=apply_timestamp)
