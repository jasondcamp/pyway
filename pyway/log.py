import sys
import logging
from pyway.helpers import Utils
from pyway.helpers import bcolors
from pyway.exceptions import InvalidLogLevel


class _Log():
    def __init__(self):
        self.logger = logging.getLogger('pyway')
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.setLevel(logging.INFO)

    def debug(self, msg):
        if self.logger:
            self.logger.debug(msg)

    def info(self, msg):
        if self.logger:
            self.logger.info(Utils.color(msg, bcolors.OKBLUE))

    def error(self, msg):
        if self.logger:
            self.logger.error(Utils.color(msg, bcolors.FAIL))

    def success(self, msg):
        self.logger.info(Utils.color(msg, bcolors.OKGREEN))

    def setlevel(self, log_level):
        if log_level == "INFO":
            self.logger.setLevel(logging.INFO)
        elif log_level == "DEBUG":
            self.logger.setLevel(logging.DEBUG)
        elif log_level == 'ERROR':
            self.logger.setLevel(logging.ERROR)
        elif log_level == 'WARN':
            self.logger.setLevel(logging.WARN)
        else:
            raise InvalidLogLevel

logger = _Log()
