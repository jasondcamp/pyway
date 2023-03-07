import os
import argparse
import yaml
import sys

# Pyway consts
SQL_MIGRATION_PREFIX = os.environ.get('PYWAY_SQL_MIGRATION_PREFIX', 'V')
SQL_MIGRATION_SEPARATOR = os.environ.get('PYWAY_SQL_MIGRATION_SEPARATOR', '__')
SQL_MIGRATION_SUFFIXES = os.environ.get('PYWAY_SQL_MIGRATION_SUFFIXES', '.sql')

class Settings():

    def __init__(self, args):
        self.args = args

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

        parser.add_argument("--schema-file", help="Schema file for import")
        parser.add_argument("-c", "--config", help="Config file")
        parser.add_argument("-v", "--version", help="Version", action='store_true')
        parser.add_argument("cmd", nargs="?", help="info|validate|migrate|import")

        args = parser.parse_args()

        if args.database_migration_dir:
            config.database_migration_dir = args.database_migration_dir
        if args.database_table:
            config.database_table = args.database_table
        if args.database_type:
            config.database_type = args.database_type
        if args.database_host:
            config.database_host = args.database_host
        if args.database_port:
            config.database_port = args.database_port
        if args.database_name:
            config.database_name = args.database_name
        if args.database_username:
            config.database_username = args.database_username
        if args.database_password:
            config.database_password = args.database_password
        if args.schema_file:
            config.schema_file = args.schema_file
        if args.config:
            config.config = args.config
        if args.version:
            config.version = args.version
        if args.cmd:
            config.cmd = args.cmd

        # Display version if it exists
        if args.version:
            print(f"Version: {__version__}")
            sys.exit(1)

        return config


    def parse_config_file(config):
        # See if there is a config file
        if os.path.exists(config.config):
            with open(config.config, "r", encoding='utf-8') as ymlfile:
                cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

            # Merge config together with args
            for c in cfg:
                setattr(config, c, cfg[c])

        return config

class ConfigFile():
    def __init__(self):
        self.database_migration_dir = os.environ.get('PYWAY_DATABASE_MIGRATION_DIR', 'resources')
        self.database_table = os.environ.get('PYWAY_TABLE', 'public.pyway')
        self.database_type = default=os.environ.get('PYWAY_TYPE', 'postgres')
        self.database_host = default=os.environ.get('PYWAY_DATABASE_HOST', 'localhost')
        self.database_port = default=os.environ.get('PYWAY_DATABASE_PORT', '5432')
        self.database_name = default=os.environ.get('PYWAY_DATABASE_NAME', 'postgres')
        self.database_username = os.environ.get('PYWAY_DATABASE_USERNAME', 'postgres')
        self.database_password = os.environ.get('PYWAY_DATABASE_PASSWORD', 'password')
        self.schema_file = None
        self.config = os.environ.get('PYWAY_CONFIG_FILE', '.pyway.conf')
        self.version = False
        self.cmd = None

