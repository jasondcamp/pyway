import os
from pyway.log import logger
from pyway.helpers import Utils
from pyway.migration import Migration
from pyway.dbms.database import factory
from pyway.errors import MIGRATIONS_NOT_FOUND
from pyway.helpers import bcolors


class Migrate():

    def __init__(self, args):
        self._db = factory(args.database_type)(args)
        self.migration_dir = args.database_migration_dir
        self.args = args

    def run(self):
        output = ''
        migrations_to_be_executed = self._get_migration_files_to_be_executed()
        if not migrations_to_be_executed:
            output += Utils.color("Nothing to do\n", bcolors.FAIL) 
            return output

        # Prepare list of schemas on which migration to be executed
        schema_list = []
        if self.args.run_migration_on_default_schema and self.args.default_schema:
            schema_list.append(self.args.default_schema)
        logger.info(f"run_migration_on_default_schema:: {self.args.run_migration_on_default_schema}")
        if self.args.run_migration_on_all_schemas_in_db_with_ms_env_prefix:
            schema_list.extend(self._db.get_all_schemas())
        elif self.args.schemas:
            schema_list.extend(self.args.schemas.split(','))

        if not len(schema_list):
            raise RuntimeError(f"Migration can't be executed since run migration on default db is set to false and "
                               f"there are no schemas mentioned in the config. To execute pyway migration, at least "
                               f"one schema is needed. Please correct the config and try again.")

        for migration in migrations_to_be_executed:
            logger.info(Utils.color(f"Migrating --> {migration.name}", bcolors.OKBLUE))
            failed_schema_list = []
            try:
                with open(os.path.join(os.getcwd(),
                          self.migration_dir, migration.name), "r", encoding='utf-8') as sqlfile:
                    script = sqlfile.read()
                    for schema_name in schema_list:
                        try:
                            schema_name = schema_name.strip()
                            logger.info(
                                Utils.color(f"Running migration --> {migration.name} on schema: {schema_name}",
                                            bcolors.OKBLUE))
                            self._db.execute(script, schema_name=schema_name)
                            logger.info(
                                Utils.color(f"Migration --> {migration.name} completed on schema: {schema_name}",
                                            bcolors.OKBLUE))
                        except Exception as ex:
                            logger.error(f"Exception occurred while running migration on schema {schema_name} and "
                                         f"the cause is {str(ex)}")
                            failed_schema_list.append(schema_name)
                            if self.args.fail_migration_on_at_least_one_schema_failure:
                                raise RuntimeError(ex)
                if len(schema_list) == len(failed_schema_list):
                    message = f"Current migration {migration.name} failed on all the schemas, hence failing the " \
                              f" migration without proceeding further."
                    logger.error(message)
                    raise RuntimeError(message)
                self._db.upgrade_version(migration)
                logger.info(Utils.color(f"{migration.name} SUCCESS\n", bcolors.OKBLUE))
            except Exception as error:
                raise RuntimeError(error)
        return output

    def _get_migration_files_to_be_executed(self):
        all_local_migrations = self._get_all_local_migrations()
        all_db_migrations = Migration.from_list(self._db.get_all_schema_migrations())

        if all_db_migrations and not all_local_migrations:
            raise RuntimeError(MIGRATIONS_NOT_FOUND % self.migration_dir)
        return Utils.subtract(all_local_migrations, all_db_migrations)

    def _get_all_local_migrations(self):
        local_files = Utils.get_local_files(self.migration_dir)
        if not local_files:
            return []
        migrations = [Migration.from_name(local_file, self.migration_dir) for local_file in local_files]
        return Utils.sort_migrations_list(migrations)
