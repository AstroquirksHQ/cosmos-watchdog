from dataclasses import dataclass
from enum import Enum


@dataclass
class Stargaze:
    PREFIX = "stars"
    SYMBOL = "STARS"
    MAGNITUDE = 6
    NODE = "https://api-stargaze-ia.cosmosia.notional.ventures"


@dataclass
class Osmosis:
    PREFIX = "osmo"
    SYMBOL = "OSMO"
    MAGNITUDE = 6
    NODE = "https://osmosis-mainnet-rpc.allthatnode.com:1317"


class Currencies(Enum):
    STARGAZE = Stargaze()
    OSMOSIS = Osmosis()
