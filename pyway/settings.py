import os
from version import __version__
# INITIALIZATION
LOGO = """
     ██████╗ ██╗   ██╗██╗    ██╗ █████╗ ██╗   ██╗
     ██╔══██╗╚██╗ ██╔╝██║    ██║██╔══██╗╚██╗ ██╔╝
     ██████╔╝ ╚████╔╝ ██║ █╗ ██║███████║ ╚████╔╝
     ██╔═══╝   ╚██╔╝  ██║███╗██║██╔══██║  ╚██╔╝
     ██║        ██║   ╚███╔███╔╝██║  ██║   ██║
     ╚═╝        ╚═╝    ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝
                        %s
""" % __version__

# SETTINGS
DATABASE_MIGRATION_DIR = 'resources'  # DIR path from migrations files
SQL_MIGRATION_PREFIX = 'V'  # FILE NAME PREFIX FOR SQL MIGRATIONS]
SQL_MIGRATION_SEPARATOR = '__'  # FILE NAME SEPARATOR FOR SQL MIGRATIONS]
SQL_MIGRATION_SUFFIXES = '.sql'  # FILE NAME SUFFIX FOR SQL MIGRATIONS]
TABLE = 'public.schema_version'  # TABLE_VERSION NAME
SGBD = 'postgres'


# ENVIRONMENTS VARIABLES
DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_PORT = os.environ.get('DATABASE_PORT', '5432')
DATABASE_NAME = os.environ['DATABASE_NAME']
DATABASE_USERNAME = os.environ['DATABASE_USERNAME']
DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
DATABASE_CONNECT_TIMEOUT = os.environ.get('DATABASE_CONNECT_TIMEOUT', '30')
DATABASE_MAX_CONNECTIONS = os.environ.get('DATABASE_MAX_CONNECTIONS', '10')
LOGS_DIR = os.getenv('LOGS_DIR', 'logs')
