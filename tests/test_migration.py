import pytest
import os
from pyway.migration import Migration


@pytest.mark.migration_test
def test_from_list() -> None:
    migrations = []
    migration = Migration('01.01', 'SQL', 'V01_01__testfile.sql', '53175082', '2023-02-28 15:56:14')
    migrations.append(migration)
    test_list = Migration.from_list(migrations)
    assert test_list[0].name == migration.name


@pytest.mark.migration_test
def test_from_name() -> None:
    migration = Migration.from_name('V01_01__test1.sql', os.path.join('tests', 'data', 'schema'))
    assert migration.name == 'V01_01__test1.sql'
    assert migration.version == "01.01"


@pytest.mark.migration_test
def test_semantic_version_from_name() -> None:
    migration = Migration.from_name('V01_01_01__test1.sql', os.path.join('tests', 'data', 'schemasemver'))
    assert migration.name == 'V01_01_01__test1.sql'
    assert migration.version == "01.01.01"
