import os
from datetime import datetime
from random import randint

import pytest

from src.core.common.config import Config
from src.core.common.database.base_model import database_proxy
from src.core.common.database.service import DatabaseService
from src.core.notifications.model import Notification
from src.core.transactions.model import Transaction, TransactionType


@pytest.fixture(scope="function", autouse=True)
def db_test():
    env = os.environ.get("ENV", "TEST")
    config = Config(env, "DB").get_database_config()
    db = DatabaseService(config)
    database_proxy.initialize(db.database)
    with database_proxy.atomic():
        Notification.drop_table()
        Transaction.drop_table()
        Transaction.create_table()
        Notification.create_table()

    yield

    with database_proxy.atomic():
        Notification.drop_table()
        Transaction.drop_table()
        Transaction.create_table()
        Notification.create_table()


@pytest.fixture(scope="function")
def populate_db():
    # Create multiple transactions for each transaction type
    for tx_type in TransactionType:
        for i in range(5):
            Transaction.create(
                from_validator=f"Validator{i}",
                validator=f"Validator{i+1}",
                delegator=f"Delegator{i}",
                type=tx_type.value,
                hash=f"Hash{i}",
                height=randint(1, 100),
                amount=randint(1, 100),
                memo=f"Memo{i}",
                timestamp=datetime.now(),
                offset=i,
            )
