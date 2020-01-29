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


# PYWAY VARIABLES
DATABASE_MIGRATION_DIR = os.environ.get('PYWAY_DATABASE_MIGRATION_DIR', 'resources')
SQL_MIGRATION_PREFIX = os.environ.get('PYWAY_SQL_MIGRATION_PREFIX', 'V')
SQL_MIGRATION_SEPARATOR = os.environ.get('PYWAY_SQL_MIGRATION_SEPARATOR', '__')
SQL_MIGRATION_SUFFIXES = os.environ.get('PYWAY_SQL_MIGRATION_SUFFIXES', '.sql')
TABLE = os.environ.get('PYWAY_TABLE', 'public.schema_version')
DBMS = os.environ['PYWAY_DBMS']
LOGS_DIR = os.getenv('PYWAY_LOGS_DIR', 'logs')


# DATABASE VARIABLES
DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_PORT = os.environ.get('DATABASE_PORT', '5432')
DATABASE_NAME = os.environ['DATABASE_NAME']
DATABASE_USERNAME = os.environ['DATABASE_USERNAME']
DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
DATABASE_CONNECT_TIMEOUT = os.environ.get('DATABASE_CONNECT_TIMEOUT', '30')
DATABASE_MAX_CONNECTIONS = os.environ.get('DATABASE_MAX_CONNECTIONS', '10')
