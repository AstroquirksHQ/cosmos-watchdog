import pytest
from peewee import IntegrityError

from api.transactions.model import Transaction, TransactionType


@pytest.mark.parametrize("tx_type", [tx_type for tx_type in TransactionType])
def test_get_last_offset_by_type(populate_db, tx_type):
    # Get the last offset for the specified transaction type
    last_offset = Transaction.get_last_offset_by_type(tx_type)

    # Assert that the last offset is correct
    assert last_offset == 4


def test_unique_constraints():
    # Create a transaction
    transaction = Transaction.create(
        from_validator="val1",
        validator="val2",
        delegator="delegator1",
        type=TransactionType.DELEGATE.value,
        hash="hash1",
        height=1,
        amount=100,
        memo="memo1",
        timestamp="2022-03-05T12:00:00Z",
        offset=1,
    )

    # Check that the transaction was created successfully
    assert transaction.id is not None

    # Try to create another transaction with the same ("delegator", "type", "hash") combination
    with pytest.raises(IntegrityError):
        Transaction.create(
            from_validator="val3",
            validator="val4",
            delegator="delegator1",
            type=TransactionType.DELEGATE.value,
            hash="hash1",
            height=2,
            amount=200,
            memo="memo2",
            timestamp="2022-03-05T12:00:01Z",
            offset=2,
        )

    # Try to create another transaction with a different combination of fields
    transaction = Transaction.create(
        from_validator="val5",
        validator="val6",
        delegator="delegator2",
        type=TransactionType.DELEGATE.value,
        hash="hash2",
        height=3,
        amount=300,
        memo="memo3",
        timestamp="2022-03-05T12:00:02Z",
        offset=3,
    )

    # Check that the transaction was created successfully
    assert transaction.id is not None

    # Try to create another transaction with the same fields as the previous one but another hash
    transaction = Transaction.create(
        from_validator="val5",
        validator="val6",
        delegator="delegator2",
        type=TransactionType.DELEGATE.value,
        hash="hash3",
        height=4,
        amount=400,
        memo="memo4",
        timestamp="2022-03-05T12:00:03Z",
        offset=4,
    )

    # Check that the transaction was created successfully
    assert transaction.id is not None
