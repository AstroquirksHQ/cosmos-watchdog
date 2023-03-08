from typing import List, Dict

from api.cosmos_client.cosmos_client import CosmosClient
from api.synchronization.synchronizers.common.TxSynchronizer import TxSynchronizer
from api.transactions.model import TransactionType


class DelegateTxSynchronizer(TxSynchronizer):
    tx_type = TransactionType.DELEGATE
    message_type = "/cosmos.staking.v1beta1.MsgDelegate"
    fetch_transactions = CosmosClient().get_delegate_txs

    @classmethod
    def parse_transaction(
        cls, message: Dict, message_props: Dict, validator_address: str
    ) -> List[Dict]:
        transactions = []
        if (
            message["@type"] == cls.message_type
            and message["validator_address"] == validator_address
        ):
            transactions.append(
                {
                    **message_props,
                    "validator": message["validator_address"],
                    "delegator": message["delegator_address"],
                    "amount": int(message["amount"]["amount"]),
                    "type": cls.tx_type.value,
                }
            )
        return transactions
