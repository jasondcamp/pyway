import os
import sys
import logging
from datetime import date

from . import settings


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
        log_dir = settings.args.logs_dir
        if log_dir:
            if settings.args.log_to_file and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            self.logger = logging.getLogger('pyway')

            now = date.today()
            if settings.args.log_to_file:
                filename = f'{os.path.abspath(log_dir)}/{now.strftime("%Y_%m_%d")}.log'
                hdlr = logging.FileHandler(filename)
                formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
                hdlr.setFormatter(formatter)
                self.logger.addHandler(hdlr)
            self.logger.addHandler(logging.StreamHandler(sys.stdout))
            self.logger.setLevel(logging.DEBUG)

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
