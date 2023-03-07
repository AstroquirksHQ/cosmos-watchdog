from typing import List

from api.cosmos_client.cosmos_client import CosmosClient
from api.synchronization.synchronizers.common.TxSynchronizer import TxSynchronizer
from api.transactions.model import TransactionType, Transaction


class DelegateTxSynchronizer(TxSynchronizer):
    tx_type = TransactionType.DELEGATE
    message_type = "/cosmos.staking.v1beta1.MsgDelegate"
    fetch_transactions = CosmosClient().get_delegate_txs

    @classmethod
    def parse_transaction(
        cls, message: dict, message_props: dict, validator_address: str
    ) -> List[Transaction]:
        transactions = []
        if (
            message["@type"] == cls.message_type
            and message["validator_address"] == validator_address
        ):
            transactions.append(
                Transaction(
                    **message_props,
                    validator=message["validator_address"],
                    delegator=message["delegator_address"],
                    amount=int(message["amount"]["amount"]),
                    type=cls.tx_type.value,
                )
            )
        return transactions
