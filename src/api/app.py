import os

import structlog
from flask import Flask
from retry import retry

from src.core.notifications.model import Notification
from src.core.transactions.model import Transaction
from src.core.common.database.base_model import database_proxy
from .config.model import APIConfig
from .config.service import APIConfigService
from .status.controller import StatusController
from src.core.common.database.context import database_context

BLUEPRINTS = [StatusController.status_routes]
MODELS = [Transaction, Notification]


@database_context
class App(Flask):
    def __init__(self, name):
        super().__init__(name)
        self.logger = structlog.get_logger(__name__).bind(
            service=self.__class__.__name__
        )

        self.init_config()

        self.create_tables()
        self.register_routes()

        self.before_request(self.execute_before_request)
        self.teardown_request(self.execute_teardown_request)

    def init_config(self) -> APIConfig:
        env = os.environ.get("ENV", "PROD")
        self.config.from_object(APIConfigService(env, file="config.yml").get_config())
        self.logger.info("config", **self.config)

    def register_routes(self):
        # Routes registration
        for blueprint in BLUEPRINTS:
            self.register_blueprint(blueprint)

    @retry(delay=5, tries=5)
    def create_tables(self):
        database_proxy.create_tables(MODELS)

    def execute_before_request(self):
        if database_proxy.is_closed():
            database_proxy.connect()

    def execute_teardown_request(self, exc):
        if not database_proxy.is_closed():
            database_proxy.close()


app = App(__name__)
