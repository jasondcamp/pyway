import psycopg2
from pyway.migration import Migration


CREATE_VERSION_MIGRATIONS = "create table if not exists %s ("\
    "id serial PRIMARY KEY,"\
    "version varchar(20) NOT NULL,"\
    "extension varchar(20) NOT NULL,"\
    "name varchar(125) NOT NULL,"\
    "checksum varchar(25) NOT NULL,"\
    "date_applied_utc timestamp DEFAULT CURRENT_TIMESTAMP"\
    ");"
SELECT_FIELDS = ("version", "extension", "name", "checksum", "date_applied_utc")
ORDER_BY_FIELD_ASC = "id"
ORDER_BY_FIELD_DESC = "id desc"
INSERT_VERSION_MIGRATE = "insert into %s (version, extension, name, checksum) values ('%s', '%s', '%s', '%s');"

CREATE_SCHEMA_TEMPLATE = "create schema if not exists %s"


class Postgres:

    def __init__(self, args):
        self.args = args
        self.version_table = args.database_table
        self.schemas = args.schemas.split(',') if args.schemas else []
        self.default_schema = args.default_schema if args.default_schema else self.schemas[0] if len(self.schemas) \
            else ''
        self.default_database = args.database_name if args.database_name else ''
        if not self.default_schema:
            raise Exception(
                'Either both default schema and schemas list is not provided or database_name property is not provided')
        if self.args.create_schema:
            self.create_schema_if_not_exists(self.default_schema)
        self.create_version_table_if_not_exists()

    def connect(self, database_name: str = None, schema_name: str = None):
        return psycopg2.connect(dbname=database_name if database_name else self.default_database,
                                user=self.args.database_username,
                                host=self.args.database_host, password=self.args.database_password,
                                port=self.args.database_port,
                                options=f"-c search_path={schema_name if schema_name else self.default_schema}")

    def create_version_table_if_not_exists(self):
        self.execute(CREATE_VERSION_MIGRATIONS % self.version_table, schema_name=self.default_schema)

    def execute(self, script, database_name: str = None, schema_name: str = None):
        conn = self.connect(database_name, schema_name)
        cur = conn.cursor()
        cur.execute(script)
        conn.commit()

    def get_all_schema_migrations(self):
        cnx = self.connect()
        cursor = cnx.cursor()
        cursor.execute(f"SELECT {','.join(SELECT_FIELDS)} FROM {self.version_table} ORDER BY {ORDER_BY_FIELD_ASC}")
        migrations = []
        for row in cursor.fetchall():
            migrations.append(Migration(row[0], row[1], row[2], row[3], row[4]))
        cursor.close()
        cnx.close()
        return migrations

    def upgrade_version(self, migration):
        self.execute(INSERT_VERSION_MIGRATE % (self.version_table, migration.version,
                                               migration.extension, migration.name,
                                               migration.checksum))

    def create_schema_if_not_exists(self, schema_name):
        self.execute(CREATE_SCHEMA_TEMPLATE % schema_name)

    def get_all_schemas(self):
        try:
            cnx = self.connect()
            cursor = cnx.cursor()
            env_prefix = self.args.ms_env.replace("-", "_")
            cursor.execute(f"SELECT table_schema FROM information_schema.tables where table_schema "
                           f"like '{env_prefix}%' group by table_schema")
            schemas = []
            for row in cursor.fetchall():
                schemas.append(row[0])
            cursor.close()
            cnx.close()
            return schemas
        except Exception as ex:
            print(f"Exception while building schemas list.")
            import traceback
            traceback.print_exc()
            raise ex
