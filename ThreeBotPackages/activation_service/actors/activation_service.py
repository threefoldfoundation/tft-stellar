import os
import sys
import time

import stellar_sdk
from stellar_sdk.exceptions import Ed25519PublicKeyInvalidError, BadRequestError, SdkError
from jumpscale.core.exceptions import JSException
from jumpscale.loader import j
from jumpscale.servers.gedis.baseactor import BaseActor, actor_method


current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../sals/")
from activation_sal import activate_account as activate_account_sal, get_wallet


class ActivationService(BaseActor):
    def _stellar_address_used_before(self, stellar_address):
        try:
            transactions = get_wallet().list_transactions(address=stellar_address)
            return len(transactions) != 0
        except stellar_sdk.exceptions.NotFoundError:
            return False

    def _get_network_passphrase(self, network: str) -> str:
        if network == "TEST":
            return stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
        return stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE

    def _activate_account(self, address):
        # TODO: serialize with a gevent pool
        wallet = get_wallet()
        tftasset = wallet._get_asset()
        a = get_wallet().load_account()
        if not a.last_created_sequence_is_used:
            if (wallet.sequencedate + 60) > int(time.time()):
                raise j.exceptions.Value(f"Busy, try again later")

        server = wallet._get_horizon_server()

        source_account = wallet.load_account()

        base_fee = server.fetch_base_fee()
        transaction = (
            stellar_sdk.TransactionBuilder(
                source_account=source_account,
                network_passphrase=self._get_network_passphrase(wallet.network.value),
                base_fee=base_fee,
            )
            .append_begin_sponsoring_future_reserves_op(address)
            .append_create_account_op(destination=address, starting_balance="0")
            .append_change_trust_op(asset_issuer=tftasset.issuer, asset_code=tftasset.code, source=address)
            .append_end_sponsoring_future_reserves_op(address)
            .set_timeout(60)
            .build()
        )
        source_keypair = stellar_sdk.Keypair.from_secret(wallet.secret)
        transaction.sign(source_keypair)
        return transaction.to_xdr()

    @actor_method
    def activate_account(self, address: str) -> str:

        if self._stellar_address_used_before(address):
            raise j.exceptions.Value("This address is not new")
        tx = self._activate_account(address)
        response = j.data.serializers.json.dumps({"activation_transaction": tx, "address": address})
        return response


Actor = ActivationService
