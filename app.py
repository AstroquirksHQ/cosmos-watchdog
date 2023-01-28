from dotenv import load_dotenv
from flask import Flask

from config import Config
from api.status.controller import StatusController
from api.transactions.model import Transaction
from common.BaseModel import database_proxy
from common.Database import Database

BLUEPRINTS = [StatusController.status_routes]
MODELS = [Transaction]


class App(Flask):
    def __init__(self, name):
        super().__init__(name)
        load_dotenv()
        self.config.from_object(Config)
        self.db = self.init_db()
        self.create_tables()
        self.register_routes()

        self.before_request(self.execute_before_request)
        self.teardown_request(self.execute_teardown_request)

    def init_db(self):
        db = Database(self.config["DATABASE"])
        database_proxy.initialize(db.db_instance)
        return db

    def register_routes(self):
        # Routes registration
        for blueprint in BLUEPRINTS:
            self.register_blueprint(blueprint)

    def create_tables(self):
        self.db.db_instance.create_tables(MODELS)

    def execute_before_request(self):
        self.db.connect_db()

    def execute_teardown_request(self, exc):
        self.db.close_db()
