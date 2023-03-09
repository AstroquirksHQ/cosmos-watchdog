from src.bot.config.model import BotConfig
from src.core.common.config_service import ConfigService


class BotConfigService(ConfigService):
    config_key = "BOT"

    def get_config(self) -> BotConfig:
        return BotConfig(
            TOKEN=self.lookup_config("TOKEN"),
            FREQUENCY=self.lookup_config("FREQUENCY"),
            CHANNEL_ID=self.lookup_config("CHANNEL_ID"),
        )
