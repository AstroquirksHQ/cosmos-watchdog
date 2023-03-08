import datetime


def utc_now():
    return datetime.datetime.utcnow()


def remove_prefix(prefix: str, value: str):
    len_prefix = len(prefix)
    return value[len_prefix:]
