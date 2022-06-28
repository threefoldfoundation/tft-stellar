import time
import json
import binascii
import base64
import math
import gevent
import requests
from datetime import datetime

import os
import sys

import stellar_sdk
from stellar_sdk.exceptions import NotFoundError
from stellar_sdk import strkey
from jumpscale.loader import j
from jumpscale.servers.gedis.baseactor import BaseActor, actor_method


CURRENT_FULL_PATH = os.path.dirname(os.path.abspath(__file__))
sals_path = CURRENT_FULL_PATH + "/../sals/"
lib_path = CURRENT_FULL_PATH + "/../../../lib/"
sys.path.extend([sals_path, lib_path])

from tfchainmigration_sal import activate_account as activate_account_sal, get_wallet, CONVERTED_ADDRESS_MODEL, db_pool
from tfchaintypes.CryptoTypes import PublicKey, PublicKeySpecifier
from tfchainexplorer import unlockhash_get, ExplorerUnlockhashResult

TFCHAIN_EXPLORER = "https://explorer2.threefoldtoken.com"

_TFT_FULL_ASSETCODES = {
    "TEST": "TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3",
    "STD": "TFT:GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
}

_TFTA_FULL_ASSETCODES = {
    "TEST": "TFTA:GB55A4RR4G2MIORJTQA4L6FENZU7K4W7ATGY6YOT2CW47M5SZYGYKSCT",
    "STD": "TFTA:GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2",
}


