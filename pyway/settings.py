import os
import sys
import argparse
from .version import __version__

# Initialization
LOGO = f"PyWay {__version__}"

parser = argparse.ArgumentParser()
parser.add_argument("--database-migration-dir", help="Database migration directory", default=os.environ.get('PYWAY_DATABASE_MIGRATION_DIR', 'resources'))
parser.add_argument("--database-table", help="Database table that stores pyway metadata", default=os.environ.get('PYWAY_TABLE', 'public.schema_version'))
parser.add_argument("--database-type", help="Database type [postgres|mysql]", default=os.environ.get('PYWAY_DBMS', 'postgres'))

parser.add_argument("--database-host", help="Database host", default=os.environ.get('PYWAY_DATABASE_HOST', 'localhost'))
parser.add_argument("--database-port", help="Database port", default=os.environ.get('PYWAY_DATABASE_PORT', '5432'))
parser.add_argument("--database-name", help="Database name", default=os.environ.get('PYWAY_DATABASE_NAME', 'postgres'))
parser.add_argument("--database-username", help="Database username", default=os.environ.get('PYWAY_DATABASE_USERNAME', 'postgres'))
parser.add_argument("--database-password", help="Database password", default=os.environ.get('PYWAY_DATABASE_PASSWORD', 'password'))

parser.add_argument("--logs-dir", help="Logs directory", default=os.environ.get('PYWAY_LOGS_DIR', 'logs'))
parser.add_argument("cmd", help="info|validate|migrate")

args = parser.parse_args()

# Pyway vars
SQL_MIGRATION_PREFIX = os.environ.get('PYWAY_SQL_MIGRATION_PREFIX', 'V')
SQL_MIGRATION_SEPARATOR = os.environ.get('PYWAY_SQL_MIGRATION_SEPARATOR', '__')
SQL_MIGRATION_SUFFIXES = os.environ.get('PYWAY_SQL_MIGRATION_SUFFIXES', '.sql')
