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

env_dotfile = os.path.join('.env.' + ENVIRONMENT)

if not os.path.exists(env_dotfile):
    logger.error('Failed loading dotenv file "%s"', env_dotfile)
    sys.exit(1)

logger.info('Loading dotenv for environment %s: %s', ENVIRONMENT, env_dotfile)
dotenv.load_dotenv(dotenv_path=env_dotfile)
