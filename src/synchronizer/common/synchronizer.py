from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Iterator, Tuple, Dict


class TxSynchronizer(ABC):
    @property
    @abstractmethod
    def tx_type(self):
        pass

    @property
    @abstractmethod
    def message_type(self):
        pass

    @property
    @abstractmethod
    def fetch_transactions(self):
        pass

    @abstractmethod
    def parse_transaction(
        self, message: Dict, message_props: Dict, validator_address: str
    ) -> List[Dict]:
        pass

    def fetch_all_txs(
        self, validator_address: str, from_offset: int = 0
    ) -> Iterator[Tuple[List[Dict], int]]:
        offset = from_offset
        while True:
            resp_json = self.fetch_transactions(validator_address, offset=offset)
            yield resp_json["tx_responses"], offset
            offset += len(resp_json["tx_responses"])
            if offset >= int(resp_json["pagination"]["total"]):
                break

    def extract_transactions(
        self,
        node_transactions: List[Dict],
        offset: int,
        validator_address: str,
    ) -> List[Dict]:
        transactions = []
        for tx in node_transactions:
            message_props = {
                "height": tx["height"],
                "hash": tx["txhash"],
                "memo": tx["tx"]["body"]["memo"],
                "timestamp": datetime.strptime(tx["timestamp"], "%Y-%m-%dT%H:%M:%SZ"),
                "offset": int(offset),
            }
            for message in tx["tx"]["body"]["messages"]:
                transactions += self.parse_transaction(
                    message, message_props, validator_address
                )
            offset += 1
        return transactions
