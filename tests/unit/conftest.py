import pytest

from src.core.notifications.service import NotificationService
from src.core.transactions.service import TransactionService
from src.synchronizer.service import SynchronizationService


@pytest.fixture
def synchronization_service():
    return SynchronizationService("validator_address")


@pytest.fixture
def transaction_service():
    return TransactionService()


@pytest.fixture
def notification_service():
    return NotificationService()
