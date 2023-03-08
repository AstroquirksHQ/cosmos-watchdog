import os
import yaml

from src.core.common.api_config import APIConfig
from src.core.common.bot_config import BotConfig
from src.core.common.database.config import DatabaseConfig
from src.core.common.utils import remove_prefix


class Config:
    def __init__(self, env: str, config_key: str, file: str = "config.yml"):
        self.config_key = config_key
        config_file = self.load_config_file(file)
        self.default_config = config_file.get(env, {}).get(config_key, {})

    @staticmethod
    def load_config_file(file: str):
        with open(file, "r") as f:
            config = yaml.safe_load(f)
        return config

    def lookup_config(self, config_name: str):
        return os.environ.get(
            config_name,
            self.default_config.get(remove_prefix(f"{self.config_key}_", config_name)),
        )

    def get_api_config(self) -> APIConfig:
        return APIConfig(
            HOST=self.lookup_config("API_HOST"), PORT=self.lookup_config("API_PORT")
        )

    def get_bot_config(self) -> BotConfig:
        return BotConfig(
            TOKEN=self.lookup_config("BOT_TOKEN"),
            FREQUENCY=self.lookup_config("BOT_FREQUENCY"),
            CHANNEL_ID=self.lookup_config("BOT_CHANNEL_ID"),
        )

    def get_database_config(self) -> DatabaseConfig:
        return DatabaseConfig(
            SCHEMA=self.lookup_config("DB_SCHEMA"),
            USER=self.lookup_config("DB_USER"),
            HOST=self.lookup_config("DB_HOST"),
            PORT=self.lookup_config("DB_PORT"),
            PASSWORD=self.lookup_config("DB_PASSWORD"),
        )
