from typing import List, Dict

from src.core.transactions.model import TransactionType
from ..common.synchronizer import TxSynchronizer
from ..delegate.synchronizer import DelegateTxSynchronizer
from ...core.cosmos_client.cosmos_client import CosmosClient


class RestakeTxSynchronizer(TxSynchronizer):
    tx_type = TransactionType.RESTAKE
    message_type = "/cosmos.authz.v1beta1.MsgExec"
    fetch_transactions = CosmosClient().get_restake_txs

    @classmethod
    def parse_transaction(
        cls, message: dict, message_props: dict, validator_address: str
    ) -> List[Dict]:
        transactions = []
        if message["@type"] == cls.message_type:
            message_props["grantee"] = message["grantee"]
            for msg in message["msgs"]:
                transactions += [
                    {**tx, "type": cls.tx_type.value}
                    for tx in DelegateTxSynchronizer.parse_transaction(
                        msg, message_props, validator_address
                    )
                ]
        return transactions
