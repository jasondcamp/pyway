import os

from .log import logger
from .settings import DATABASE_MIGRATION_DIR, LOGS_DIR


def _dir_maker(dir_):
    if not os.path.exists(dir_):
        logger.info("%s don't found, creating local folder" % dir_)
        os.makedirs(dir_)


_dir_maker(LOGS_DIR)
_dir_maker(DATABASE_MIGRATION_DIR)

'''
import os
import sys
import logging
import dotenv

logger = logging.getLogger(__name__)

dotenv.load_dotenv()
ENVIRONMENT = os.getenv('ENVIRONMENT')

if not ENVIRONMENT:
    logger.error('Required ENVIRONMENT env variable')
    sys.exit(1)

env_dotfile = os.path.join(os.getcwd(), '.env.' + ENVIRONMENT)

if not os.path.exists(env_dotfile):
    logger.warn('%s not found. Environment variables will be used.' % env_dotfile)
else:
    logger.info('Loading dotenv for environment %s: %s', ENVIRONMENT, env_dotfile)
    dotenv.load_dotenv(dotenv_path=env_dotfile)
'''
