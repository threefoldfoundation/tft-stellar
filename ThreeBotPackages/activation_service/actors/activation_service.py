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

_MAX_FEE=1000000

SUPPORTED_ASSETS = {
    "TEST": [
        "TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3",
        "TFTA:GB55A4RR4G2MIORJTQA4L6FENZU7K4W7ATGY6YOT2CW47M5SZYGYKSCT",
        "FreeTFT:GBLDUINEFYTF7XEE7YNWA3JQS4K2VD37YU7I2YAE7R5AHZDKQXSS2J6R",
        "USDC:GAHHZJT5OIK6HXDXLCSRDTTNPE52CMXFWW6YQXCBMHW2HUI6D365HPOO",
    ],
    "STD": [
        "TFT:GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
        "TFTA:GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2",
        "FreeTFT:GCBGS5TFE2BPPUVY55ZPEMWWGR6CLQ7T6P46SOFGHXEBJ34MSP6HVEUT",
        "USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
    ],
}


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

    def _get_wallet(self):
        wallet = get_wallet()
        if not wallet:
            raise j.exceptions.Value("Service unavailable")
        # TODO: serialize with a gevent pool
        a = get_wallet().load_account()
        if not a.last_created_sequence_is_used:
            if (wallet.sequencedate + 60) > int(time.time()):
                raise j.exceptions.Value(f"Busy, try again later")
        return wallet

    def _activate_account(self, address):
        wallet = self._get_wallet()
        tftasset = wallet._get_asset()

        source_account = wallet.load_account()

        transaction = (
            stellar_sdk.TransactionBuilder(
                source_account=source_account,
                network_passphrase=self._get_network_passphrase(wallet.network.value),
                base_fee=_MAX_FEE,
            )
            .append_begin_sponsoring_future_reserves_op(address)
            .append_create_account_op(destination=address, starting_balance="0")
            .append_change_trust_op(stellar_sdk.Asset(tftasset.code,tftasset.issuer), source=address)
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

    @actor_method
    def fund_trustline(self, address: str, asset: str)->dict:

        wallet = self._get_wallet()
        if asset not in SUPPORTED_ASSETS[str(wallet.network.value)]:
            raise j.exceptions.NotFound("Unsupported asset")

        asset_code, asset_issuer = asset.split(":")

        source_account = wallet.load_account()

        transaction = (
            stellar_sdk.TransactionBuilder(
                source_account=source_account,
                network_passphrase=self._get_network_passphrase(wallet.network.value),
                base_fee=_MAX_FEE,
            )
            .append_begin_sponsoring_future_reserves_op(address)
            .append_change_trust_op(stellar_sdk.Asset(asset_code,asset_issuer), source=address)
            .append_end_sponsoring_future_reserves_op(address)
            .set_timeout(60)
            .build()
        )
        source_keypair = stellar_sdk.Keypair.from_secret(wallet.secret)
        transaction.sign(source_keypair)
        return {"addtrustline_transaction":transaction.to_xdr()}


Actor = ActivationService
