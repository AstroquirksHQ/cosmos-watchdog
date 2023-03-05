from enum import Enum

from peewee import CharField, IntegerField, BigIntegerField, Check, DoesNotExist

from common.BaseModel import BaseModel


class TransactionType(Enum):
    RESTAKE = "RESTAKE"
    DELEGATE = "DELEGATE"
    UNDELEGATE = "UNDELEGATE"
    REDELEGATE = "REDELEGATE"
    UNREDELEGATE = "UNREDELEGATE"


class Transaction(BaseModel):
    from_validator = CharField(null=True)
    validator = CharField()
    delegator = CharField()
    type = CharField(choices=[type.value for type in TransactionType])
    hash = CharField()
    height = IntegerField()
    amount = BigIntegerField()
    memo = CharField()
    timestamp = CharField()
    offset = IntegerField()

    class Meta:
        indexes = (
            (('delegator', 'type', 'hash'), True),
        )

    @staticmethod
    def get_last_offset_by_type(type: TransactionType) -> int:
        try:
            return (
                Transaction.select()
                .where(Transaction.type == type.value)
                .order_by(Transaction.offset.desc())
                .get().offset
            )
        except DoesNotExist:
            return 0
