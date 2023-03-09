import os

import structlog
from retry import retry

from src.core.common.database.base_model import database_proxy
from src.core.common.database.config.service import DatabaseConfigService
from src.core.common.database.service import DatabaseService
from src.core.notifications.model import Notification
from src.core.transactions.model import Transaction

MODELS = [Transaction, Notification]


def database_context(cls):
    class DecoratedClass(cls):
        def __init__(self, *args, **kwargs):
            is_initialized = True
            try:
                database_proxy.database
            except AttributeError:
                is_initialized = False
            if not is_initialized:
                logger = structlog.get_logger(__name__).bind(service=cls.__name__)

                # getting env
                env = os.environ.get("ENV", "PROD")
                logger.info("Environment", env=env)

                # getting config
                db_config = DatabaseConfigService(env, "config.yml").get_config()
                logger.info("Database config", config=db_config)

                # initializing db
                database_service = DatabaseService(db_config)
                database_proxy.initialize(database_service.database)

                self.create_tables()

            # call the original constructor
            super().__init__(*args, **kwargs)

        @retry(delay=5, tries=5)
        def create_tables(self):
            database_proxy.create_tables(MODELS)

    DecoratedClass.__name__ = cls.__name__

    return DecoratedClass
