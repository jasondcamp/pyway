import sys

from pyway.log import logger
from pyway.helpers import Utils
from pyway.dbms.database import factory
from pyway.migration import Migration
from pyway.errors import OUT_OF_DATE_ERROR, DIFF_NAME_ERROR, DIFF_CHECKSUM_ERROR, VALID_NAME_ERROR, MIGRATIONS_NOT_FOUND, MIGRATIONS_NOT_STARTED

class Validate():
    def __init__(self, conf):
        self._db = factory(conf.args.database_type)(conf)
        self._migration_dir = conf.args.database_migration_dir

    def run(self):
        local_migrations = self._get_all_local_migrations()
        db_migrations = self._db.get_all_schema_migrations()

        if not db_migrations:
            logger.error(MIGRATIONS_NOT_STARTED)
            sys.exit(1)

        if db_migrations and not local_migrations:
            logger.error(MIGRATIONS_NOT_FOUND % self._migration_dir)

        if local_migrations:
            local_migrations_map = Utils.create_map_from_list("version", local_migrations)

            for db_migration in db_migrations:
                logger.info(f"Validating --> {db_migration.name}")
                local_migration = local_migrations_map.get(db_migration.version)

                if not self._out_of_date(local_migration):
                    logger.error(OUT_OF_DATE_ERROR % db_migration.name)
                elif not self._name_format(local_migration.name):
                    logger.error(VALID_NAME_ERROR % (local_migration.name, Utils.expected_pattern()))
                elif not self._diff_names(local_migration, db_migration):
                    logger.error(DIFF_NAME_ERROR % (local_migration.name, db_migration.name))
                elif not self._diff_checksum(local_migration, db_migration):
                    logger.error(DIFF_CHECKSUM_ERROR % (local_migration.name, local_migration.checksum, db_migration.checksum))
                else:
                    logger.success(f"{db_migration.name} VALID")

    def _out_of_date(self, local_migration):
        return bool(local_migration is not None)

    def _diff_names(self, local_migration, db_migration):
        return bool(local_migration.name == db_migration.name)

    def _diff_checksum(self, local_migration, db_migration):
        return bool(local_migration.checksum == db_migration.checksum)

    def _name_format(self, name):
        return bool(Utils.is_file_name_valid(name))

    def _get_all_local_migrations(self):
        local_files = Utils.get_local_files()
        if not local_files:
            return []
        migrations = [Migration.from_name(local_file) for local_file in local_files]
        return Utils.sort_migrations_list(migrations)
