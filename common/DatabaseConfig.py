from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    SCHEMA: str
    USER: str
    HOST: str
    PORT: str
    PASSWORD: str

    def to_dict(self):
        return {
            "SCHEMA": self.SCHEMA,
            "HOST": self.HOST,
            "PORT": self.PORT,
            "USER": self.USER,
            "PASSWORD": "****",
        }
