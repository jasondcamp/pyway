from pydbwrapper import Database as Datasource, Config


CREATE_VERSION_MIGRATIONS = "create table if not exists %s ("\
    "installed_rank serial PRIMARY KEY,"\
    "version varchar(20) NOT NULL,"\
    "extension varchar(20) NOT NULL,"\
    "name varchar(125) NOT NULL,"\
    "checksum varchar(25) NOT NULL"\
    ");"
SELECT_FIELDS = ("version", "extension", "name", "checksum")
ORDER_BY_FIELD_ASC = "installed_rank"
ORDER_BY_FIELD_DESC = "installed_rank desc"
INSERT_VERSION_MIGRATE = "insert into %s (version, extension, name, checksum) values (%s, %s, %s, %s);"


class Postgres():

    def __init__(self, config):
        self.config = config
        self.version_table = config.TABLE
        self.create_version_table_if_not_exists()

    def connect(self):
        return Datasource(Config(config_dict={
            "host": self.config.DATABASE_URL,
            "port": self.config.DATABASE_PORT,
            "dbname": self.config.DATABASE_NAME,
            "user": self.config.DATABASE_USERNAME,
            "password": self.config.DATABASE_PASSWORD,
            "connect_timeout": int(self.config.DATABASE_CONNECT_TIMEOUT),
            "maxconnections": int(self.config.DATABASE_MAX_CONNECTIONS)
        }))

    def create_version_table_if_not_exists(self):
        self.execute(CREATE_VERSION_MIGRATIONS % self.version_table)

    def execute(self, scipt):
        with self.connect() as db:
            db.execute(scipt, None, True)

    def get_all_schema_migrations(self):
        with self.connect() as db:
            return db.select(self.version_table)\
                .fields(*SELECT_FIELDS)\
                .order_by(ORDER_BY_FIELD_ASC).execute().fetchall()

    def upgrade_version(self, migration):
        with self.connect() as db:
            db.insert(self.version_table).setall(migration.__dict__).execute()

    def get_max_version(self):
        with self.connect() as db:
            fetched = db.select(self.version_table).fields("version").order_by(ORDER_BY_FIELD_DESC)\
                .execute().fetchone()
            return int(fetched.version) if fetched is not None else 0
