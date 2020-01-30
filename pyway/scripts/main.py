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
    logger.info('STARTING MIGRATE PROCESS . . .')
    Migrate(settings).run()
    logger.info('.MIGRATE ENDED.')


@cli.command()
def validate():
    logger.info('STARTING VALIDATE PROCESS . . .')
    Validate(settings).run()
    logger.info('.VALIDATE ENDED.')


@cli.command()
def info():
    logger.info('INFO . . .')
    Info(settings).run()
    logger.info('.INFO ENDED.')


if __name__ == '__main__':
    cli()
