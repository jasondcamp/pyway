from .log import logger
from .helpers import Utils
from .dbms.database import factory
from .migration import Migration
from .errors import OUT_OF_DATE_ERROR, DIFF_NAME_ERROR, DIFF_CHECKSUM_ERROR, VALID_NAME_ERROR


class Validate():

    def __init__(self, conf):
        self._db = factory(conf.DBMS)(conf)

    def run(self):
        local_migrations = self._get_all_local_migrations()
        db_migrations = Migration.from_list(self._db.get_all_schema_migrations())
        local_migrations_map = Utils.create_map_from_list("version", local_migrations)

        for db_migration in db_migrations:
            logger.info("Validating --> %s" % db_migration.name)
            local_migration = local_migrations_map.get(db_migration.version)
            self._out_of_date(local_migration, db_migration)
            self._name_format(local_migration.name)
            self._diff_names(local_migration, db_migration)
            self._diff_checksum(local_migration, db_migration)
            logger.success("%s VALID" % db_migration.name)

    def _out_of_date(self, local_migration, db_migration):
        if local_migration is None:
            logger.error(OUT_OF_DATE_ERROR % db_migration.name)

    def _diff_names(self, local_migration, db_migration):
        if local_migration.name != db_migration.name:
            logger.error(DIFF_NAME_ERROR % (local_migration.name, db_migration.name))

    def _diff_checksum(self, local_migration, db_migration):
        if local_migration.checksum != db_migration.checksum:
            error = DIFF_CHECKSUM_ERROR % (local_migration.name, local_migration.checksum, db_migration.checksum)
            logger.error(error)

    def _name_format(self, name):
        if not Utils.is_file_name_valid(name):
            error = VALID_NAME_ERROR % (name, Utils.expected_pattern())
            logger.error(error)

    def _get_all_local_migrations(self):
        local_files = Utils.get_local_files()
        migrations = [Migration.from_name(local_file) for local_file in local_files]
        return Utils.sort_migrations_list(migrations)
