from dataclasses import dataclass


@dataclass
class APIConfig:
    HOST: str
    PORT: str

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self) -> dict:
        return {
            "HOST": self.HOST,
            "PORT": self.PORT,
        }
