from src.core.common.config_service import ConfigService
from src.synchronizer.config.model import SynchronizerConfig


class SynchronizerConfigService(ConfigService):
    config_key = "SYNCHRONIZER"

    def get_config(self) -> SynchronizerConfig:
        return SynchronizerConfig(
            FREQUENCY=self.lookup_config("FREQUENCY"),
            VALIDATOR_ADDRESS=self.lookup_config("VALIDATOR_ADDRESS"),
            NOTIFY=self.lookup_config("NOTIFY")
        )
