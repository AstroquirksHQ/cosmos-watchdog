from src.core.transactions.model import TransactionType
from ..redelegate.synchronizer import RedelegateTxSynchronizer
from ...core.cosmos_client.cosmos_client import CosmosClient


class UnredelegateTxSynchronizer(RedelegateTxSynchronizer):
    tx_type = TransactionType.UNREDELEGATE
    message_type = "/cosmos.staking.v1beta1.MsgBeginRedelegate"
    fetch_transactions = CosmosClient().get_unredelegate_txs
