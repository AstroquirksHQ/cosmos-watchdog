from typing import Optional

from flask import current_app
from peewee import IntegrityError

from api.transactions.model import TransactionType, Transaction


class TransactionService:
    def __init__(self):
        self.logger = current_app.logger

    def save_many(self, transactions: list[Transaction]) -> list[int]:
        new_entries = []
        for tx in transactions:
            try:
                tx.save()
                new_entries.append(tx.id)
            except IntegrityError:
                self.logger.debug("The transaction already exist")
                pass
        self.logger.info(f"Saved {len(new_entries)} new transactions!")
        return new_entries

    def delete_transactions(self, tx_type: TransactionType, from_offset: int):
        self.logger.warn(f"DELETING {tx_type.value} TRANSACTIONS ...")
        nb_del = Transaction.delete_by_type_from_offset(tx_type, from_offset)
        self.logger.warn(f"{nb_del} {tx_type.value} TRANSACTIONS DELETED !")
