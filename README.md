[![Build Status](https://travis-ci.org/sergiosbx/pyway.svg?branch=master)](https://travis-ci.org/sergiosbx/pyway)


Pyway Database Version Control
===============================

version number: 0.2.0


Overview
--------

Pyway is a database versioning and migration tool inspired on Flyway


Download and Install
--------------------

To install use pip:

    $ pip install pyway


Or on requirements:

    git+git://github.com/sergiosbx/pyway@{version}


Or clone the repo:

    $ git clone https://github.com/sergiosbx/pyway.git
    $ python setup.py install


CONFIGURATION
-------

#### PYWAY

| Variable | Description | Default |
| --------------- | -------------- | :--------------: |
| PYWAY_DATABASE_MIGRATION_DIR | Folder name to migration files | resources |
| PYWAY_SQL_MIGRATION_PREFIX | Prefix for version in migration file | V |
| PYWAY_SQL_MIGRATION_SEPARATOR | Separator between version and description to the migration file | __ |
| PYWAY_SQL_MIGRATION_SUFFIXES | Suffix extension for migration files | .sql |
| PYWAY_TABLE | Name of schema history table | public.schema_version |
| PYWAY_DBMS | Data Base Management System [`postgres`, `oracle`, `mysql`, `sqlserver`] | *required* |
| PYWAY_LOGS_DIR | Folder name to logs construct | logs |


#### DATABASE

| Variable | Description | Default
| --------------- | -------------- | :--------------: |
| DATABASE_URL | URL to connect to the database | *required* |
| DATABASE_PORT | Port to connect to the database | *required* |
| DATABASE_NAME | Name of database to connect | *required* |
| DATABASE_USERNAME | User to use to connect to the database | *required* |
| DATABASE_PASSWORD | Password to use to connect to the database | *required* |
| DATABASE_CONNECT_TIMEOUT | Timeout to connect to the database (seconds) | 30 |
| DATABASE_MAX_CONNECTIONS | Max connections to the database | 10 |


USAGE
-------

#### INFO
Information lets you know where you are. At first glance, you will see which migrations have already been applied, which others are still pending, and whether there is a discrepancy between the checksum of the local file and the database schema table.

    $ pyway info


#### VALIDATE
Validate helps you verify that the migrations applied to the database match the ones available locally.

    $ pyway validate


#### MIGRATE
After `VALIDATE`, it will scan the **PYWAY_DATABASE_MIGRATION_DIR** for available migrations. It will compare them to the migrations that have been applied to the database. If any new migration is found, it will migrate the database to close the gap.

    $ pyway migrate
