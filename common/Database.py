import structlog
from peewee import PostgresqlDatabase

from common.DatabaseConfig import DatabaseConfig


class Database:
    def __init__(self, config: DatabaseConfig):
        self.logger = structlog.get_logger(self.__class__.__name__)
        self.config = config
        self.db_instance = self.init_db()

    def init_db(self) -> PostgresqlDatabase:
        self.logger.info("Connect database", **self.config.to_dict())

        return PostgresqlDatabase(
            self.config.SCHEMA,
            user=self.config.USER,
            password=self.config.PASSWORD,
            host=self.config.HOST,
            port=self.config.PORT,
        )

    def connect_db(self):
        if self.db_instance.is_closed():
            self.db_instance.connect()

    def close_db(self):
        if not self.db_instance.is_closed():
            self.db_instance.close()
