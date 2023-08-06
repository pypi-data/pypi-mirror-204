"""Solana wrapper class.

This SOL class is meant to be accessed via KilnConnect.sol, it is
publicly exported in the SDK. This file contains helpers to
integration our Solana API with integrations such as Fireblocks. It
provides convenient shortcuts to use our SDK.
"""
import logging
from typing import Union, Callable

from .errors import KilnInternalServerError
from kiln_connect.integrations import (
    Integrations,
    Asset
)

from kiln_connect.openapi_client import (
    ApiClient, SOLStakeTxPayload, SOLDeactivateStakeTxPayload, SOLWithdrawStakeTxPayload, SOLMergeStakesTxPayload,
    SOLSplitStakeTxPayload,
)
from kiln_connect.openapi_client import (
    SolApi,
    SOLBroadcastTxPayload,
    SOLBroadcastTx,
    SOLPrepareTxPayload
)

from kiln_connect.openapi_client.exceptions import ServiceException


class SOL(SolApi):
    """Wrapper for the Solana API.
    """

    def __init__(self, api: ApiClient, integrations: Integrations):
        super().__init__(api)
        self.integrations = integrations

    def process_transaction(self, integration: str,
                            craft_tx: Union[SOLStakeTxPayload, SOLDeactivateStakeTxPayload, SOLWithdrawStakeTxPayload],
                            post_func: Callable) -> SOLBroadcastTx:
        fb = self.integrations.get_integration(integration)

        response = post_func(craft_tx)
        logging.debug("TX Crafted")

        unsigned_tx_payload = response.data.unsigned_tx_serialized
        unsigned_tx_hash = response.data.unsigned_tx_hash

        # Sign TX.
        sig = fb.raw_sign(Asset.sol, unsigned_tx_hash)

        signatures = []
        if isinstance(sig["fullSig"], str):
            signatures.append(sig["fullSig"])
        else:
            signatures = sig["fullSig"]

        # Prepare TX.
        prepare_tx = SOLPrepareTxPayload(
            unsigned_tx_serialized=unsigned_tx_payload,
            signatures=signatures,
        )

        logging.debug(
            "Preparing TX - unsigned_tx_serialized={0}, signatures={1}".format(
                prepare_tx.unsigned_tx_serialized, prepare_tx.signatures))

        response = super().post_sol_prepare_tx(prepare_tx)
        logging.debug("TX Prepared")

        # Broadcast TX.
        broadcast_tx = SOLBroadcastTxPayload(
            tx_serialized=response.data.signed_tx_serialized,
        )

        logging.debug(f"Broadcasting TX - {broadcast_tx.tx_serialized}")
        try:
            response = super().post_sol_broadcast_tx(broadcast_tx)
        except ServiceException:
            # Currently our OpenAPI specs does not expose schemas for error code responses so impossible
            # to provide better info
            logging.debug(r"/!\ Kiln API Internal Error /!\\")
            raise KilnInternalServerError()

        logging.debug("TX Broadcast")
        return response.data

    def stake(self, integration: str, account_id: str, wallet: str, vote_account: str,
              amount_lamports: int) -> SOLBroadcastTx:
        """Helper to stake on Solana using Fireblocks
        """
        # Craft TX.
        craft_tx = SOLStakeTxPayload(
            account_id=account_id,
            wallet=wallet,
            amount_lamports=str(amount_lamports),
            vote_account_address=vote_account
        )

        logging.debug(
            "Crafting TX - account_id={0}, wallet={1}, vote_account_address={2}, amount_lamports={3}".format(
                craft_tx.account_id, craft_tx.wallet, craft_tx.vote_account_address, craft_tx.amount_lamports))

        return self.process_transaction(integration, craft_tx, super().post_sol_stake_tx)

    def deactivate_stake(self, integration: str, stake_account: str, wallet: str) -> SOLBroadcastTx:
        """Helper to deativate stake on Solana using Fireblocks
        """
        # Craft TX.
        craft_tx = SOLDeactivateStakeTxPayload(
            stake_account=stake_account,
            wallet=wallet,
        )

        logging.debug(
            "Crafting TX - stake_account={0}, wallet={1}".format(
                craft_tx.stake_account, craft_tx.wallet))

        return self.process_transaction(integration, craft_tx, super().post_sol_deactivate_stake_tx)

    def withdraw_stake(self, integration: str, stake_account: str, wallet: str,
                       amount_lamports: int = None) -> SOLBroadcastTx:
        """Helper to withdraw stake on Solana using Fireblocks
        """
        # Craft TX.
        craft_tx = SOLWithdrawStakeTxPayload(
            stake_account=stake_account,
            wallet=wallet,
        )

        if amount_lamports is not None:
            craft_tx.amount_lamports = str(amount_lamports)

        logging.debug(
            "Crafting TX - stake_account={0}, wallet={1}, amount_lamports".format(
                craft_tx.stake_account, craft_tx.amount_lamports))

        return self.process_transaction(integration, craft_tx, super().post_sol_withdraw_stake_tx)

    def merge_stakes(self, integration: str, stake_account_source: str, stake_account_destination: str, wallet: str) -> SOLBroadcastTx:
        """Helper to merge stake on Solana using Fireblocks
        """
        # Craft TX.
        craft_tx = SOLMergeStakesTxPayload(
            stake_account_source=stake_account_source,
            stake_account_destination=stake_account_destination,
            wallet=wallet,
        )

        logging.debug(
            "Crafting TX - stake_account_source={0}, stake_account_destination={1}, wallet={2}".format(
                craft_tx.stake_account_source, craft_tx.stake_account_destination, craft_tx.wallet))

        return self.process_transaction(integration, craft_tx, super().post_sol_merge_stakes_tx)

    def split_stake(self, integration: str, account_id: str, stake_account: str, wallet: str, amount_lamports: int) -> SOLBroadcastTx:
        """Helper to split stake on Solana using Fireblocks
        """
        # Craft TX.
        craft_tx = SOLSplitStakeTxPayload(
            account_id=account_id,
            stake_account=stake_account,
            wallet=wallet,
            amount_lamports=str(amount_lamports),
        )

        logging.debug(
            "Crafting TX - account_id={0}, stake_account={1}, wallet={2}, amount_lamports={3}".format(
                craft_tx.account_id, craft_tx.stake_account, craft_tx.wallet, craft_tx.amount_lamports))

        return self.process_transaction(integration, craft_tx, super().post_sol_split_stake_tx)
