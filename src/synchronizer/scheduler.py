import asyncio
import os

import structlog

from src.core.transactions.model import TransactionType
from src.synchronizer.config.model import SynchronizerConfig
from src.synchronizer.config.service import SynchronizerConfigService
from src.synchronizer.service import SynchronizationService


class BackgroundTxSynchronizer:
    def __init__(self):
        self.logger = structlog.get_logger(__name__).bind(
            service=self.__class__.__name__
        )
        self.loop = asyncio.get_event_loop()
        self.config = self.init_config()
        self.service = SynchronizationService(self.config.VALIDATOR_ADDRESS)

    def init_config(self) -> SynchronizerConfig:
        env = os.environ.get("ENV", "PROD")
        config = SynchronizerConfigService(env, file="config.yml").get_config()
        self.logger.info("config", **config.to_dict())
        return config

    async def _background_run(self, tx_type: TransactionType):
        while True:
            self.logger.info(
                f"[{tx_type.value}] Running synchronization ...", tx_type=tx_type.value
            )
            self.service.synchronize_by_type(tx_type, notify=False)
            self.logger.info(
                f"[{tx_type.value}] sleeping {self.config.FREQUENCY} seconds ...",
                tx_type=tx_type.value,
            )
            await asyncio.sleep(self.config.FREQUENCY)

    def start(self):
        tasks = [
            self.loop.create_task(self._background_run(tx_type))
            for tx_type in TransactionType
        ]
        self.loop.run_until_complete(asyncio.gather(*tasks))
