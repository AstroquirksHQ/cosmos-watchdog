from typing import Dict, Optional

import requests
import structlog

from src.core.cosmos_client.exceptions import EmptyResponseException


class CosmosClient:
    """
    A client for interacting with the Cosmos blockchain via its RPC API.
    """

    # Default value of the base URL of the Osmosis API
    BASE_URL = "https://osmosis-mainnet-rpc.allthatnode.com:1317"

    def __init__(self, url: str = BASE_URL):
        self.base_url = url
        self.logger = structlog.get_logger(__name__).bind(
            service=self.__class__.__name__
        )

    def get(self, endpoint: str, params: dict = None) -> Optional[dict]:
        url = f"{self.base_url}{endpoint}"
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        if not resp.content:
            raise EmptyResponseException
        return resp.json()

    def get_delegations(self, validator_address: str) -> dict:
        """
        Returns a dictionary containing information about the delegations
        made to the specified validator.

        Args:
            validator_address (str): The address of the validator to query.

        Returns:
            dict: A dictionary containing information about the delegations made
                to the specified validator.
        """
        url = f"/cosmos/staking/v1beta1/validators/{validator_address}/delegations"
        return self.get(url)

    def get_reward_commission(self, validator_address: str) -> float:
        """
        Returns the current reward commission for a validator.

        Args:
            validator_address (str): The validator's address.

        Returns:
            float: The current reward commission of the validator
        """
        url = f"/cosmos/distribution/v1beta1/validators/{validator_address}/commission"
        resp = self.get(url)
        return float(resp["commission"]["commission"][0]["amount"])

    def get_stake_authorization(self, grantee: str, granter: str) -> dict:
        params = {"grantee": grantee, "granter": granter}
        """
        TODO : Check this transaction :
        hash = 4F403497F94794C486BDDF4A9BB38E65A76A4251F87AA6B7C6283FBFBD7D494C
        https://www.mintscan.io/osmosis/txs/{hash}

        Why is it not in the grants ?
        """
        return self.get("/cosmos/authz/v1beta1/grants", params=params)

    def get_block_height(self) -> int:
        """
        Returns the current block height of the blockchain.

        Returns:
            int: The current block height of the blockchain.
        """
        url = "/cosmos/base/tendermint/v1beta1/blocks/latest"
        resp = self.get(url)
        return int(resp["block"]["header"]["height"])

    def get_validator(self, validator_address: str):
        """
        Returns information about the specified validator.

        Args:
            validator_address (str): The address of the validator to query.

        Returns:
            dict: A dictionary containing information about the specified validator.
        """
        resp = self.get(f"/cosmos/staking/v1beta1/validators/{validator_address}")
        return resp

    def get_delegator_delegations_by_validator(self, delegator: str, validator: str):
        """
        Retrieves all delegations of a delegator to a particular validator.

        :param delegator: The delegator address
        :param validator: The validator address
        :return: A dictionary containing the delegator's delegations to the validator
        """
        resp = self.get(
            f"/cosmos/staking/v1beta1/delegators/{delegator}/validators/{validator}"
        )
        return resp

    def get_delegator_all_delegations(self, delegator: str):
        """
        WIP
        """
        resp = self.get(f"/cosmos/staking/v1beta1/delegations/{delegator}")
        return resp

    def get_tx_by_hash(self, hash: str):
        """
        WIP
        """
        resp = self.get(f"/cosmos/tx/v1beta1/txs/{hash}")
        return resp

    def get_delegate_txs(self, address: str, offset: int = 0) -> Dict:
        self.logger.info(f"Fetching delegate txs for {address} - offset {offset}")
        params = {
            "events": [
                "message.action='/cosmos.staking.v1beta1.MsgDelegate'",
                f"delegate.validator='{address}'",
            ],
            "pagination.offset": offset,
        }
        try:
            resp = self.get("/cosmos/tx/v1beta1/txs", params=params)
        except Exception as e:
            self.logger.error(e)
            return {"tx_responses": [], "pagination": {"total": 0}}
        return resp

    def get_redelegate_txs(self, address: str, offset: int = 0):
        self.logger.info(f"Fetching redelegate tx to {address} - offset {offset}")
        params = {
            "events": [
                "message.action='/cosmos.staking.v1beta1.MsgBeginRedelegate'",
                f"redelegate.destination_validator='{address}'",
            ],
            "pagination.offset": offset,
        }
        try:
            resp = self.get("/cosmos/tx/v1beta1/txs", params=params)
        except Exception as e:
            self.logger.error(e)
            return {"tx_responses": [], "pagination": {"total": 0}}
        return resp

    def get_unredelegate_txs(self, address: str, offset: int = 0):
        self.logger.info(f"Fetching unredelegate tx from {address} - offset {offset}")
        params = {
            "events": [
                "message.action='/cosmos.staking.v1beta1.MsgBeginRedelegate'",
                f"redelegate.source_validator='{address}'",
            ],
            "pagination.offset": offset,
        }
        try:
            resp = self.get("/cosmos/tx/v1beta1/txs", params=params)
        except Exception as e:
            self.logger.error(e)
            return {"tx_responses": [], "pagination": {"total": 0}}
        return resp

    def get_undelegate_txs(self, address: str, offset: int = 0):
        self.logger.info(f"Fetching undelegate tx from {address} - offset {offset}")
        params = {
            "events": [
                "message.action='/cosmos.staking.v1beta1.MsgUndelegate'",
                f"unbond.validator='{address}'",
            ],
            "pagination.offset": offset,
        }
        try:
            resp = self.get("/cosmos/tx/v1beta1/txs", params=params)
        except Exception as e:
            self.logger.error(e)
            return {"tx_responses": [], "pagination": {"total": 0}}
        return resp

    def get_restake_txs(self, address: str, offset: int = 0):
        self.logger.info(f"Fectching restake tx for {address} - offset {offset}")
        params = {
            "events": [
                "message.action='/cosmos.authz.v1beta1.MsgExec'",
                f"delegate.validator='{address}'",
            ],
            "pagination.offset": offset,
        }
        try:
            resp = self.get("/cosmos/tx/v1beta1/txs", params=params)
        except Exception as e:
            self.logger.error(e)
            return {"tx_responses": [], "pagination": {"total": 0}}
        return resp
