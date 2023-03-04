import os
import sys
import logging
from datetime import date

from pyway import settings

LOG_TO_FILE=False
LOG_DIR="logs"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class _Log():
    def __init__(self):
        logging.debug("magic")
        self.logger = logging.getLogger('pyway')
        self.logger.setLevel(logging.INFO)

    def debug(self, msg):
        if self.logger:
            self.logger.debug(msg)

    def info(self, msg):
        if self.logger:
            self.logger.info(self._colored(msg, bcolors.OKBLUE))

    def error(self, msg):
        if self.logger:
            self.logger.error(self._colored(msg, bcolors.FAIL))

    def warn(self, msg):
        if self.logger:
            self.logger.warn(self._colored(msg, bcolors.WARNING))

    def _colored(self, msg, color):
        return f"{color}{msg}{bcolors.ENDC}"

    def success(self, msg):
        if self.logger:
            self.logger.info(self._colored(msg, bcolors.OKGREEN))


logger = _Log()
