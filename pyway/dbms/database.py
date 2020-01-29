from pydoc import locate


def factory(dbms):
    return locate('pyway.dbms.%s.%s' % (dbms, dbms.title()))
