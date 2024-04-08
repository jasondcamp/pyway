# Pyway Database Version Control
![](https://img.shields.io/pypi/v/pyway.svg) ![](https://img.shields.io/badge/status-beta-yellow) ![](https://github.com/jasondcamp/pyway/actions/workflows/pyway-test.yml/badge.svg)  ![](https://img.shields.io/pypi/pyversions/pyway.svg) ![](https://img.shields.io/badge/license-GPL-lightgrey)

![](https://api.codeclimate.com/v1/badges/6ad7c702ffb0b1b96c1a/maintainability) ![](https://api.codeclimate.com/v1/badges/6ad7c702ffb0b1b96c1a/test_coverage)

## Overview
Pyway is a database versioning and migration tool inspired by Flyway

## Supported Databases
- MySQLd Commercial (Version 8+)
- MariaDB (Version 10+)
- PostgreSQL
- DuckDB (Version 0.10+)

## Download and Install
To install use pip:

    $ pip install pyway

Or clone the repo:

    $ git clone https://github.com/jasondcamp/pyway.git
    $ python -m build

## Configuration
#### Pyway environment variables and command line options

Priority is `env variables` -> `config file` -> `command args`

| Env Variable | Command Line | Description | Default |
| --------------- | -------------- | -------------- | :--------------: |
| PYWAY_DATABASE_MIGRATION_DIR | --database-migration-dir | Folder name to migration files | resources |
| PYWAY_SQL_MIGRATION_PREFIX | | Prefix for version in migration file | V |
| PYWAY_SQL_MIGRATION_SEPARATOR | | Separator between version and description to the migration file | __ |
| PYWAY_SQL_MIGRATION_SUFFIXES | | Suffix extension for migration files | .sql |
| PYWAY_TABLE | --database-table | Name of schema history table | *None* |
| PYWAY_TYPE | --database-type | Data Base Management System [`postgres`, `mysql`, `duckdb` ] | *None* *required* |
| PYWAY_DATABASE_HOST | --database-host | Host to connect to the database | *None* |
| PYWAY_DATABASE_PORT | --database-port | Port to connect to the database | *None* |
| PYWAY_DATABASE_NAME | --database-name | Name of database to connect | *None* |
| PYWAY_DATABASE_USERNAME |--database-username | User to use to connect to the database | *None* |
| PYWAY_DATABASE_PASSWORD | --database-password | Password to use to connect to the database | *None* |
| PYWAY_CONFIG_FILE | -c, --config | Configuration file | .pyway.conf |
| | --schema-file | Used when importing a schema file | |
| | --checksum-file | Used when updating a checksum - *advanced use*! | |

#### Configuration file
Pyway supports a configuration file with the default file as `.pyway.conf`. A sample config file is below:

_Postgres:_
```
database_type: postgres
database_username: postgres
database_password: 123456
database_host: localhost
database_port: 5432
database_name: postgres
database_migration_dir: schema
database_table: public.pyway
```
_MySQL:_
```
database_type: mysql
database_username: admin
database_password: 123456
database_host: localhost
database_port: 3306
database_name: maindb
database_migration_dir: schema
database_table: pyway
```


## Pyway Files
Files are raw SQL files that are named like the following. Major/minor versioning and semantic versioning is supported.

V{major}\_{minor}\_({patch})\_\_{description}.sql

Example: V01_01__initial_schema.sql

Example: V01_01_01__initial_schema.sql

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

#### Import
This allows the user to import a schema file into the migration, for example if the base schema has already been applied, then the user can import that file in so they can then apply subsequent migrations. Currently the import looks in the `database_migration_dir` for the file.

    $ pyway import --schema-file V01_01__initial_schema.sql

#### Checksum
Updates a checksum in the database. This is for advanced use only, as it could put the pyway database out of sync with reality.  This is mainly to be used for development, where your pyway file may change because of manual applies or formatting changes. It is meant to get the database in sync with what you believe to be the current state of your system. It should NEVER be used in production, only initial development. If you require schema changes in production, create a new schema and apply that.

    $ pyway checksum --checksum-file V01_01__initial_schema.sql
