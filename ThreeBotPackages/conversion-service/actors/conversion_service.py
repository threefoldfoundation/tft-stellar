from Jumpscale import j
import time
import json
import binascii
import base64
import math
import gevent
from datetime import datetime


_TFT_FULL_ASSETCODES = {
    "TEST": "TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3",
    "STD": "TFT:GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
}

_TFTA_FULL_ASSETCODES = {
    "TEST": "TFTA:GB55A4RR4G2MIORJTQA4L6FENZU7K4W7ATGY6YOT2CW47M5SZYGYKSCT",
    "STD": "TFTA:GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2",
}


class conversion_service(j.baseclasses.threebot_actor):
    def _init(self, **kwargs):
        self.converted_addresses_model = j.tools.threebot_packages.threefoldfoundation__unlock_service.bcdb_model_get(
            url="threefoldfoundation.conversion_service.converted_address"
        )

    def _stellar_address_used_before(self, stellar_address):
        try:
            stellar_client = self.package_author.conversion_wallet
            from stellar_sdk.exceptions import NotFoundError

            stellar_client.list_transactions(address=stellar_address)
        except NotFoundError:
            return False
        else:
            return True

    def _stellar_address_to_tfchain_address(self, stellar_address):
        from JumpscaleLibs.clients.tfchain.types.CryptoTypes import PublicKey, PublicKeySpecifier
        from stellar_sdk import strkey

        raw_public_key = strkey.StrKey.decode_ed25519_public_key(stellar_address)
        rivine_public_key = PublicKey(PublicKeySpecifier.ED25519, raw_public_key)
        return str(rivine_public_key.unlockhash)

    def _is_zero_balance_tfchain(self, tfchain_address):
        tfchain_client = j.clients.tfchain.get("tfchain")
        # get balance from tfchain
        result = tfchain_client.unlockhash_get(tfchain_address)
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

    @j.baseclasses.actor_method
    def activate_account(self, address, tfchain_address, schema_out=None, user_session=None):
        
        if tfchain_address != self._stellar_address_to_tfchain_address(address):
            raise j.exceptions.Base("The stellar and tfchain addresses are not created from the same private key")
        if self._is_zero_balance_tfchain(tfchain_address):
            raise j.exceptions.Base("Tfchain address has 0 balance, no need to activate an account")
        if self._stellar_address_used_before(address):
            raise j.exceptions.Base("This address is not new")

        return self.package_author.activate_account(address)
    

    def _address_converted_before(self, address: str):
        convertedaddresses = self.converted_addresses_model.find(stellaraddress=address)
        if convertedaddresses:
            return True
        converted_address = self.converted_addresses_model.new()
        converted_address.stellaraddress = address
        converted_address.save()
        return False

    @j.baseclasses.actor_method
    def migrate_tokens(self, tfchain_address, stellar_address, schema_out=None, user_session=None):
        converter_wallet = self.package_author.conversion_wallet
        tfchain_client = j.clients.tfchain.get("tfchain")

        # Check after getting the wallets so all required imports are certainly met
        if tfchain_address != self._stellar_address_to_tfchain_address(stellar_address):
            raise j.exceptions.Base("The stellar and tfchain addresses are not created from the same private key")

        asset = _TFTA_FULL_ASSETCODES[str(converter_wallet.network)]

        # get balance from tfchain
        unlockhash = tfchain_client.unlockhash_get(tfchain_address)
        balance = unlockhash.balance()

        is_authorized = tfchain_client.authcoin.is_authorized(unlockhash.unlockhash)

        if is_authorized:
            raise j.exceptions.Base("Tfchain addressess should be deauthorized first before migrating to Stellar")

        memo_hash = None
        sorted_transactions = sorted(unlockhash.transactions, key=lambda tx: tx.height, reverse=True)
        for tx in sorted_transactions:
            if tx.version.value == 176:
                memo_hash = tx.id

        if memo_hash is None:
            raise j.exceptions.Base("Deathorization transaction is still being processed")

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
        if self.package_author.db_pool.apply(self._address_converted_before, (stellar_address,)):
            raise j.exceptions.Base("Migration already executed for address")

        # check the stellar network to be sure
        def decode_memo_hash(memo_hash):
            try:
                return binascii.hexlify(base64.b64decode(memo_hash)).decode("utf-8")
            except Exception:
                raise j.exceptions.Base("Decoding memo hash failed")

        tft_asset_issuer = _TFT_FULL_ASSETCODES[str(converter_wallet.network)].split(":")[1]
        tfta_asset_issuer = _TFTA_FULL_ASSETCODES[str(converter_wallet.network)].split(":")[1]
        for asset_issuer in (tfta_asset_issuer, tft_asset_issuer):
            converter_transactions = converter_wallet.list_transactions(asset_issuer)
            for converter_tx in converter_transactions:
                if converter_tx.memo_hash is None:
                    continue
                converter_tx_decoded_memo_hash = decode_memo_hash(converter_tx.memo_hash)
                if memo_hash == converter_tx_decoded_memo_hash:
                    raise j.exceptions.Base("Migration already executed for address")

        if not unlocked_tokens.is_zero():
            self.package_author.transfer(stellar_address, "{0:.7f}".format(unlocked_tokens), asset, memo_hash=memo_hash)

        if not locked_tokens.is_zero():
            conversion_group = gevent.pool.Group()
            for tx in unlockhash.transactions:
                for coin_output in tx.coin_outputs:
                    lock_time = coin_output.condition.lock.value
                    if lock_time == 0:
                        break
                    lock_time_date = datetime.fromtimestamp(lock_time)
                    # if lock time year is before 2021 be convert to TFTA
                    if lock_time_date.year < 2021:
                        asset = _TFTA_FULL_ASSETCODES[str(converter_wallet.network)]
                    # else we convert to TFT
                    else:
                        asset = _TFT_FULL_ASSETCODES[str(converter_wallet.network)]

                    if time.time() < lock_time:
                        conversion_group.apply_async(
                            self.package_author.transfer,
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
