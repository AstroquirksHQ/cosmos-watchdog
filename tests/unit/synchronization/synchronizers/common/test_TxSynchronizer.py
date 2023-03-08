from datetime import datetime
from typing import Dict, List
from unittest.mock import Mock, call

from api.synchronization.synchronizers.common.TxSynchronizer import TxSynchronizer


def test_fetch_all_txs():
    tx_responses = [
        {
            "height": 1,
            "txhash": "hash1",
            "tx": {"body": {"memo": "memo1", "messages": []}},
            "timestamp": "2022-03-08T08:01:00.000000Z",
        },
        {
            "height": 2,
            "txhash": "hash2",
            "tx": {"body": {"memo": "memo2", "messages": []}},
            "timestamp": "2022-03-08T08:02:00.000000Z",
        },
    ]

    mocked_fetch_transactions = Mock(
        side_effect=lambda validator_address, offset: {
            "tx_responses": tx_responses,
            "pagination": {"total": "4"},
        }
    )

    class MySynchronizer(TxSynchronizer):
        @property
        def tx_type(cls):
            return "my_tx_type"

        @property
        def message_type(cls):
            return "my_message_type"

        @property
        def fetch_transactions(self):
            return mocked_fetch_transactions

        @classmethod
        def parse_transaction(
            cls, message: Dict, message_props: Dict, validator_address: str
        ) -> List[Dict]:
            pass

    synchronizer = MySynchronizer()

    validator_address = "validator1"
    txs = []
    for resp, offset in synchronizer.fetch_all_txs(validator_address):
        txs += resp

    assert len(txs) == 4
    assert txs[0] == tx_responses[0]
    assert txs[1] == tx_responses[1]
    assert txs[2] == tx_responses[0]
    assert txs[3] == tx_responses[1]
    mocked_fetch_transactions.assert_called()
    calls = mocked_fetch_transactions.mock_calls
    expected_calls = [
        call(validator_address, offset=0),
        call(validator_address, offset=2),
    ]
    assert calls == expected_calls


def test_extract_transactions():
    message_type = "my_message_type"

    class MySynchronizer(TxSynchronizer):
        @property
        def tx_type(self):
            return "my_tx_type"

        @property
        def message_type(self):
            return message_type

        @property
        def fetch_transactions(self):
            pass

        @classmethod
        def parse_transaction(
            cls, message: Dict, message_props: Dict, validator_address: str
        ) -> List[Dict]:
            return [
                {
                    "message": message,
                    "message_props": message_props,
                    "validator_address": validator_address,
                }
            ]

    synchronizer = MySynchronizer()

    node_transactions = [
        {
            "height": 1,
            "txhash": "hash1",
            "tx": {
                "body": {
                    "memo": "memo1",
                    "messages": [{"type": message_type, "data": "data1"}],
                }
            },
            "timestamp": "2022-03-07T10:00:00Z",
        },
        {
            "height": 2,
            "txhash": "hash2",
            "tx": {
                "body": {
                    "memo": "memo2",
                    "messages": [{"type": message_type, "data": "data2"}],
                }
            },
            "timestamp": "2022-03-07T11:00:00Z",
        },
    ]

    offset = 0
    validator_address = "my_validator_address"
    expected_transactions = [
        {
            "message": {"type": message_type, "data": "data1"},
            "message_props": {
                "height": 1,
                "hash": "hash1",
                "memo": "memo1",
                "timestamp": datetime.strptime(
                    "2022-03-07T10:00:00Z", "%Y-%m-%dT%H:%M:%SZ"
                ),
                "offset": 0,
            },
            "validator_address": validator_address,
        },
        {
            "message": {"type": message_type, "data": "data2"},
            "message_props": {
                "height": 2,
                "hash": "hash2",
                "memo": "memo2",
                "timestamp": datetime.strptime(
                    "2022-03-07T11:00:00Z", "%Y-%m-%dT%H:%M:%SZ"
                ),
                "offset": 1,
            },
            "validator_address": validator_address,
        },
    ]
    assert (
        synchronizer.extract_transactions(node_transactions, offset, validator_address)
        == expected_transactions
    )
