from dataclasses import dataclass


@dataclass
class SynchronizerConfig:
    FREQUENCY: int
    VALIDATOR_ADDRESS: str
    NOTIFY: bool

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self) -> dict:
        return {
            "FREQUENCY": self.FREQUENCY,
            "VALIDATOR_ADDRESS": self.VALIDATOR_ADDRESS,
            "NOTIFY": self.NOTIFY,
        }
