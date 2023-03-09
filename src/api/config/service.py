from src.api.config.model import APIConfig
from src.core.common.config_service import ConfigService


class APIConfigService(ConfigService):
    config_key = "API"

    def get_config(self) -> APIConfig:
        return APIConfig(
            HOST=self.lookup_config("HOST"),
            PORT=self.lookup_config("PORT"),
        )
