from pydoc import locate
from typing import Any, Union


def factory(dbms: Union[str, None]) -> Any:
    if dbms:
        return locate('pyway.dbms.%s.%s' % (dbms, dbms.title()))
    return None
