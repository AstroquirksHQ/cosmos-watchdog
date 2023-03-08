from src.core.transactions.model import TransactionType
from src.synchronizer.common.synchronizer import TxSynchronizer
from src.synchronizer.unredelegate.synchronizer import UnredelegateTxSynchronizer


def test_parse_transaction():
    synchronizer = UnredelegateTxSynchronizer()
    validator_address = "validator_address"

    assert isinstance(synchronizer, TxSynchronizer)

    message = {
        "@type": "/cosmos.staking.v1beta1.MsgBeginRedelegate",
        "amount": {"amount": "100", "denom": "STAKE"},
        "delegator_address": "cosmos1delegator",
        "validator_src_address": validator_address,
        "validator_dst_address": "cosmos1source",
    }

    message_props = {
        "height": 1,
        "hash": "hash",
        "memo": "memo",
        "timestamp": "2022-03-08T08:01:00.000000Z",
        "offset": 0,
    }

    transactions = synchronizer.parse_transaction(
        message, message_props, validator_address
    )

    assert len(transactions) == 1
    assert transactions[0]["height"] == message_props["height"]
    assert transactions[0]["hash"] == message_props["hash"]
    assert transactions[0]["memo"] == message_props["memo"]
    assert transactions[0]["timestamp"] == message_props["timestamp"]
    assert transactions[0]["offset"] == message_props["offset"]
    assert transactions[0]["validator"] == message["validator_dst_address"]
    assert transactions[0]["from_validator"] == message["validator_src_address"]
    assert transactions[0]["delegator"] == message["delegator_address"]
    assert transactions[0]["amount"] == int(message["amount"]["amount"])
    assert transactions[0]["type"] == TransactionType.UNREDELEGATE.value
