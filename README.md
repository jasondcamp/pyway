[![Build Status](https://travis-ci.org/sergiosbx/pyway.svg?branch=master)](https://travis-ci.org/sergiosbx/pyway)


# Pyway Database Version Control
version number: 0.3.0


## Overview
Pyway is a database versioning and migration tool inspired by Flyway


## Download and Install
To install use pip:

    $ pip install pyway

Or clone the repo:

    $ git clone https://github.com/jasondcamp/pyway.git
    $ python setup.py install


## Configuration
#### Pyway environment variables and command line options

| Env Variable | Command Line | Description | Default |
| --------------- | -------------- | -------------- | :--------------: |
| PYWAY_DATABASE_MIGRATION_DIR | --database-migration-dir | Folder name to migration files | resources |
| PYWAY_SQL_MIGRATION_PREFIX | | Prefix for version in migration file | V |
| PYWAY_SQL_MIGRATION_SEPARATOR | | Separator between version and description to the migration file | __ |
| PYWAY_SQL_MIGRATION_SUFFIXES | | Suffix extension for migration files | .sql |
| PYWAY_TABLE | --database-table | Name of schema history table | public.pyway |
| PYWAY_TYPE | --database-type | Data Base Management System [`postgres`, `mysql` ] | *required* |
| PYWAY_DATABASE_HOST | --database-host | Host to connect to the database | localhost |
| PYWAY_DATABASE_PORT | --database-port | Port to connect to the database | 5432 |
| PYWAY_DATABASE_NAME | --database-name | Name of database to connect | postgres |
| PYWAY_DATABASE_USERNAME |--database-username | User to use to connect to the database | postgres |
| PYWAY_DATABASE_PASSWORD | --database-password | Password to use to connect to the database | *None* |
| PYWAY_LOGS_DIR | --logs-dir | Folder name to logs construct | logs |
| | --log-to-file | Log to external file | False |
| PYWAY_CONFIG_FILE | -c, --config | Configuration file | .pyway.conf |

#### Configuration file
Pyway supports a configuration file with the default file as `.pyway.conf`. A sample config file is below:
```
database:
    type: postgres
    username: postgres
    password: 123456
    host: localhost
    port: 5432
    database: postgres
logging:
    logsdir: logs
    logtofile: False
general:
    migrationsdir: schema
    pywaytable: public.pyway
```


## Pyway Files
Files are raw SQL files that are named like the following:

V{major}\_{minor}\_\_{description}.sql

Example: V01_01__initial_schema.sql

Note that the description needs to match the word regexp [A-Za-z0-9_]


## Usage

#### Info
Information lets you know where you are. At first glance, you will see which migrations have already been applied, which others are still pending, and whether there is a discrepancy between the checksum of the local file and the database schema table.

    $ pyway info


#### Validate
Validate helps you verify that the migrations applied to the database match the ones available locally. This compares the checksums to validate that what is in the migration on disk is what was committed into the database.

    $ pyway validate


#### Migrate
After `validate`, it will scan the **Database migration dir** for available migrations. It will compare them to the migrations that have been applied to the database. If any new migration is found, it will migrate the database to close the gap.

    $ pyway migrate
