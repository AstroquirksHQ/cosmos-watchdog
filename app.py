import os

import structlog
from flask import Flask
from retry import retry

from api.synchronization.model import Synchronization
from cli.cli import synchronize
from config import Config
from api.status.controller import StatusController
from api.transactions.model import Transaction
from common.BaseModel import database_proxy
from common.Database import Database

BLUEPRINTS = [StatusController.status_routes]
MODELS = [Transaction, Synchronization]


class App(Flask):
    def __init__(self, name):
        super().__init__(name)
        self.logger = structlog.get_logger(self.__class__.__name__)

        self.init_config()
        self.cli.add_command(synchronize)
        self.db = self.init_db()
        self.create_tables()
        self.register_routes()

        self.before_request(self.execute_before_request)
        self.teardown_request(self.execute_teardown_request)

    def init_config(self):
        env = os.environ.get("ENV", "PROD")
        self.config.from_object(Config(env))
        self.logger.info("config", **self.config)

    def init_db(self):
        db = Database(self.config["DB"])
        database_proxy.initialize(db.db_instance)
        return db

    def register_routes(self):
        # Routes registration
        for blueprint in BLUEPRINTS:
            self.register_blueprint(blueprint)

    @retry(delay=5, tries=5)
    def create_tables(self):
        self.db.db_instance.create_tables(MODELS)

    def execute_before_request(self):
        self.db.connect_db()

    def execute_teardown_request(self, exc):
        self.db.close_db()
