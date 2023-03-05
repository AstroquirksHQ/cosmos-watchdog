from typing import Optional

from peewee import CharField, IntegerField, DoesNotExist

from api.transactions.model import TransactionType
from common.BaseModel import BaseModel


class Synchronization(BaseModel):
    type = CharField(choices=[type.value for type in TransactionType])
    offset = IntegerField()

    @staticmethod
    def get_last_offset_by_type(type: TransactionType) -> int:
        try:
            return (
                Synchronization.select()
                .where(Synchronization.type == type.value)
                .order_by(Synchronization.offset.desc())
                .get().offset
            )
        except DoesNotExist:
            return 0