class TFchainmigration_service(BaseActor):
    def _stellar_address_used_before(self, stellar_address):
        try:
            stellar_client = get_wallet()

            transactions = stellar_client.list_transactions(address=stellar_address)
            return len(transactions) != 0
        except NotFoundError:
            return False

    def _stellar_address_to_tfchain_address(self, stellar_address):
        raw_public_key = strkey.StrKey.decode_ed25519_public_key(stellar_address)
        rivine_public_key = PublicKey(PublicKeySpecifier.ED25519, raw_public_key)
        return str(rivine_public_key.unlockhash)

    def _is_zero_balance_tfchain(self, tfchain_address):
        # get balance from tfchain
        result = unlockhash_get(tfchain_address)
        if result is None:
            return True
        balance = result.balance()

        unlocked_tokens = balance.available.value
        locked_tokens = balance.locked.value
        unconfirmed_unlocked_tokens = balance.unconfirmed.value
        unconfirmed_locked_tokens = balance.unconfirmed_locked.value

        if (
            unlocked_tokens.is_zero()
            & locked_tokens.is_zero()
            & unconfirmed_unlocked_tokens.is_zero()
            & unconfirmed_locked_tokens.is_zero()
        ):
            return True
        else:
            return False

    def _transfer(self, destination_address, amount, asset: str, locked_until=None, memo_hash=None):
        issuer_address = asset.split(":")[1]
        converter_wallet = get_wallet()
        return converter_wallet.transfer(
            destination_address,
            amount,
            asset,
            locked_until,
            memo_hash=memo_hash,
            fund_transaction=False,
            from_address=issuer_address,
        )

    def transfer(self, destination_address, amount, asset: str, locked_until=None, memo_hash=None):
        if locked_until:
            return self._transfer_locked_tokens(destination_address, amount, asset, locked_until, memo_hash)
        else:
            asset_code = asset.split(":")[0]
            pool = self._tft_issuing_pool if asset_code == "TFT" else self._tfta_issuing_pool
            return pool.apply(self._transfer, args=(destination_address, amount, asset, locked_until, memo_hash))

    def _transfer_locked_tokens(self, destination_address, amount, asset: str, locked_until=None, memo_hash=None):
        asset_code = asset.split(":")[0]
        asset_issuer = asset.split(":")[1]
        import stellar_sdk

        escrow_kp = stellar_sdk.Keypair.random()

        # delegate to the activation pool
        activate_account_sal(escrow_kp.public_key)
        conversion_wallet = get_wallet()
        # no problem using the conversion wallet, just use it's code
        conversion_wallet.add_trustline(asset_code, asset_issuer, escrow_kp.secret)
        preauth_tx = conversion_wallet._create_unlock_transaction(escrow_kp, locked_until)
        preauth_tx_hash = preauth_tx.hash()
        unlock_hash = stellar_sdk.strkey.StrKey.encode_pre_auth_tx(preauth_tx_hash)
        conversion_wallet._create_unlockhash_transaction(unlock_hash=unlock_hash, transaction_xdr=preauth_tx.to_xdr())
        conversion_wallet._set_escrow_account_signers(
            escrow_kp.public_key, destination_address, preauth_tx_hash, escrow_kp
        )

        # delegate to the issuing pool
        self.transfer(escrow_kp.public_key, amount, asset, memo_hash=memo_hash)

        return preauth_tx.to_xdr()

    @actor_method
    def activate_account(self, address=None, tfchain_address=None, args: dict = None):
        # Backward compatibility with jsx service for request body {'args': {'address': <address>}}
        if not tfchain_address and not address and not args:
            raise j.exceptions.Value(f"missing a required argument: 'tfchain_address' and 'address' ")
        if args:
            try:
                if "tfchain_address" in args:
                    tfchain_address = args.get("tfchain_address", None)
                else:
                    raise j.exceptions.Value(f"missing a required argument: 'tfchain_address' in args dict")
                if "address" in args:
                    address = args.get("address", None)
                else:
                    raise j.exceptions.Value(f"missing a required argument: 'address' in args dict")
            except j.data.serializers.json.json.JSONDecodeError:
                pass

        if tfchain_address != self._stellar_address_to_tfchain_address(address):
            raise j.exceptions.Value("The stellar and tfchain addresses are not created from the same private key")
        if self._is_zero_balance_tfchain(tfchain_address):
            raise j.exceptions.Value("Tfchain address has 0 balance, no need to activate an account")
        if self._stellar_address_used_before(address):
            raise j.exceptions.Value("This address is not new")

        return activate_account_sal(address)

    def _address_converted_before(self, address: str):
        if address in CONVERTED_ADDRESS_MODEL.list_all():
            return True
        converted_address = CONVERTED_ADDRESS_MODEL.new(address)
        converted_address.stellaraddress = address
        converted_address.save()
        return False

    def _is_authorized(self, tfchain_address : str):
        """
        Query the explorer backend to see if an address is currently authorized.
        @param tfchain_address: tfchain_address for which to look up the authorizaton state
        """
        # define endpoint
        endpoint = f"/explorer/authcoin/status?addr={tfchain_address}"
        # parse response, this returns an array of json booleans
        resp = requests.get(TFCHAIN_EXPLORER + endpoint)
        resp=resp.json()

        try:
            # we only check 1 address in this function
            # so it's always index 0 we are interested in.
            return resp["auths"][0]
        except (KeyError, IndexError) as exc:
            # invalid explorer response
            raise j.exceptions.Value(str(exc))

    @actor_method
    def migrate_tokens(self, tfchain_address=None, stellar_address=None, args: dict = None) -> str:
        # Backward compatibility with jsx service for request body {'args': {'address': <address>}}
        if not tfchain_address and not stellar_address and not args:
            raise j.exceptions.Value(f"missing a required argument: 'tfchain_address' and 'stellar_address' ")
        if args:
            try:
                if "tfchain_address" in args:
                    tfchain_address = args.get("tfchain_address", None)
                else:
                    raise j.exceptions.Value(f"missing a required argument: 'tfchain_address' in args dict")
                if "stellar_address" in args:
                    stellar_address = args.get("stellar_address", None)
                else:
                    raise j.exceptions.Value(f"missing a required argument: 'stellar_address' in args dict")
            except j.data.serializers.json.json.JSONDecodeError:
                pass

        # Check after getting the wallets so all required imports are certainly met
        if tfchain_address != self._stellar_address_to_tfchain_address(stellar_address):
            raise j.exceptions.Value("The stellar and tfchain addresses are not created from the same private key")

        network = str(get_wallet().network.value)

        asset = _TFT_FULL_ASSETCODES[network]

        # get balance from tfchain
        unlockhash = unlockhash_get(tfchain_address)
        if unlockhash is None:
            return json.dumps([])  # nothing to do

        balance = unlockhash.balance()

        if self._is_authorized(tfchain_address):
            raise j.exceptions.Value("Tfchain addressess should be deauthorized first before migrating to Stellar")

        memo_hash = None
        sorted_transactions = sorted(unlockhash.transactions, key=lambda tx: tx.height, reverse=True)
        for tx in sorted_transactions:
            if tx.version.value == 176: # deauthorization transaction
                memo_hash = tx.id

        if memo_hash is None:
            raise j.exceptions.Value("Deauthorization transaction is still being processed")

        unlocked_tokens = balance.available.value
        locked_tokens = balance.locked.value

        unconfirmed_unlocked_tokens = balance.unconfirmed.value
        unconfirmed_locked_tokens = balance.unconfirmed_locked.value

        if not unconfirmed_unlocked_tokens.is_zero():
            raise Exception("Can't migrate right now, address had unconfirmed unlocked balance.")

        if not unconfirmed_locked_tokens.is_zero():
            raise Exception("Can't migrate right now, address had unconfirmed locked balance.")

        # check if the conversion already happened
        # First look in our internal db
        if db_pool.apply(self._address_converted_before, (stellar_address,)):
            raise j.exceptions.Value("Migration already executed for address")

        # check the stellar network to be sure
        def decode_memo_hash(memo_hash):
            try:
                return binascii.hexlify(base64.b64decode(memo_hash)).decode("utf-8")
            except Exception:
                raise j.exceptions.Value("Decoding memo hash failed")

        tft_asset_issuer = _TFT_FULL_ASSETCODES[network].split(":")[1]
        tfta_asset_issuer = _TFTA_FULL_ASSETCODES[network].split(":")[1]
        for asset_issuer in (tfta_asset_issuer, tft_asset_issuer):
            converter_transactions = get_wallet().list_transactions(asset_issuer)
            for converter_tx in converter_transactions:
                if converter_tx.memo_hash is None:
                    continue
                converter_tx_decoded_memo_hash = decode_memo_hash(converter_tx.memo_hash)
                if memo_hash == converter_tx_decoded_memo_hash:
                    raise j.exceptions.Value("Migration already executed for address")

        if not unlocked_tokens.is_zero():
            self.transfer(stellar_address, "{0:.7f}".format(unlocked_tokens), asset, memo_hash=memo_hash)

        if not locked_tokens.is_zero():
            conversion_group = gevent.pool.Group()
            for tx in unlockhash.transactions:
                for coin_output in tx.coin_outputs:
                    if str(coin_output.condition.unlockhash) != tfchain_address:
                        continue
                    lock_time = coin_output.condition.lock.value
                    if lock_time == 0:
                        continue

                    if time.time() < lock_time:
                        conversion_group.apply_async(
                            self.transfer,
                            (
                                stellar_address,
                                "{0:.7f}".format(coin_output.value.value),
                                asset,
                                math.ceil(lock_time),
                                memo_hash,
                            ),
                        )
            conversion_group.join()
        return json.dumps([])


Actor = TFchainmigration_service
