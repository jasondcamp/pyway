import sys
import os

from pyway.settings import Settings
from pyway.configfile import ConfigFile
from pyway.info import Info
from pyway.log import logger
from pyway.migrate import Migrate
from pyway.validate import Validate
from pyway.import_ import Import
from pyway.checksum import Checksum
from pyway.helpers import Utils
from pyway.version import __version__


def migrate(config: ConfigFile) -> None:
    # Validate first
    validate(config)

    logger.info('Starting migration process...')
    output = Migrate(config).run()
    logger.info(output)
    logger.info('Migration completed.')


def validate(config: ConfigFile) -> None:
    logger.info('Starting validation process')
    output = Validate(config).run(skip_initial_check=True)
    logger.info(output)
    logger.info('Validation completed.')


def info(config: ConfigFile) -> None:
    logger.info('Gathering info...')
    tbl = Info(config).run()
    logger.info(tbl)


def import_(config: ConfigFile) -> None:
    logger.info("Importing schema...")
    migration_name = Import(config).run()
    logger.info(f"{migration_name} Imported")


def checksum(config: ConfigFile) -> None:
    logger.info("Updating checksum...")
    name, checksum = Checksum(config).run()
    logger.info(f"{name} checksum updated to {checksum}")


def cli() -> None:
    logger.info(f"PyWay {__version__}")

    config = Settings.parse_arguments()
    config_file = Settings.parse_config_file(config.config)
    config.merge(config_file)

    # Base validation - required for all databases
    required_vars = ["database_type", "database_table", "database_name"]
    
    # Database-specific validation
    if config.database_type == "oracle":
        # Oracle: flexible validation based on connection method
        oracle_use_wallet = getattr(config, 'oracle_use_wallet', False)
        wallet_location = getattr(config, 'oracle_wallet_location', None) or os.getenv('TNS_ADMIN')
        has_username = getattr(config, 'database_username', None)
        
        # For Oracle, database_username is only required if not using wallet
        if not oracle_use_wallet and not wallet_location and not has_username:
            required_vars.append("database_username")
        
        # For Oracle, database_host is optional (can use TNS Names)
        # Do not add database_host to required_vars for Oracle
    else:
        # For all other databases: require host and username
        required_vars.extend(["database_host", "database_username"])
    
    # Validate required fields
    Utils.check_required_vars(required_vars, config)

    if config.cmd == "info":
        info(config)
    elif config.cmd == "validate":
        validate(config)
    elif config.cmd == "migrate":
        migrate(config)
    elif config.cmd == "import":
        import_(config)
    elif config.cmd == "checksum":
        checksum(config)
    else:
        logger.error(f"Command '{config.cmd}' not recognized, exiting!")
        sys.exit(1)


if __name__ == '__main__':
    cli()
