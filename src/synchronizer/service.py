from typing import Dict, Type

import structlog

from src.core.common.database.context import database_context
from src.core.notifications.service import NotificationService
from src.core.transactions.model import TransactionType, Transaction
from src.core.transactions.service import TransactionService
from src.synchronizer.common.synchronizer import TxSynchronizer
from src.synchronizer.delegate.synchronizer import DelegateTxSynchronizer
from src.synchronizer.redelegate.synchronizer import RedelegateTxSynchronizer
from src.synchronizer.restake.synchronizer import RestakeTxSynchronizer
from src.synchronizer.undelegate.synchronizer import UndelegateTxSynchronizer
from src.synchronizer.unredelegate.synchronizer import UnredelegateTxSynchronizer

TRANSACTION_SYNCHRONIZERS: Dict[TransactionType, Type[TxSynchronizer]] = {
    TransactionType.DELEGATE: DelegateTxSynchronizer,
    TransactionType.UNDELEGATE: UndelegateTxSynchronizer,
    TransactionType.REDELEGATE: RedelegateTxSynchronizer,
    TransactionType.UNREDELEGATE: UnredelegateTxSynchronizer,
    TransactionType.RESTAKE: RestakeTxSynchronizer,
}


@database_context
class SynchronizationService:
    PAGE_SIZE = 100

    def __init__(self, validator_address: str):
        self.logger = structlog.get_logger(__name__).bind(
            service=self.__class__.__name__
        )
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
                    self.notification_service.new_notifications_for_tx_ids(
                        new_transactions
                    )

    def synchronize_by_type(self, tx_type: TransactionType, notify: bool):
        synchronizer = TRANSACTION_SYNCHRONIZERS.get(tx_type)
        if synchronizer is None:
            raise ValueError(f"Transaction type not supported: {tx_type}")
        self.synchronize(synchronizer(), notify=notify)
