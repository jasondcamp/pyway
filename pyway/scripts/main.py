import sys

from pyway.settings import Settings
from pyway.info import Info
from pyway.log import logger
from pyway.migrate import Migrate
from pyway.validate import Validate
from pyway.import_ import Import
from pyway.version import __version__

def migrate(args):
    logger.info('Starting migration process...')
    Migrate(args).run()
    logger.info('Migration completed.')


def validate(args):
    logger.info('Starting validation process')
    Validate(args).run()
    logger.info('Validation completed.')


def info(args):
    logger.info('Gathering info...')
    Info(args).run()
    print()

def import_(args):
    logger.info("Importing schema...")
    Import(args).run()

def cli():
    logger.info(f"PyWay {__version__}")

    args = Settings.parse_arguments()
    args = Settings.parse_config_file(args)

    if args.cmd == "info":
        info(args)
    elif args.cmd == "validate":
        validate(args)
    elif args.cmd == "migrate":
        migrate(args)
    elif args.cmd == "import":
        import_(args)
    else:
        logger.error(f"Command '{settings.args.cmd}' not recognized, exiting!")
        sys.exit(1)

if __name__ == '__main__':
    cli()
