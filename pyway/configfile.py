import os


class ConfigFile():
    def __init__(self) -> None:
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
