import pytest
from peewee import IntegrityError

from api.transactions.model import Transaction, TransactionType


@pytest.mark.parametrize("tx_type", [tx_type for tx_type in TransactionType])
def test_get_last_offset_by_type(populate_db, tx_type):
    last_offset = Transaction.get_last_offset_by_type(tx_type)

    assert last_offset == 4


@pytest.mark.parametrize("tx_type", [tx_type for tx_type in TransactionType])
def test_get_last_offset_by_type_empty_db(tx_type):
    last_offset = Transaction.get_last_offset_by_type(tx_type)

    assert last_offset == 0


@pytest.mark.parametrize(
    "tx_type, from_offset, expected_count",
    [
        (TransactionType.RESTAKE, 3, 2),  # Test with offset == 3
        (TransactionType.RESTAKE, 0, 5),  # Test with offset == 0
    ],
)
def test_delete_by_type_from_offset(populate_db, tx_type, from_offset, expected_count):
    count = Transaction.delete_by_type_from_offset(tx_type, from_offset)
    assert count == expected_count


def test_unique_constraints():
    tx_props = {
        "from_validator": "val1",
        "validator": "val2",
        "delegator": "delegator1",
        "type": TransactionType.DELEGATE.value,
        "hash": "hash1",
        "height": 1,
        "amount": 100,
        "memo": "memo1",
        "timestamp": "2022-03-05T12:00:00Z",
        "offset": 1,
    }

    # Create a transaction
    transaction = Transaction.create(**tx_props)

    # Check that the transaction was created successfully
    assert transaction.id is not None

    # Try to create another transaction with the same ("delegator", "type", "hash") combination
    with pytest.raises(IntegrityError):
        Transaction.create(
            **{
                **tx_props,
                "delegator": "delegator1",
                "type": TransactionType.DELEGATE.value,
                "hash": "hash1",
            }
        )

    # Try to create another transaction with the same fields as the previous one but another delegator
    transaction = Transaction.create(**{**tx_props, "delegator": "abc"})

    # Check that the transaction was created successfully
    assert transaction.id is not None

    # Try to create another transaction with the same fields as the first one but another type
    transaction = Transaction.create(
        **{**tx_props, "type": TransactionType.REDELEGATE.value}
    )

    # Check that the transaction was created successfully
    assert transaction.id is not None

    # Try to create another transaction with the same fields as the first one but another hash
    transaction = Transaction.create(**{**tx_props, "hash": "abxkjguk"})

    # Check that the transaction was created successfully
    assert transaction.id is not None
