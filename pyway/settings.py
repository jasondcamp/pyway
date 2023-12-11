import os
import argparse
import yaml

# Pyway consts
SQL_MIGRATION_PREFIX = os.environ.get('PYWAY_SQL_MIGRATION_PREFIX', 'V')
SQL_MIGRATION_SEPARATOR = os.environ.get('PYWAY_SQL_MIGRATION_SEPARATOR', '__')
SQL_MIGRATION_SUFFIXES = os.environ.get('PYWAY_SQL_MIGRATION_SUFFIXES', '.sql')
ARGS = ['database_migration_dir', 'database_table', 'database_type', 'database_host',
        'database_port', 'database_name', 'database_username', 'database_password',
        'schema_file', 'checksum_file', 'config', 'version', 'cmd']


class Settings():

    def __init__(self, args):
        self.args = args


    @staticmethod
    def parse_args(config, args):
        for arg in ARGS:
            if getattr(args, arg):
                setattr(config, arg, getattr(args, arg))
        return config

    @classmethod
    def parse_arguments(self, config):
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
        parser.add_argument("--checksum-file", help="Checksum to update")
        parser.add_argument("-c", "--config", help="Config file")
        parser.add_argument("-v", "--version", help="Version", action='store_true')
        parser.add_argument("cmd", nargs="?", help="info|validate|migrate|import|checksum")

        config = self.parse_args(config, parser.parse_args())
        return (config, parser)

    @classmethod
    def parse_config_file(self, config):
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
        self.database_type = os.environ.get('PYWAY_TYPE', 'postgres')
        self.database_host = os.environ.get('PYWAY_DATABASE_HOST', 'localhost')
        self.database_port = os.environ.get('PYWAY_DATABASE_PORT', '5432')
        self.database_name = os.environ.get('PYWAY_DATABASE_NAME', 'postgres')
        self.database_username = os.environ.get('PYWAY_DATABASE_USERNAME', 'postgres')
        self.database_password = os.environ.get('PYWAY_DATABASE_PASSWORD', 'password')
        self.schema_file = None
        self.checksum_file = None
        self.config = os.environ.get('PYWAY_CONFIG_FILE', '.pyway.conf')
        self.version = False
        self.cmd = None
