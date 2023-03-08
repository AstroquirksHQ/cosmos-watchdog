from api.cosmos_client.cosmos_client import CosmosClient
from api.synchronization.synchronizers.DelegateTxSynchronizer import (
    DelegateTxSynchronizer,
)
from api.transactions.model import TransactionType


class UndelegateTxSynchronizer(DelegateTxSynchronizer):
    tx_type = TransactionType.UNDELEGATE
    message_type = "/cosmos.staking.v1beta1.MsgUndelegate"
    fetch_transactions = CosmosClient().get_undelegate_txs
