import os

from pyway.log import logger
from pyway.helpers import Utils
from pyway.migration import Migration
from pyway.dbms.database import factory
from pyway.errors import MIGRATIONS_NOT_FOUND

class Migrate():

    def __init__(self, args):
        self._db = factory(args.database_type)(args)
        self.migration_dir = args.database_migration_dir
        self.args = args

    def run(self):
        migrations_to_be_executed = self._get_migration_files_to_be_executed()
        if not migrations_to_be_executed:
            logger.info("Nothing to do")
            return

        for migration in migrations_to_be_executed:
            logger.info(f"Migrating --> {migration.name}")
            try:
                with open(os.path.join(os.getcwd(), self.migration_dir, migration.name), "r", encoding='utf-8') as sqlfile:
                    self._db.execute(sqlfile.read())
                self._db.upgrade_version(migration)
                logger.success(f"{migration.name} SUCCESS")
            except Exception as error:
                logger.error(error)

    def _get_migration_files_to_be_executed(self):
        all_local_migrations = self._get_all_local_migrations()
        all_db_migrations = Migration.from_list(self._db.get_all_schema_migrations())

        if all_db_migrations and not all_local_migrations:
            logger.error(MIGRATIONS_NOT_FOUND % self.migration_dir)
        return Utils.subtract(all_local_migrations, all_db_migrations)

    def _get_all_local_migrations(self):
        local_files = Utils.get_local_files(self.migration_dir)
        if not local_files:
            return []
        migrations = [Migration.from_name(local_file, self.migration_dir) for local_file in local_files]
        return Utils.sort_migrations_list(migrations)
