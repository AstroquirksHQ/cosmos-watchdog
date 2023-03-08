from typing import List, Dict

from src.core.transactions.model import TransactionType
from ..common.synchronizer import TxSynchronizer
from ...core.cosmos_client.cosmos_client import CosmosClient


class RedelegateTxSynchronizer(TxSynchronizer):
    tx_type = TransactionType.REDELEGATE
    message_type = "/cosmos.staking.v1beta1.MsgBeginRedelegate"
    fetch_transactions = CosmosClient().get_redelegate_txs

    @classmethod
    def parse_transaction(
        cls, message: Dict, message_props: Dict, validator_address: str
    ) -> List[Dict]:
        transactions = []
        if message["@type"] == cls.message_type and (
            message["validator_dst_address"] == validator_address
            or message["validator_src_address"] == validator_address
        ):
            transactions.append(
                {
                    **message_props,
                    "from_validator": message["validator_src_address"],
                    "validator": message["validator_dst_address"],
                    "delegator": message["delegator_address"],
                    "amount": int(message["amount"]["amount"]),
                    "type": TransactionType.REDELEGATE.value
                    if message["validator_dst_address"] == validator_address
                    else TransactionType.UNREDELEGATE.value,
                }
            )
        return transactions
