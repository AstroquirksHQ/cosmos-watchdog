from src.core.common.config_service import ConfigService
from src.core.common.database.config.model import DatabaseConfig


class DatabaseConfigService(ConfigService):
    config_key = "DB"

    def get_config(self) -> DatabaseConfig:
        return DatabaseConfig(
            SCHEMA=self.lookup_config("SCHEMA"),
            USER=self.lookup_config("USER"),
            HOST=self.lookup_config("HOST"),
            PORT=self.lookup_config("PORT"),
            PASSWORD=self.lookup_config("PASSWORD"),
        )
