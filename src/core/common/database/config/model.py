from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    SCHEMA: str
    USER: str
    HOST: str
    PORT: str
    PASSWORD: str

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self) -> dict:
        return {
            "SCHEMA": self.SCHEMA,
            "HOST": self.HOST,
            "PORT": self.PORT,
            "USER": self.USER,
            "PASSWORD": "****",
        }
