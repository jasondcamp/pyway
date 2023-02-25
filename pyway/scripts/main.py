import click

from pyway import settings
from pyway.info import Info
from pyway.log import logger
from pyway.migrate import Migrate
from pyway.validate import Validate


@click.group()
def cli():
    logger.info(settings.LOGO)


@cli.command()
def migrate():
    logger.info('Starting migration process...')
    Migrate(settings).run()
    logger.info('Migration completed.')


@cli.command()
def validate():
    logger.info('Starting validation process')
    Validate(settings).run()
    logger.info('Validation completed.')


@cli.command()
def info():
    logger.info('Gathering info...')
    Info(settings).run()
    print()

if __name__ == '__main__':
    cli()
