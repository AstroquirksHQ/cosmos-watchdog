from enum import Enum

from peewee import ForeignKeyField, CharField

from api.transactions.model import Transaction
from common.BaseModel import BaseModel


class NotificationStatus(Enum):
    PENDING = "PENDING"
    SENT = "SENT"


class Notification(BaseModel):
    transaction = ForeignKeyField(Transaction, on_delete="CASCADE")
    status = CharField(default=NotificationStatus.PENDING.value)

    @classmethod
    def get_pending(cls):
        return cls.select().where(cls.status == NotificationStatus.PENDING.value)

    def to_sent(self):
        self.status = NotificationStatus.SENT.value
        self.save()
