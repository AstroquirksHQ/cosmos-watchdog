import os

from common.DatabaseConfig import DatabaseConfig


class Config:
    DATABASE = DatabaseConfig(
        SCHEMA=os.environ.get("DB_SCHEMA"),
        USER=os.environ.get("DB_USER"),
        HOST=os.environ.get("DB_HOST"),
        PORT=os.environ.get("DB_PORT"),
        PASSWORD=os.environ.get("DB_PASSWORD"),
    )
    HOST = os.environ.get("HOST")
    PORT = os.environ.get("PORT")
