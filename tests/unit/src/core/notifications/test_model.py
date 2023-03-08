from src.core.notifications.model import Notification, NotificationStatus
from src.core.transactions.model import Transaction


def test_get_pending(populate_db):
    # Create 2 notifications, one pending and one sent
    Notification.create(
        transaction=Transaction.get_by_id(1), status=NotificationStatus.PENDING.value
    )
    Notification.create(
        transaction=Transaction.get_by_id(2), status=NotificationStatus.SENT.value
    )

    # Ensure only the pending notification is returned
    assert Notification.get_pending().count() == 1
    assert Notification.get_pending().first().transaction == Transaction.get_by_id(1)


def test_to_sent(populate_db):
    # Create a notification and set its status to SENT
    notification = Notification.create(
        transaction=Transaction.get_by_id(1), status=NotificationStatus.PENDING.value
    )

    notification.to_sent()

    # Ensure the status was changed and the notification was saved
    assert notification.status == NotificationStatus.SENT.value
