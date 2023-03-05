from typing import Callable, List, Dict, Any



class TransactionService:
    def __init__(self, validator_address: str):
        ...
    #
    # def compute_delegate_txs(self, address: str) -> Dict[str, Dict[str, Any]]:
    #     print(f"Fetching all delegate tx for {address}")
    #     txs = self.fetch_all_txs(address, self.client.get_delegate_txs)
    #     addresses, total_amount = self.parse_delegate_txs(txs, address)
    #     print(f"total addresses delegate {len(addresses.keys())}")
    #     print(f"total delegated {total_amount}")
    #     return addresses
