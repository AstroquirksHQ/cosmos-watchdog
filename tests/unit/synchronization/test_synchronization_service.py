from unittest.mock import MagicMock, Mock

import pytest

from api.synchronization.service import TRANSACTION_SYNCHRONIZERS
from api.transactions.model import TransactionType


def test_synchronize_by_supported_type(synchronization_service):
    synchronization_service.synchronize = MagicMock()
    tx_type = TransactionType.DELEGATE

    synchronization_service.synchronize_by_type(tx_type, notify=True)

    synchronizer = TRANSACTION_SYNCHRONIZERS[tx_type]

    synchronization_service.synchronize.assert_called_once()
    calls = synchronization_service.synchronize.mock_calls
    assert isinstance(calls[0].args[0], synchronizer)
    assert calls[0].kwargs == {"notify": True}


@pytest.mark.parametrize(
    "notify",
    [
        True,
        False,
    ],
)
def test_synchronize(synchronization_service, notify):
    synchronization_service.transaction_service.save_many = MagicMock(
        return_value=[Mock(), Mock()]
    )
    synchronization_service.notification_service.new_notifications_for_tx_ids = (
        MagicMock()
    )
    synchronization_service.get_page_offset = MagicMock(return_value=10)
    mocked_synchronizer = MagicMock()

    mocked_synchronizer.fetch_all_txs = MagicMock(
        return_value=iter(
            [
                (
                    [
                        {
                            "@type": "/cosmos.staking.v1beta1.MsgDelegate",
                            "validator_address": "cosmosvaloper1abc",
                        }
                    ],
                    20,
                )
            ]
        )
    )

    synchronization_service.synchronize(mocked_synchronizer, notify)

    synchronization_service.get_page_offset.assert_called_once_with(
        mocked_synchronizer.tx_type
    )
    mocked_synchronizer.fetch_all_txs.assert_called_once_with(
        synchronization_service.validator_address, 10
    )
    synchronization_service.transaction_service.save_many.assert_called_once()
    assert (
        synchronization_service.notification_service.new_notifications_for_tx_ids.call_count
        == int(notify)
    )
