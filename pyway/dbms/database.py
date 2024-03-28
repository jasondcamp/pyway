from pydoc import locate
from typing import Any


def factory(dbms: str) -> Any:
    return locate('pyway.dbms.%s.%s' % (dbms, dbms.title()))
