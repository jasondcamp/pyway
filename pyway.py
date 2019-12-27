from pathlib import Path
from zlib import crc32 as checksum

from migration import Migration

class Pyway:
    '''
    Pyway is a Flyway like migration manager.

    For the ones that don't know Flyway, it is one migration manager from the
    java world. Different from Liqbase, in Flyway you just write the migration
    in the database own language, in the Flyway case SQL, other than a XML file
    descibing every table/entity in the database. In Liqbase the files represents
    how the database state, in Flyway it has a sequence of files with commands
    that will make the database get into the disered state.
    '''

    def __init__(self, dir):
        '''
        Passing a dir it will create a Pyway with a migration with all the migrations
        in that folder.

        Preparing cenario for example:
        >>> db_directory = Path('db')
        >>> db_directory.mkdir()
        >>> migration_example = db_directory / 'V01_01__EXAMPLE_MIGRATION.sql'
        >>> migration_example.touch()

        Example:
        >>> py = Pyway(dir='db')
        >>> list(py.migrations)
        [Migration(major=1, minor=1, name='EXAMPLE_MIGRATION')]

        Cleaning cenario:
        >>> migration_example.unlink()
        >>> db_directory.rmdir()
        '''

        migrations_directory = Path(dir)
        assert migrations_directory.is_dir(), 'dir must be a directory'
        self.dir = migrations_directory
        # TODO: Verify if all file have same format, error if not


    @property
    def migrations(self):
        for f in self.dir.iterdir():
            m = Migration.fromfile(f)
            m.checksum = checksum(f.read_bytes())
            yield m



def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()
