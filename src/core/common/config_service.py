import os
import yaml


class ConfigService:
    config_key = ""

    def __init__(self, env: str, file: str = "config.yml"):
        config_file = self.load_config_file(file)
        self.default_config = config_file.get(env, {}).get(self.config_key, {})

    @classmethod
    def prefixed(cls, value: str) -> str:
        return f"{cls.config_key}_{value}"

    @staticmethod
    def load_config_file(file: str):
        with open(file, "r") as f:
            config = yaml.safe_load(f)
        return config

    def lookup_config(self, config_name: str):
        return os.environ.get(
            self.prefixed(config_name), self.default_config.get(config_name)
        )

    def get_config(self):
        raise NotImplementedError
