import os
import argparse
import yaml

# Pyway consts
SQL_MIGRATION_PREFIX = os.environ.get('PYWAY_SQL_MIGRATION_PREFIX', 'V')
SQL_MIGRATION_SEPARATOR = os.environ.get('PYWAY_SQL_MIGRATION_SEPARATOR', '__')
SQL_MIGRATION_SUFFIXES = os.environ.get('PYWAY_SQL_MIGRATION_SUFFIXES', '.sql')
ARGS = ['database_migration_dir', 'database_table', 'database_type', 'database_host',
        'database_port', 'database_name', 'database_username', 'database_password',
        'schema_file', 'config', 'version', 'cmd']


def parse_args(config, args):
    for arg in ARGS:
        if getattr(args, arg):
            setattr(config, arg, getattr(args, arg))
    return config


class Settings:

    def __init__(self, args):
        self.args = args

    @staticmethod
    def parse_arguments(config):
        parser = argparse.ArgumentParser()
        parser.add_argument("--database-migration-dir", help="Database migration directory")
        parser.add_argument("--database-table", help="Database table that stores pyway metadata")
        parser.add_argument("--database-type", help="Database type [postgres|mysql]")
        parser.add_argument("--database-host", help="Database host")
        parser.add_argument("--database-port", help="Database port")
        parser.add_argument("--database-name", help="Database name")
        parser.add_argument("--database-username", help="Database username")
        parser.add_argument("--database-password", help="Database password")
        parser.add_argument("--schemas", help="Comma separated list of schemas")
        parser.add_argument("--run-migration-on-default-schema", help="Boolean flag to check and run migration on"
                                                                      "default schema specified", default=True)
        parser.add_argument("--fail-migration-on-at-least-one-schema-failure",
                            help="Boolean flag to check and update the migration status on failures of "
                                 "multiple schemas", default=False)
        parser.add_argument("--create-schema", help="Boolean flag when set creates the schema if not exists",
                            default=False)
        parser.add_argument("--default-schema", help="Default schema in which migration history will be maintained")
        parser.add_argument("--run-migration-on-all-schemas-in-db-with-ms-env-prefix",
                            help="Boolean flag to check and run migration on all schemas prefixed with ms_env variable")
        parser.add_argument("--ms-env", help="Environment variable to check for schema prefix")
        parser.add_argument("--schema-file", help="Schema file for import")
        parser.add_argument("-c", "--config", help="Config file")
        parser.add_argument("-v", "--version", help="Version", action='store_true')
        parser.add_argument("cmd", nargs="?", help="info|validate|migrate|import")

        parse_args(config, parser.parse_args())
        return config, parser

    @staticmethod
    def parse_config_file(config):
        # See if there is a config file
        if os.path.exists(config.config):
            with open(config.config, "r", encoding='utf-8') as ymlfile:
                cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

            # Merge config together with args
            for c in cfg:
                setattr(config, c, cfg[c])

        return config


class ConfigFile:
    def __init__(self):
        self.database_migration_dir = os.environ.get('PYWAY_DATABASE_MIGRATION_DIR', 'pyway_migrations/versions')
        self.database_table = os.environ.get('PYWAY_DATABASE_TABLE', 'pyway_migration_history')
        self.database_type = os.environ.get('PYWAY_DATABASE_TYPE', 'postgres')
        self.database_host = os.environ.get('PYWAY_DATABASE_HOST', 'localhost')
        self.database_port = os.environ.get('PYWAY_DATABASE_PORT', '5432')
        self.database_name = os.environ.get('PYWAY_DATABASE_NAME', 'postgres')
        self.database_username = os.environ.get('PYWAY_DATABASE_USERNAME', 'postgres')
        self.database_password = os.environ.get('PYWAY_DATABASE_PASSWORD', 'password')
        self.schema_file = None
        self.config = os.environ.get('PYWAY_CONFIG_FILE', '.pyway.conf')
        self.version = False
        self.cmd = None
        self.run_migration_on_default_schema = os.environ.get('PYWAY_RUN_MIGRATION_ON_DEFAULT_SCHEMA', True)
        self.create_schema = os.environ.get('PYWAY_CREATE_SCHEMA', True)
        self.schemas = os.environ.get('PYWAY_SCHEMAS', "")
        self.fail_migration_on_at_least_one_schema_failure = os.environ.get(
            'PYWAY_FAIL_MIGRATION_ON_AT_LEAST_ONE_SCHEMA_FAILURE', False)
        self.default_schema = os.environ.get('PYWAY_DEFAULT_SCHEMA', "public")
        self.run_migration_on_all_schemas_in_db_with_ms_env_prefix = os.environ.get(
            'PYWAY_RUN_MIGRATION_ON_ALL_SCHEMAS_IN_DB_WITH_MS_ENV_PREFIX', False)
        self.ms_env = os.environ.get('MS_ENV', "dev")
