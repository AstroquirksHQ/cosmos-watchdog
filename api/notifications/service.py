import structlog

from api.notifications.model import Notification


class NotificationService:
    def __init__(self):
        self.logger = structlog.get_logger(__name__)

    def get_pending_notifications(self) -> list[Notification]:
        all_notifications = Notification.get_pending()
        self.logger.info(f"Found {len(all_notifications)} notifications to send !")
        return all_notifications

    def mark_as_sent(self, notification: Notification):
        notification.to_sent()
        self.logger.info(f"Notification for tx ({notification.transaction}) sent !")

    def new_notifications(self, new_transactions_ids: list[int]):
        new_entries = (
            Notification.insert_many(
                [{"transaction_id": tx_id} for tx_id in new_transactions_ids]
            )
            .returning(Notification.id)
            .on_conflict_ignore()
            .execute()
        )
        self.logger.info(
            f"Saved {len(new_entries) if new_entries else 0} new notifications !"
        )
        return new_entries
