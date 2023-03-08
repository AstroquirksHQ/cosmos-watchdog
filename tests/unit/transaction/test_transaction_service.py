from random import randint

import pytest

from api.transactions.model import TransactionType, Transaction


def test_save_many(transaction_service):
    transactions = []
    for tx_type in TransactionType:
        for i in range(5):
            transactions.append(
                {
                    "from_validator": f"Validator{i}",
                    "validator": f"Validator{i + 1}",
                    "delegator": f"Delegator{i}",
                    "type": tx_type.value,
                    "hash": f"Hash{i}",
                    "height": randint(1, 100),
                    "amount": randint(1, 100),
                    "memo": f"Memo{i}",
                    "timestamp": "%Y-%m-%d %H:%M:%S",
                    "offset": i,
                }
            )
    new_entries = transaction_service.save_many(transactions)
    assert len(new_entries) == len(transactions)

    # verify entries were saved in database
    saved_tx = Transaction.select().where(Transaction.id.in_(new_entries))
    assert saved_tx.count() == len(transactions)

    # try to save transactions again and verify duplicates are not saved
    duplicated_entries = transaction_service.save_many(transactions)
    assert len(duplicated_entries) == 0


@pytest.mark.parametrize(
    "tx_type, from_offset, expected_deleted",
    [
        (TransactionType.DELEGATE, 0, 5),
        (TransactionType.DELEGATE, 2, 3),
        (TransactionType.DELEGATE, 238, 0),
    ],
)
def test_delete_transactions(
    populate_db, transaction_service, tx_type, from_offset, expected_deleted
):
    nb_deleted = transaction_service.delete_transactions(tx_type, from_offset)
    assert nb_deleted == expected_deleted

    deleted_tx = Transaction.select().where(
        Transaction.type == tx_type.value, Transaction.offset >= from_offset
    )
    assert deleted_tx.count() == 0


@pytest.mark.parametrize(
    "tx_type, from_offset, expected_deleted",
    [
        (TransactionType.DELEGATE, 0, 0),
        (TransactionType.DELEGATE, 24, 0),
    ],
)
def test_delete_transactions_empty_db(
    transaction_service, tx_type, from_offset, expected_deleted
):
    nb_deleted = transaction_service.delete_transactions(tx_type, from_offset)
    assert nb_deleted == expected_deleted

    deleted_tx = Transaction.select().where(
        Transaction.type == tx_type.value, Transaction.offset >= from_offset
    )
    assert deleted_tx.count() == expected_deleted
