from dataclasses import dataclass
from typing import Dict


@dataclass
class BotConfig:
    TOKEN: str
    FREQUENCY: int
    CHANNEL_ID: int

    def to_dict(self) -> Dict:
        return {
            "TOKEN": "***",
            "FREQUENCY": self.FREQUENCY,
            "CHANNEL_ID": self.CHANNEL_ID,
        }
