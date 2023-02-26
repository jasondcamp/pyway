import os
import sys
import argparse

from .log import logger
from .settings import args


def _dir_maker(dir_):
    if not os.path.exists(dir_):
        logger.info("%s not found, creating local folder" % dir_)
        os.makedirs(dir_)

if args.log_to_file:
    _dir_maker(settings.args.logs_dir)

_dir_maker(settings.args.database_migration_dir)

