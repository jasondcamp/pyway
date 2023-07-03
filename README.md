# Pyway Database Version Control
![](https://img.shields.io/pypi/v/pyway.svg) ![](https://img.shields.io/badge/status-beta-yellow) ![](https://github.com/jasondcamp/pyway/actions/workflows/pyway-test.yml/badge.svg)  ![](https://img.shields.io/pypi/pyversions/pyway.svg) ![](https://img.shields.io/badge/license-GPL-lightgrey)

![](https://api.codeclimate.com/v1/badges/6ad7c702ffb0b1b96c1a/maintainability) ![](https://api.codeclimate.com/v1/badges/6ad7c702ffb0b1b96c1a/test_coverage)

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

Priority is `env variables` -> `config file` -> `command args`

| Env Variable                             | Command Line                         | Description                                                                                                                            |      Default       |
|------------------------------------------|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|:------------------:|
| PYWAY_DATABASE_MIGRATION_DIR             | --database-migration-dir             | Folder name to migration files                                                                                                         |     resources      |
| PYWAY_SQL_MIGRATION_PREFIX               |                                      | Prefix for version in migration file                                                                                                   |         V          |
| PYWAY_SQL_MIGRATION_SEPARATOR            |                                      | Separator between version and description to the migration file                                                                        |         __         |
| PYWAY_SQL_MIGRATION_SUFFIXES             |                                      | Suffix extension for migration files                                                                                                   |        .sql        |
| PYWAY_DEFAULT_SCHEMA                     | --default-schema                     | Name of the default schema to store history table                                                                                      |       public       |
| PYWAY_CREATE_SCHEMA                      | --create-schema                      | Boolean flag to check and create schema if not exists                                                                                  |         1          |
| PYWAY_DATABASE_TABLE                     | --database-table                     | Name of the history table                                                                                                              |       pyway        |
| PYWAY_DATABASE_TABLE                     | --database-table                     | Name of the history table                                                                                                              |       pyway        |
| PYWAY_RUN_MIGRATION_ON_DEFAULT_SCHEMA    | --run-migration-on-default-schema    | If you want to exclude default schema from migration set this to 0                                                                     |         1          |
| PYWAY_DATABASE_HOST                      | --database-host                      | Host to connect to the database                                                                                                        |     localhost      |
| PYWAY_DATABASE_PORT                      | --database-port                      | Port to connect to the database                                                                                                        |        5432        |
| PYWAY_DATABASE_NAME                      | --database-name                      | Name of database to connect                                                                                                            |      postgres      |
| PYWAY_DATABASE_USERNAME                  | --database-username                  | User to use to connect to the database                                                                                                 |      postgres      |
| PYWAY_DATABASE_PASSWORD                  | --database-password                  | Password to use to connect to the database                                                                                             |       *None*       |
| PYWAY_CONFIG_FILE                        | -c, --config                         | Configuration file                                                                                                                     |    .pyway.conf     |
|                                          | --schema-file                        | Used when importing a schema file                                                                                                      |                    |
| PYWAY_RUN_MIGRATION_ON_ALL_SCHEMAS_IN_DB | --run-migration-on-all-schemas-in-db | Set this to 1 if you want to run migration on all schemas in connected DB. You must pass ms_env variable to fetch schemas with prefix. |         0          |
| PYWAY_MS_ENV                             | --ms-env                             | Schema prefix to check for list of schemas to execture migration on                                                                    |        dev         |
| PYWAY_SCHEMAS                            | --schemas                            | List of schemas to execute migration on when you don't want to run migration on all schemas in db                                      | schema_1, schema_2 |

#### Configuration file
Pyway supports a configuration file with the default file as `.pyway.conf`. A sample config file is below:
```
database_type: postgres
database_username: postgres
database_password: 123456
database_host: localhost
database_port: 5432
database_database: postgres
database_migration_dir: schema
database_table: pyway
default_schema: public
create_schema: 1
run_migration_on_default_schema: 0
fail_migration_on_at_least_one_schema_failure: 0
schemas: schema_1, schema_2
run_migration_on_all_schemas_in_db: 1
MS_ENV: dev

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

#### Import
This allows the user to import a schema file into the migration, for example if the base schema has already been applied, then the user can import that file in so they can then apply subsequent migrations.

    $ pyway import --schema-file V01_01__initial_schema.sql

