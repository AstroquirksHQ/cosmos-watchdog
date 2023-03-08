import structlog
from peewee import IntegrityError

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

    def new_notifications_for_tx_ids(self, transactions_ids: list[int]):
        new_entries = []
        for id in transactions_ids:
            try:
                notif = Notification(transaction=id)
                notif.save()
                new_entries.append(notif.id)
            except IntegrityError:
                self.logger.debug(
                    f"The Notification already exist for transaction ({id})"
                )
                pass
        self.logger.info(f"Saved {len(new_entries)} new notifications !")
        return new_entries
