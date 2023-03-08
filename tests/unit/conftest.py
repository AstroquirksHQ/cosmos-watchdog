from datetime import datetime
from random import randint

import pytest

from api.notifications.model import Notification
from api.notifications.service import NotificationService
from api.synchronization.service import SynchronizationService
from api.transactions.model import TransactionType, Transaction
from api.transactions.service import TransactionService
from run import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def synchronization_service():
    return SynchronizationService("validator_address")


@pytest.fixture
def transaction_service():
    return TransactionService()


@pytest.fixture
def notification_service():
    return NotificationService()


@pytest.fixture(scope="function", autouse=True)
def db_test():
    with app.db.db_instance.atomic():
        Notification.drop_table()
        Transaction.drop_table()
        Transaction.create_table()
        Notification.create_table()

    with app.app_context():
        yield

    with app.db.db_instance.atomic():
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
