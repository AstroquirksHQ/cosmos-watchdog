from typing import Optional

from flask import current_app
from api.transactions.model import TransactionType, Transaction


class TransactionService:
    def __init__(self):
        self.logger = current_app.logger

    def save_many(self, transactions: list[dict]):
        new_entries = (
            Transaction.insert_many(transactions).on_conflict_ignore().execute()
        )
        self.logger.info(f"Saved {len(new_entries)} new transactions")

    def delete_transactions(self, tx_type: TransactionType, from_offset: Optional[int]):
        self.logger.warn(f"DELETING {tx_type.value} TRANSACTIONS ...")
        nb_del = Transaction.delete_by_type_from_offset(tx_type, from_offset)
        self.logger.warn(f"{nb_del} {tx_type.value} TRANSACTIONS DELETED !")
