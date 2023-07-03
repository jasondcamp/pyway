import sys

from pyway.settings import Settings
from pyway.settings import ConfigFile
from pyway.info import Info
from pyway.log import logger
from pyway.migrate import Migrate
from pyway.validate import Validate
from pyway.import_ import Import
from pyway.version import __version__


def migrate(config):
    logger.info('Starting migration process...')
    output = Migrate(config).run()
    logger.info(output)
    logger.info('Migration completed.')


def validate(config):
    logger.info('Starting validation process')
    output = Validate(config).run()
    logger.info(output)
    logger.info('Validation completed.')


def info(config):
    logger.info('Gathering info...')
    tbl = Info(config).run()
    logger.info(tbl)
    print()


def import_(config):
    logger.info("Importing schema...")
    migration_name = Import(config).run()
    logger.info(f"{migration_name} Imported")


def cli():
    logger.info(f"PyWay {__version__}")

    config = ConfigFile()
    (config, parser) = Settings.parse_arguments(config)
    config = Settings.parse_config_file(config)

    # Display version if it exists
    if config.version:
        print(f"Version: {__version__}")
        sys.exit(1)

    # If no arg is specified, show help
    if not config.cmd:
        # TODO: figure out how to print help
        parser.print_help()
        sys.exit(1)

    if config.cmd == "info":
        info(config)
    elif config.cmd == "validate":
        validate(config)
    elif config.cmd == "migrate":
        migrate(config)
    elif config.cmd == "import":
        import_(config)
    else:
        logger.error(f"Command '{config.cmd}' not recognized, exiting!")
        sys.exit(1)


if __name__ == '__main__':
    cli()
