from .log import logger
from .helpers import Utils
from .validate import Validate
from .migration import Migration
from .dbms.database import factory


class Migrate():

    def __init__(self, conf):
        Validate(conf).run()
        self._db = factory(conf.DBMS)(conf)

    def run(self):
        migrations_to_be_executed = self._get_migration_files_to_be_executed()
        if migrations_to_be_executed is None or len(migrations_to_be_executed) == 0:
            logger.info("Nothing to do")
            return

        for migration in migrations_to_be_executed:
            logger.info("Migrating --> %s" % migration.name)
            try:
                with open(Utils.fullname(migration.name), "r") as sqlfile:
                    self._db.execute(sqlfile.read())
                self._db.upgrade_version(migration)
                logger.success("%s SUCCESS" % migration.name)
            except Exception as error:
                logger.error(error)

    def _get_migration_files_to_be_executed(self):
        all_local_migrations = self._get_all_local_migrations()
        all_db_migrations = Migration.from_list(self._db.get_all_schema_migrations())
        return Utils.subtract(all_local_migrations, all_db_migrations)

    def _get_all_local_migrations(self):
        local_files = Utils.get_local_files()
        migrations = [Migration.from_name(local_file) for local_file in local_files]
        return Utils.sort_migrations_list(migrations)
