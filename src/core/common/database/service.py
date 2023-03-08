import structlog
from peewee import PostgresqlDatabase

from src.core.common.database.config.model import DatabaseConfig


class DatabaseService:
    def __init__(self, config: DatabaseConfig):
        self.logger = structlog.get_logger(self.__class__.__name__)
        self.config = config
        self.database = self.init_db()

    def init_db(self) -> PostgresqlDatabase:
        self.logger.info("Connect database", **self.config.to_dict())

        return PostgresqlDatabase(
            self.config.SCHEMA,
            user=self.config.USER,
            password=self.config.PASSWORD,
            host=self.config.HOST,
            port=self.config.PORT,
        )
