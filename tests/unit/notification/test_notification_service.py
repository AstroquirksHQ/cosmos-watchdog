from api.notifications.model import Notification


def test_new_notifications(populate_db, notification_service):
    tx_ids = range(1, 6)
    new_entries = notification_service.new_notifications_for_tx_ids(tx_ids)
    assert len(new_entries) == len(tx_ids)

    # verify entries were saved in database
    saved_tx = Notification.select().where(Notification.id.in_(new_entries))
    assert saved_tx.count() == len(tx_ids)
