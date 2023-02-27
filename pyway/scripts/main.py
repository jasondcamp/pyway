import sys

from pyway import settings
from pyway.info import Info
from pyway.log import logger
from pyway.migrate import Migrate
from pyway.validate import Validate


def migrate():
    logger.info('Starting migration process...')
    Migrate(settings).run()
    logger.info('Migration completed.')


def validate():
    logger.info('Starting validation process')
    Validate(settings).run()
    logger.info('Validation completed.')


def info():
    logger.info('Gathering info...')
    Info(settings).run()
    print()

def cli():
    logger.info(settings.LOGO)

    if settings.args.cmd == "info":
        info()
    elif settings.args.cmd == "validate":
        validate()
    elif settings.args.cmd == "migrate":
        migrate()
    else:
        logger.error(f"Command '{settings.args.cmd}' not recognized, exiting!")
        sys.exit(1)

if __name__ == '__main__':
    cli()
