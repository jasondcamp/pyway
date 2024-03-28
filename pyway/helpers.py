import os
import re
import zlib
from typing import Any, Dict, List, Iterable

from pyway import settings
from pyway.errors import VALID_NAME_ERROR, DIRECTORY_NOT_FOUND, OUT_OF_DATE_ERROR


class bcolors():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Utils():

    @staticmethod
    def subtract(list_a: List, list_b: List) -> List:
        result = []
        if list_a and list_b:
            checksum_list_b = [b.checksum for b in list_b]
            result = [a for a in list_a if a.checksum not in checksum_list_b]
        elif list_a and not list_b:
            # List B is empty (usually from a new install)
            return list_a
        return result

    @staticmethod
    def expected_pattern() -> str:
        return f'{settings.SQL_MIGRATION_PREFIX}{{major}}_{{minor}}{settings.SQL_MIGRATION_SEPARATOR}' \
                f'{{description}}{settings.SQL_MIGRATION_SUFFIXES}'

    @staticmethod
    def is_file_name_valid(name: str) -> bool:
        _pattern = r"%s\d+[._]\d+|\d+[._]\d+__%s\.%s$" % \
            (settings.SQL_MIGRATION_PREFIX, settings.SQL_MIGRATION_SEPARATOR, settings.SQL_MIGRATION_SUFFIXES)
        return re.match(_pattern, name, re.IGNORECASE) is not None

    @staticmethod
    def sort_migrations_list(migrations: List[Any]) -> List[Any]:
        return sorted(migrations, key=lambda x: [x.get("version"), x.get("name")] if isinstance(x, dict) else
                                                [x.version, x.name], reverse=False)

    @staticmethod
    def flatten_migrations(migrations: Iterable[Any]) -> List[Dict[Any, Any]]:
        migration_list = []
        for migration in migrations:
            migration_list.append({'version': migration.version, 'extension': migration.extension,
                                   'name': migration.name, 'checksum': migration.checksum,
                                   'apply_timestamp': migration.apply_timestamp})
        return migration_list

    @staticmethod
    def get_version_from_name(name: str) -> str:
        ver = re.findall(r"(\d+[._]\d+|\d+)[._](\d+)__", name)
        if not ver:
            raise ValueError(VALID_NAME_ERROR % (name, Utils.expected_pattern()))

        if isinstance(ver[0], tuple):
            version: str = ".".join(ver[0])
            version = version.replace("_", ".")
        else:
            version = ver[0].replace("_", ".")

        return version

    @staticmethod
    def get_extension_from_name(name: str) -> str:
        return name.split('.')[-1].upper()

    @staticmethod
    def load_checksum_from_name(name: str, path: str) -> str:
        fullname = os.path.join(os.getcwd(), path, name)
        prev = 0
        try:
            for line in open(fullname, "rb"):
                prev = zlib.crc32(line, prev)
            return "%X" % (prev & 0xFFFFFFFF)
        except FileNotFoundError:
            raise FileNotFoundError(OUT_OF_DATE_ERROR % fullname.split("/")[-1])

    @staticmethod
    def basepath(d: str) -> str:
        return os.path.join(os.getcwd(), d)

    @staticmethod
    def get_local_files(d: str) -> List[str]:
        path = Utils.basepath(d)
        dir_list = []
        try:
            # Skip any hidden files
            for f in os.listdir(path):
                if not f.startswith('.'):
                    dir_list.append(f)
        except OSError:
            raise FileNotFoundError(DIRECTORY_NOT_FOUND % path)
        return dir_list

    @staticmethod
    def create_map_from_list(key: str, list_: List[Any]) -> Dict[Any, Any]:
        return {lst.__dict__[key]: lst for lst in list_}

    @staticmethod
    def color(msg: str, color: str) -> str:
        return f"{color}{msg}{bcolors.ENDC}"
