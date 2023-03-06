from unittest import mock
from unittest.mock import MagicMock

from api.transactions.model import TransactionType


def test_fetch_all_txs(synchronization_service):
    mock_response = {
        "pagination": {"total": "2"},
        "tx_responses": [{"txhash": "hash"}],
    }
    mock_fetch_function = mock.MagicMock(return_value=mock_response)
    mock_callback = mock.MagicMock()

    synchronization_service.fetch_all_txs(
        "address", fetch_function=mock_fetch_function, callback=mock_callback
    )

    assert mock_fetch_function.call_count == 2
    assert mock_fetch_function.call_args == mock.call("address", offset=1)
    assert mock_callback.call_count == 2
    assert mock_callback.call_args == mock.call(mock_response["tx_responses"], 1)
