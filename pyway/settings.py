import os
import argparse
import yaml
from typing import Tuple, Dict, Union

from pyway.configfile import ConfigFile
from pyway.configfile import MockArgs

# Pyway consts
SQL_MIGRATION_PREFIX = os.environ.get('PYWAY_SQL_MIGRATION_PREFIX', 'V')
SQL_MIGRATION_SEPARATOR = os.environ.get('PYWAY_SQL_MIGRATION_SEPARATOR', '__')
SQL_MIGRATION_SUFFIXES = os.environ.get('PYWAY_SQL_MIGRATION_SUFFIXES', '.sql')
ARGS = ['database_migration_dir', 'database_table', 'database_type', 'database_host',
        'database_port', 'database_name', 'database_username', 'database_password',
        'schema_file', 'checksum_file', 'config', 'version', 'cmd']


class Settings():
    @staticmethod
    def parse_args(config: ConfigFile, args: Union[argparse.Namespace, MockArgs]) -> ConfigFile:
        for arg in ARGS:
            if getattr(args, arg):
                setattr(config, arg, getattr(args, arg))
        return config

    @classmethod
    def parse_arguments(self, config: ConfigFile) -> Tuple[ConfigFile, argparse.ArgumentParser]:
        parser: argparse.ArgumentParser = argparse.ArgumentParser()
        parser.add_argument("--database-migration-dir", help="Database migration directory")
        parser.add_argument("--database-table", help="Database table that stores pyway metadata")
        parser.add_argument("--database-type", help="Database type [postgres|mysql|duckdb]")
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

        new_config: ConfigFile = self.parse_args(config, parser.parse_args())
        return (new_config, parser)

    @classmethod
    def parse_config_file(self, config: ConfigFile) -> ConfigFile:
        # See if there is a config file
        if os.path.exists(config.config):
            with open(config.config, "r", encoding='utf-8') as ymlfile:
                cfg: Dict = yaml.load(ymlfile, Loader=yaml.FullLoader)

            # Merge config together with args
            for c in cfg:
                if isinstance(cfg[c], str):
                    # Interpolate env vars
                    cfg[c] = os.path.expandvars(cfg[c])
                setattr(config, c, cfg[c])

        return config
