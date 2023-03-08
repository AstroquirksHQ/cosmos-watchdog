from peewee import Model, AutoField, Proxy
from playhouse.postgres_ext import DateTimeTZField

from src.core.common.utils import utc_now

database_proxy = Proxy()


class BaseModel(Model):
    id = AutoField()
    created_on = DateTimeTZField(default=utc_now)
    updated_on = DateTimeTZField(default=utc_now)

    class Meta:
        database = database_proxy

    def save(self, *args, **kwargs):
        self.updated_on = utc_now()
        return super().save(*args, **kwargs)
