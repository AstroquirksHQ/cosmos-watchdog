from typing import Dict, List

import structlog
from peewee import IntegrityError

from src.core.common.database.context import database_context
from src.core.transactions.model import Transaction, TransactionType


@database_context
class TransactionService:
    def __init__(self):
        self.logger = structlog.get_logger(__name__).bind(
            service=self.__class__.__name__
        )

    def save_many(self, transactions_datas: List[Dict]) -> List[int]:
        new_entries = []
        for tx_data in transactions_datas:
            try:
                tx = Transaction(**tx_data)
                tx.save()
                new_entries.append(tx.id)
            except IntegrityError:
                self.logger.debug("The transaction already exist")
                pass
        self.logger.info(f"Saved {len(new_entries)} new transactions!")
        return new_entries

    def delete_transactions(self, tx_type: TransactionType, from_offset: int) -> int:
        self.logger.warn(f"DELETING {tx_type.value} TRANSACTIONS ...")
        nb_del = Transaction.delete_by_type_from_offset(tx_type, from_offset)
        self.logger.warn(f"{nb_del} {tx_type.value} TRANSACTIONS DELETED !")
        return nb_del
