import os
import yaml

from src.core.common.utils import remove_prefix


class ConfigService:
    config_key = ""

    def __init__(self, env: str, file: str = "config.yml"):
        config_file = self.load_config_file(file)
        self.default_config = config_file.get(env, {}).get(self.config_key, {})

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

    def get_config(self):
        pass
