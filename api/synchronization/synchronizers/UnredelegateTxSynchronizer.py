from api.cosmos_client.cosmos_client import CosmosClient
from api.synchronization.synchronizers.RedelegateTxSynchronizer import (
    RedelegateTxSynchronizer,
)
from api.transactions.model import TransactionType


class UnredelegateTxSynchronizer(RedelegateTxSynchronizer):
    tx_type = TransactionType.UNREDELEGATE
    message_type = "/cosmos.staking.v1beta1.MsgBeginRedelegate"
    fetch_transactions = CosmosClient().get_unredelegate_txs
