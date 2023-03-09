from src.core.transactions.model import TransactionType
from src.synchronizer.common.synchronizer import TxSynchronizer
from src.synchronizer.restake.synchronizer import RestakeTxSynchronizer


def test_parse_transaction():
    synchronizer = RestakeTxSynchronizer()

    assert isinstance(synchronizer, TxSynchronizer)
    validator_address = "validator_address"

    message = {
        "@type": "/cosmos.authz.v1beta1.MsgExec",
        "grantee": "cosmos1grantee",
        "msgs": [
            {
                "@type": "/cosmos.staking.v1beta1.MsgDelegate",
                "delegator_address": "cosmos1delegator",
                "validator_address": validator_address,
                "amount": {"denom": "stake", "amount": "1000"},
            },
            {
                "@type": "/cosmos.staking.v1beta1.MsgDelegate",
                "delegator_address": "cosmos1delegator",
                "validator_address": validator_address,
                "amount": {"denom": "stake", "amount": "1000"},
            },
        ],
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

    assert len(transactions) == 2
    assert transactions[0]["height"] == message_props["height"]
    assert transactions[0]["hash"] == message_props["hash"]
    assert transactions[0]["memo"] == message_props["memo"]
    assert transactions[0]["timestamp"] == message_props["timestamp"]
    assert transactions[0]["offset"] == message_props["offset"]
    assert transactions[0]["validator"] == message["msgs"][0]["validator_address"]
    assert transactions[0]["delegator"] == message["msgs"][0]["delegator_address"]
    assert transactions[0]["amount"] == int(message["msgs"][0]["amount"]["amount"])
    assert transactions[0]["type"] == TransactionType.RESTAKE.value
