import os
import argparse
import yaml
import sys

from pyway.version import __version__

# Initialization
LOGO = f"PyWay {__version__}"

parser = argparse.ArgumentParser()
parser.add_argument("--database-migration-dir", help="Database migration directory",
        default=os.environ.get('PYWAY_DATABASE_MIGRATION_DIR', 'resources'))
parser.add_argument("--database-table", help="Database table that stores pyway metadata",
        default=os.environ.get('PYWAY_TABLE', 'public.pyway'))
parser.add_argument("--database-type", help="Database type [postgres|mysql]", default=os.environ.get('PYWAY_TYPE', 'postgres'))

parser.add_argument("--database-host", help="Database host", default=os.environ.get('PYWAY_DATABASE_HOST', 'localhost'))
parser.add_argument("--database-port", help="Database port", default=os.environ.get('PYWAY_DATABASE_PORT', '5432'))
parser.add_argument("--database-name", help="Database name", default=os.environ.get('PYWAY_DATABASE_NAME', 'postgres'))
parser.add_argument("--database-username", help="Database username", default=os.environ.get('PYWAY_DATABASE_USERNAME', 'postgres'))
parser.add_argument("--database-password", help="Database password", default=os.environ.get('PYWAY_DATABASE_PASSWORD', 'password'))

parser.add_argument("-c", "--config", help="Config file", default=os.environ.get('PYWAY_CONFIG_FILE', '.pyway.conf'))
parser.add_argument("-v", "--version", help="Version", action='store_true')
parser.add_argument("--logs-dir", help="Logs directory", default=os.environ.get('PYWAY_LOGS_DIR', 'logs'))
parser.add_argument("--log-to-file", help="Log to file", action='store_true')
parser.add_argument("cmd", nargs="?", help="info|validate|migrate")

args = parser.parse_args()

# Pyway vars that shouldn't change
SQL_MIGRATION_PREFIX = os.environ.get('PYWAY_SQL_MIGRATION_PREFIX', 'V')
SQL_MIGRATION_SEPARATOR = os.environ.get('PYWAY_SQL_MIGRATION_SEPARATOR', '__')
SQL_MIGRATION_SUFFIXES = os.environ.get('PYWAY_SQL_MIGRATION_SUFFIXES', '.sql')

# Display version if it exists
if args.version:
    print(f"Version: {__version__}")
    sys.exit(1)

# If no arg is specified, show help
if not args.cmd:
    parser.print_help()
    sys.exit(1)

# See if there is a config file
if os.path.exists(args.config):
    with open(args.config, "r", encoding='utf-8') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Merge config together with args
    if 'database' in cfg:
        if 'type' in cfg['database']:
            args.database_type = cfg['database']['type']
        if 'username' in cfg['database']:
            args.database_username = cfg['database']['username']
        if 'password' in cfg['database']:
            args.database_password = cfg['database']['password']
        if 'database' in cfg['database']:
            args.database_name = cfg['database']['database']
        if 'host' in cfg['database']:
            args.database_host = cfg['database']['host']
        if 'port' in cfg['database']:
            args.database_port = cfg['database']['port']

    if 'logging' in cfg:
        if 'logsdir' in cfg['logging']:
            args.logs_dir = cfg['logging']['logsdir']
        if 'logtofile' in cfg['logging']:
            args.log_to_file = cfg['logging']['logtofile']

    if 'general' in cfg:
        if 'migrationsdir' in cfg['general']:
            args.database_migration_dir = cfg['general']['migrationsdir']
        if 'pywaytable' in cfg['general']:
            args.database_table = cfg['general']['pywaytable']
