from peewee import CharField

from common.BaseModel import BaseModel


class Transaction(BaseModel):
    hash = CharField()
