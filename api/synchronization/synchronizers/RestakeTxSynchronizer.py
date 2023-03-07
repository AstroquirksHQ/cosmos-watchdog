from typing import List

from api.cosmos_client.cosmos_client import CosmosClient
from api.synchronization.synchronizers.DelegateTxSynchronizer import (
    DelegateTxSynchronizer,
)
from api.synchronization.synchronizers.common.TxSynchronizer import TxSynchronizer
from api.transactions.model import Transaction, TransactionType


class RestakeTxSynchronizer(TxSynchronizer):
    tx_type = TransactionType.RESTAKE
    message_type = "/cosmos.authz.v1beta1.MsgExec"
    fetch_transactions = CosmosClient().get_restake_txs

    def parse_transaction(
        cls, message: dict, message_props: dict, validator_address: str
    ) -> List[Transaction]:
        transactions = []
        if message["@type"] == cls.message_type:
            message_props["grantee"] = message["grantee"]
            for msg in message["msgs"]:
                transactions += DelegateTxSynchronizer.parse_transaction(
                    msg, message_props, validator_address
                )
        return transactions
