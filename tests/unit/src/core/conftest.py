import os
import secrets
from datetime import datetime
from random import randint

import pytest

from src.core.common.database.base_model import database_proxy
from src.core.common.database.config.service import DatabaseConfigService
from src.core.common.database.service import DatabaseService
from src.core.notifications.model import Notification
from src.core.transactions.model import Transaction, TransactionType


@pytest.fixture(scope="function", autouse=True)
def db_connection():
    env = os.environ.get("ENV", "TEST")
    config = DatabaseConfigService(env, file="config.yml").get_config()
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
                from_validator=f"Validator{i}-{secrets.token_hex(16)}",
                validator=f"Validator{i+1}-{secrets.token_hex(16)}",
                delegator=f"Delegator{i}-{secrets.token_hex(16)}",
                type=tx_type.value,
                hash=f"Hash{i}-{secrets.token_hex(16)}",
                height=randint(1, 100000),
                amount=randint(100000, 10000000000),
                memo=f"Memo{i} - Test-Integration : {secrets.token_hex(16)}",
                timestamp=datetime.now(),
                offset=i,
            )
