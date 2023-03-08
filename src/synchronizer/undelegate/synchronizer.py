from src.core.transactions.model import TransactionType
from ..delegate.synchronizer import DelegateTxSynchronizer
from ...core.cosmos_client.cosmos_client import CosmosClient


class UndelegateTxSynchronizer(DelegateTxSynchronizer):
    tx_type = TransactionType.UNDELEGATE
    message_type = "/cosmos.staking.v1beta1.MsgUndelegate"
    fetch_transactions = CosmosClient().get_undelegate_txs
