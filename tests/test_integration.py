import pytest
import os
from strip_ansi import strip_ansi
from pyway.info import Info
# from pyway.migrate import Migrate
# from pyway.validate import Validate
# from pyway.import_ import Import
# from pyway.settings import Settings
from pyway.settings import ConfigFile
from mysqld_integration_test import Mysqld
import mysql.connector

INFO_TABLE = """+-----------+-------------+-------------------+------------+-------------------+
|   version | extension   | name              | checksum   | apply_timestamp   |
|-----------+-------------+-------------------+------------+-------------------|
|      1.01 | SQL         | V01_01__test1.sql | new        | new               |
|      1.02 | SQL         | V01_02__test2.sql | new        | new               |
|      1.03 | SQL         | V01_03__test3.sql | new        | new               |
+-----------+-------------+-------------------+------------+-------------------+"""


def execute_query(mysqld, query):
    cnx = mysql.connector.connect(user=mysqld.username,
                                  password=mysqld.password,
                                  host=mysqld.host,
                                  port=mysqld.port, database='test')
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()


def select_query(mysqld, query):
    cnx = mysql.connector.connect(user=mysqld.username,
                                  password=mysqld.password,
                                  host=mysqld.host,
                                  port=mysqld.port, database='test')
    cursor = cnx.cursor()
    cursor.execute(query)
    for _result in cursor:
        result = _result
    cursor.close()
    cnx.close()

    return result[0]


@pytest.fixture
def mysqld_connect(autouse=True):
    mysqld = Mysqld()
    return mysqld.run()


@pytest.mark.integration_test
def test_pyway_table_creation(mysqld_connect):
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mysqld_connect.host
    config.database_username = mysqld_connect.username
    config.database_password = mysqld_connect.password
    config.database_port = mysqld_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data')
    tbl = Info(config).run()

    assert strip_ansi(tbl) == INFO_TABLE
