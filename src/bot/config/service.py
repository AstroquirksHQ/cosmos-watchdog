from src.bot.config.model import BotConfig
from src.core.common.config_service import ConfigService


class BotConfigService(ConfigService):
    config_key = "BOT"

    def get_config(self) -> BotConfig:
        return BotConfig(
            TOKEN=self.lookup_config("BOT_TOKEN"),
            FREQUENCY=self.lookup_config("BOT_FREQUENCY"),
            CHANNEL_ID=self.lookup_config("BOT_CHANNEL_ID"),
        )
