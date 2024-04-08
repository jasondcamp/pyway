import os
from typing import Any, Union


class ConfigFile():
    def __init__(self, **kwargs: Any) -> None:
        self.database_migration_dir = os.environ.get('PYWAY_DATABASE_MIGRATION_DIR', 'resources')
        self.database_table = os.environ.get('PYWAY_TABLE', kwargs.get('database_table'))
        self.database_type = os.environ.get('PYWAY_TYPE', kwargs.get('database_type'))
        self.database_host = os.environ.get('PYWAY_DATABASE_HOST', kwargs.get('database_host'))
        self.database_port = os.environ.get('PYWAY_DATABASE_PORT', kwargs.get('database_port'))
        self.database_name = os.environ.get('PYWAY_DATABASE_NAME', kwargs.get('database_name'))
        self.database_username = os.environ.get('PYWAY_DATABASE_USERNAME', kwargs.get('database_username'))
        self.database_password = os.environ.get('PYWAY_DATABASE_PASSWORD', kwargs.get('database_password'))
        self.schema_file: Union[str, None] = None
        self.checksum_file = None
        self.config = os.environ.get('PYWAY_CONFIG_FILE', '.pyway.conf')
        self.version = False
        self.cmd = None


class MockConfig():
    pass


class MockArgs():
    pass
