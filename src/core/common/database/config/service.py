from src.core.common.config_service import ConfigService
from src.core.common.database.config.model import DatabaseConfig


class DatabaseConfigService(ConfigService):
    config_key = "DB"

    def get_config(self) -> DatabaseConfig:
        return DatabaseConfig(
            SCHEMA=self.lookup_config("DB_SCHEMA"),
            USER=self.lookup_config("DB_USER"),
            HOST=self.lookup_config("DB_HOST"),
            PORT=self.lookup_config("DB_PORT"),
            PASSWORD=self.lookup_config("DB_PASSWORD"),
        )
