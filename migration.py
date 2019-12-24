class Migration:
    '''
    This class represents a migration for the database.
    A migration is built using a major version, minor version,
    and a name, may be built just as follow.

    >>> ddl_migration  = Migration(name='database_creation', major=0, minor=0)

    A migration normally will be generate from two main places, at least what I
    may think for now, from a file or from database.

    Mostly this class will not be instantiated by constructor, but by its
    alternative constructors, for example, from file:

    >>> Migration.fromfile('V00_01__DDL.sql')
    Migration(major=0, minor=1, name='DDL')

    More about fromfile method may be found on its own documentation.

    '''

    def __init__(self, major, minor, name):
        self.major = int(major)
        self.minor = int(minor)
        self.name = str(name)

    @classmethod
    def fromfile(cls, file):
        '''
        File may be an actual File instance or a string with a file path.
        If no path is given before the file name, it will be assumed './'
        >>> Migration.fromfile('V01_01__CREATE_TABLE_USER.sql')
        Migration(major=1, minor=1, name='CREATE_TABLE_USER')
        '''
        from pathlib import Path

        file = Path(file)
        major, minor, name = cls.parse_filename(file.name)
        return cls(major, minor, name)

    @staticmethod
    def parse_filename(filename):
        '''
        This will extract major, minor and name from a filepath string
        >>> Migration.parse_filename('V02_01__ADDING_PARSES_PATTERNS.sql')
        (2, 1, 'ADDING_PARSES_PATTERNS')
        '''
        version, name = filename.split('__')
        major, minor = version.split('_')
        name = name.split('.')[0]
        return int(major[1:]), int(minor), name

    def __repr__(self, *args, **kwargs):
        class_name = self.__class__.__name__
        return '{}(major={}, minor={}, name={})'.format(
            class_name, self.major, self.minor, repr(self.name))


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()
