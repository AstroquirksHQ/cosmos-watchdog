from typing import Callable, List, Dict, Any

from flask import current_app

from api.cosmos_client.cosmos_client import CosmosClient
from api.transactions.model import TransactionType, Transaction
from api.transactions.service import TransactionService


class SynchronizationService:
    PAGE_SIZE = 100

    def __init__(self, validator_address: str):
        self.logger = current_app.logger
        self.validator_address = validator_address
        self.restake_address = "osmo1ctfwwaxgwu4u45wvzxe5cky2zw8k9t6qt95hhn"
        self.cosmos_client = CosmosClient()
        self.transaction_service = TransactionService()

    def fetch_all_txs(
        self,
        address: str,
        fetch_function: Callable,
        callback: Callable,
        from_offset: int = 0,
    ):
        offset = from_offset
        while True:
            resp_json = fetch_function(address, offset=offset)
            callback(resp_json["tx_responses"], offset)
            offset += len(resp_json["tx_responses"])
            if offset >= int(resp_json["pagination"]["total"]):
                break

    def extract_transactions(
        self, node_transactions: List[Dict[str, Any]], offset: int
    ) -> List[Dict]:
        transactions = []
        for tx in node_transactions:
            tx_hash = tx["txhash"]
            height = tx["height"]
            timestamp = tx["timestamp"]
            memo = tx["tx"]["body"]["memo"]
            for message in tx["tx"]["body"]["messages"]:
                if (
                    message["@type"] == "/cosmos.staking.v1beta1.MsgDelegate"
                    and message["validator_address"] == self.validator_address
                ):
                    transactions.append(
                        {
                            "validator": message["validator_address"],
                            "delegator": message["delegator_address"],
                            "amount": int(message["amount"]["amount"]),
                            "hash": tx_hash,
                            "height": height,
                            "type": TransactionType.DELEGATE.value,
                            "memo": memo,
                            "timestamp": timestamp,
                            "offset": int(offset),
                        }
                    )
                elif message[
                    "@type"
                ] == "/cosmos.staking.v1beta1.MsgBeginRedelegate" and (
                    message["validator_dst_address"] == self.validator_address
                    or message["validator_src_address"] == self.validator_address
                ):
                    transactions.append(
                        {
                            "from_validator": message["validator_src_address"],
                            "validator": message["validator_dst_address"],
                            "delegator": message["delegator_address"],
                            "amount": int(message["amount"]["amount"]),
                            "hash": tx_hash,
                            "height": height,
                            "type": TransactionType.REDELEGATE.value
                            if message["validator_dst_address"]
                            == self.validator_address
                            else TransactionType.UNREDELEGATE.value,
                            "memo": memo,
                            "timestamp": timestamp,
                            "offset": int(offset),
                        }
                    )
                elif (
                    message["@type"] == "/cosmos.authz.v1beta1.MsgExec"
                    and message["grantee"] == self.restake_address
                ):
                    for msg in message["msgs"]:
                        if (
                            msg["@type"] == "/cosmos.staking.v1beta1.MsgDelegate"
                            and msg["validator_address"] == self.validator_address
                        ):
                            transactions.append(
                                {
                                    "validator": msg["validator_address"],
                                    "delegator": msg["delegator_address"],
                                    "amount": int(msg["amount"]["amount"]),
                                    "hash": tx_hash,
                                    "height": height,
                                    "type": TransactionType.RESTAKE.value,
                                    "memo": memo,
                                    "timestamp": timestamp,
                                    "offset": int(offset),
                                }
                            )
                elif (
                    message["@type"] == "/cosmos.staking.v1beta1.MsgUndelegate"
                    and message["validator_address"] == self.validator_address
                ):
                    transactions.append(
                        {
                            "validator": message["validator_address"],
                            "delegator": message["delegator_address"],
                            "amount": int(message["amount"]["amount"]),
                            "hash": tx_hash,
                            "height": height,
                            "type": TransactionType.UNDELEGATE.value,
                            "memo": memo,
                            "timestamp": timestamp,
                            "offset": int(offset),
                        }
                    )
            offset += 1
        return transactions

    def extract_and_save_txs(self, node_transactions: list, offset: int):
        transactions = self.extract_transactions(node_transactions, offset)
        self.logger.info(f"Found {len(transactions)} transactions from offset {offset}")
        if transactions:
            self.transaction_service.save_many(transactions)

    def synchronize(self, tx_type: TransactionType, fetch_function: Callable):
        self.logger.info(f"[{tx_type.value}] - Synchronizing transactions ...")
        last_offset = Transaction.get_last_offset_by_type(tx_type)
        self.logger.info(f"[{tx_type.value}] - Last offset seen : {last_offset}")
        page_offset = int(last_offset / self.PAGE_SIZE) * self.PAGE_SIZE
        self.fetch_all_txs(
            self.validator_address,
            fetch_function=fetch_function,
            callback=self.extract_and_save_txs,
            from_offset=page_offset,
        )

    def synchronize_delegate(self):
        self.synchronize(
            TransactionType.DELEGATE, fetch_function=self.cosmos_client.get_delegate_txs
        )

    def synchronize_undelegate(self):
        self.synchronize(
            TransactionType.UNDELEGATE,
            fetch_function=self.cosmos_client.get_undelegate_txs,
        )

    def synchronize_redelegate(self):
        self.synchronize(
            TransactionType.REDELEGATE,
            fetch_function=self.cosmos_client.get_redelegate_txs,
        )

    def synchronize_unredelegate(self):
        self.synchronize(
            TransactionType.UNREDELEGATE,
            fetch_function=self.cosmos_client.get_unredelegate_txs,
        )

    def synchrinize_restake(self):
        self.synchronize(
            TransactionType.RESTAKE, fetch_function=self.cosmos_client.get_restake_txs
        )

    def synchronize_by_type(self, tx_type: TransactionType):
        if tx_type == TransactionType.DELEGATE:
            self.synchronize_delegate()
        elif tx_type == TransactionType.UNDELEGATE:
            self.synchronize_undelegate()
        elif tx_type == TransactionType.REDELEGATE:
            self.synchronize_redelegate()
        elif tx_type == TransactionType.UNREDELEGATE:
            self.synchronize_unredelegate()
        elif tx_type == TransactionType.RESTAKE:
            self.synchrinize_restake()
