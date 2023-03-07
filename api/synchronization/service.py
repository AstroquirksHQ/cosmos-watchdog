from typing import Dict, Type

from flask import current_app

from api.notifications.service import NotificationService
from api.synchronization.synchronizers.DelegateTxSynchronizer import (
    DelegateTxSynchronizer,
)
from api.synchronization.synchronizers.RedelegateTxSynchronizer import (
    RedelegateTxSynchronizer,
)
from api.synchronization.synchronizers.RestakeTxSynchronizer import (
    RestakeTxSynchronizer,
)
from api.synchronization.synchronizers.UndelegateTxSynchronizer import (
    UndelegateTxSynchronizer,
)
from api.synchronization.synchronizers.UnredelegateTxSynchronizer import (
    UnredelegateTxSynchronizer,
)
from api.synchronization.synchronizers.common.TxSynchronizer import TxSynchronizer
from api.transactions.model import TransactionType, Transaction
from api.transactions.service import TransactionService

TRANSACTION_SYNCHRONIZERS: Dict[TransactionType, Type[TxSynchronizer]] = {
    TransactionType.DELEGATE: DelegateTxSynchronizer,
    TransactionType.UNDELEGATE: UndelegateTxSynchronizer,
    TransactionType.REDELEGATE: RedelegateTxSynchronizer,
    TransactionType.UNREDELEGATE: UnredelegateTxSynchronizer,
    TransactionType.RESTAKE: RestakeTxSynchronizer,
}


class SynchronizationService:
    PAGE_SIZE = 100

    def __init__(self, validator_address: str):
        self.logger = current_app.logger
        self.validator_address = validator_address
        self.transaction_service = TransactionService()
        self.notification_service = NotificationService()

    def get_page_offset(self, tx_type: TransactionType) -> int:
        last_offset = Transaction.get_last_offset_by_type(tx_type)
        return int(last_offset / self.PAGE_SIZE) * self.PAGE_SIZE

    def synchronize(self, synchronizer: TxSynchronizer, notify: bool):
        self.logger.info(
            f"[{synchronizer.tx_type.value}] - Synchronizing transactions ..."
        )
        page_offset = self.get_page_offset(synchronizer.tx_type)
        self.logger.info(
            f"[{synchronizer.tx_type.value}] - Last offset seen: {page_offset}"
        )
        transactions_batches = synchronizer.fetch_all_txs(
            self.validator_address, page_offset
        )
        for transactions_batch, offset in transactions_batches:
            transactions = synchronizer.extract_transactions(
                transactions_batch, offset, self.validator_address
            )
            self.logger.info(
                f"Found {len(transactions)} transactions from offset {offset}"
            )
            if transactions:
                new_transactions = self.transaction_service.save_many(transactions)
                if notify:
                    self.notification_service.new_notifications(new_transactions)

    def synchronize_by_type(self, tx_type: TransactionType, notify: bool):
        synchronizer = TRANSACTION_SYNCHRONIZERS.get(tx_type)
        if synchronizer is None:
            raise ValueError(f"Transaction type not supported: {tx_type}")
        self.synchronize(synchronizer(), notify=notify)
