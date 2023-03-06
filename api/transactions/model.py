from enum import Enum

from peewee import CharField, IntegerField, BigIntegerField, DoesNotExist

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
        indexes = ((("delegator", "type", "hash"), True),)

    @classmethod
    def get_last_offset_by_type(cls, type: TransactionType) -> int:
        try:
            return (
                cls.select()
                .where(cls.type == type.value)
                .order_by(cls.offset.desc())
                .get()
                .offset
            )
        except DoesNotExist:
            return 0

    @classmethod
    def delete_by_type_from_offset(
        cls, tx_type: TransactionType, from_offset=None
    ) -> int:
        query = cls.delete().where(cls.type == tx_type.value)
        if from_offset is not None:
            query = query.where(cls.offset >= from_offset)
        return query.execute()
