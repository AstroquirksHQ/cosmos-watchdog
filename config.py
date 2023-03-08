import os
import yaml

from common.DatabaseConfig import DatabaseConfig


class Config:
    def __init__(self, env: str, file: str = "config.yml"):
        config_file = self.load_config_file(file)
        self.default_config = config_file.get(env, {})
        self.DB = DatabaseConfig(
            SCHEMA=self.lookup_config("DB_SCHEMA"),
            USER=self.lookup_config("DB_USER"),
            HOST=self.lookup_config("DB_HOST"),
            PORT=self.lookup_config("DB_PORT"),
            PASSWORD=self.lookup_config("DB_PASSWORD"),
        )
        self.HOST = self.lookup_config("HOST")
        self.PORT = self.lookup_config("PORT")
        self.DISCORD_TOKEN = self.lookup_config("DISCORD_TOKEN")

    @staticmethod
    def load_config_file(file: str):
        with open(file, "r") as f:
            config = yaml.safe_load(f)
        return config

    def lookup_config(self, config_name: str):
        return os.environ.get(config_name, self.default_config.get(config_name))
