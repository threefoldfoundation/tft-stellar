import os
import sys
import time

import stellar_sdk
from jumpscale.core.exceptions import JSException
from jumpscale.loader import j
from jumpscale.servers.gedis.baseactor import BaseActor, actor_method


current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../sals/")
from vesting_sal import get_wallet


_TFT_ISSUERS = {
    "TEST": "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3",
    "STD": "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
}

_COSIGNERS = {
    "TEST": [
        "GBOZV7I3NJGXIFBMGHTETCY7ZL36QMER25IJGRFEEX3KM36YRUMHEZAP",
        "GCU5OGRCFJ3NWQWUF3A4MAGNYABOPJMCHMXYQ7TC4RQ6IYBIZBEOGN6H",
        "GAK2Q3P3YOAPK6MCM4P3ASDJYSHQ376LIO64CHBXNKIRFZECH2JY2LYX",
        "GALOCGHPJ2KQ67VIZRSLOAPJIBCUL54WG6ZHFDB6AKPIMEQXHU374UCJ",
        "GC3IFIJ7KEOZ5CUZS57HMLJLXISS7N45INIGXO2JFNJBLKOGYTSADFPB",
        "GD56QGOWI5ZRJAXNLMAH6BQ3MQEXNWI5H6Q57BFMOQZKPMRLPIYK4RC6",
        "GAJFU5JCWRVJ5G7HDYSW6NMDSS6XTRPCNEULD5MWCKQEIGFFSJMDZXUA",
        "GDBDJCWCEHLCCJ74HJUDJIBTZO7JVFCI2IIDLEPL33FHOAKVDCNAUE4P",
        "GBMXLD4BEJWWETPCFTO2NI7MFRGGBFZDIOVA7OHHFA5XBTB7YHUQBQME",
    ],
    "STD": [],
}

DATA_ENTRY_KEY = "tft-vesting"


class VestingService(BaseActor):
    def _get_network(self) -> str:
        return str(get_wallet().network.value)

    def _get_network_passphrase(self) -> str:
        if self._get_network() == "TEST":
            return stellar_sdk.Network.TESTNET_NETWORK_PASSPHRASE
        return stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE

    def _get_horizon_server(self) -> stellar_sdk.Server:
        return get_wallet()._get_horizon_server()

    def _get_tft_issuer(self) -> str:
        return _TFT_ISSUERS[self._get_network()]

    def _get_cosigners(self) -> list:
        return _COSIGNERS[self._get_network()]

    def _create_recovery_transaction(self, vesting_address: str) -> stellar_sdk.TransactionEnvelope:
        activation_account_id = get_wallet().address
        horizon_server = self._get_horizon_server()
        source_account = horizon_server.load_account(vesting_address)
        source_account.sequence += 1
        tx = stellar_sdk.TransactionBuilder(source_account, network_passphrase=self._get_network_passphrase())
        tx.append_change_trust_op(asset_code="TFT", asset_issuer=self._get_tft_issuer(), limit="0")
        tx.append_manage_data_op(DATA_ENTRY_KEY, None)
        tx.append_account_merge_op(activation_account_id)
        txe = tx.build()
        # TODO: set minium timebound to two weeks from now

        # save the preauth transaction in our unlock service
        unlock_hash_signer = stellar_sdk.strkey.StrKey.encode_pre_auth_tx(txe.hash())
        data = {"unlockhash": unlock_hash_signer, "transaction_xdr": txe.to_xdr()}
        url = f"https://{'testnet.threefold.io' if self._get_network()=='TEST' else'tokenservices.threefold.io'}/threefoldfoundation/unlock_service/create_unlockhash_transaction"
        resp = j.tools.http.post(url, json={"args": data})
        resp.raise_for_status()
        return txe

    def _create_vesting_account(self, owner_address) -> str:

        escrow_kp = stellar_sdk.Keypair.random()
        escrow_address = escrow_kp.public_key
        # TODO: serialize with a gevent pool

        wallet = get_wallet()
        activation_account = wallet.load_account()
        if not activation_account.last_created_sequence_is_used:
            if (wallet.sequencedate + 30) > int(time.time()):
                raise j.exceptions.Value(f"Busy, try again later")

        if not wallet:
            raise j.exceptions.Value("Service unavailable")
        tftasset = wallet._get_asset()

        horizon_server = self._get_horizon_server()

        base_fee = horizon_server.fetch_base_fee()

        txb = (
            stellar_sdk.TransactionBuilder(activation_account, network_passphrase=self._get_network_passphrase())
            .append_create_account_op(escrow_address, starting_balance="7.6")
            .append_change_trust_op("TFT", self._get_tft_issuer(), source=escrow_address)
        )
        activation_kp = stellar_sdk.Keypair.from_secret(wallet.secret)

        tx = txb.build()
        tx.sign(activation_kp)
        tx.sign(escrow_kp)
        horizon_server.submit_transaction(tx)
        # TODO: try except and clean up the unfinished vesting account
        vesting_account = horizon_server.load_account(escrow_address)
        txb = stellar_sdk.TransactionBuilder(
            vesting_account, network_passphrase=self._get_network_passphrase()
        ).append_ed25519_public_key_signer(owner_address, weight=5, source=escrow_address)
        recovery_transaction = self._create_recovery_transaction(escrow_address)
        # TODO: publish recovery transaction
        print(f"Recovery transaction:\n{recovery_transaction.to_xdr()}")
        txb.append_pre_auth_tx_signer(recovery_transaction.hash(), weight=10, source=escrow_address)
        for cosigner in self._get_cosigners():
            txb.append_ed25519_public_key_signer(cosigner, weight=1, source=escrow_address)
        txb.append_manage_data_op(DATA_ENTRY_KEY, "here comes the formula or reference", source=escrow_address)
        txb.append_set_options_op(
            master_weight=0, low_threshold=10, med_threshold=10, high_threshold=10, source=escrow_address
        )

        tx = txb.build()
        tx.sign(escrow_kp)
        horizon_server.submit_transaction(tx)
        return escrow_address

    @actor_method
    def create_vesting_account(self, owner_address: str) -> dict:
        escrow_address = self._create_vesting_account(owner_address)
        return {"address": escrow_address}


Actor = VestingService
