from pydoc import locate


def factory(sgbd):
    return locate('pyway.sgbds.%s.%s' % (sgbd, sgbd.title()))
