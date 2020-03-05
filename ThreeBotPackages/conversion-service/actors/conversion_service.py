from Jumpscale import j
from decimal import Decimal, getcontext
import time
import json


_TFT_FULL_ASSETCODES={"TEST":"TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3","STD":"TFT:issuertobefilledin"}

class conversion_service(j.baseclasses.threebot_actor):


    def _stellar_address_used_before(self, stellar_address):
        try:
           stellar_client= j.clients.stellar.get("converter")
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


    @j.baseclasses.actor_method
    def activate_account(self, address, tfchain_address, schema_out=None, user_session=None):
        if self._stellar_address_used_before(address):
           raise j.exceptions.Base("This address is not new")
        if tfchain_address != self._stellar_address_to_tfchain_address(address):
            raise j.exceptions.Base("The stellar and tfchain addresses are not created from the same private key")
        converter = j.clients.stellar.get("converter")
        return converter.activate_account(address, starting_balance="2.6")

    @j.baseclasses.actor_method
    def migrate_tokens(self, tfchain_address, stellar_address, schema_out=None, user_session=None):
        converter_wallet = j.clients.stellar.get("converter")
        tfchain_client = j.clients.tfchain.get("tfchain")

        #Check after getting the wallets so all required imports are certainly met
        if tfchain_address != self._stellar_address_to_tfchain_address(stellar_address):
            raise j.exceptions.Base("The stellar and tfchain addresses are not created from the same private key")

        asset = _TFT_FULL_ASSETCODES[str(converter_wallet.network)]

        # get balance from tfchain
        unlockhash = tfchain_client.unlockhash_get(tfchain_address)
        balance = unlockhash.balance()

        is_authorized = tfchain_client.authcoin.is_authorized(unlockhash.unlockhash)

        if is_authorized:
            raise j.exceptions.Base("Tfchain addressess should be deauthorized first before migrating to Stellar!")

        memo_text = None
        sorted_transactions = sorted(unlockhash.transactions, key=lambda tx: tx.height, reverse=True)
        for tx in sorted_transactions:
            if tx.version.value == 176:
                memo_text = tx.id

        if memo_text is None:
            raise j.exceptions.Base("For some reason ")

        stellar_transactions = converter_wallet.list_transactions(address=stellar_address)
        for stellar_tx in stellar_transactions:
            if stellar_tx.memo_text == memo_text:
                converter_transactions = converter_wallet.list_transactions()
                # double check if the transaction also already exists in the converter wallet transactions
                for converter_tx in converter_transactions:
                    if memo_text == converter_tx.memo_text:
                        raise j.exceptions.Base("Migration already executed for address")

        # set Decimal precision to 7
        getcontext().prec = 7

        unlocked_tokens = balance.available.value
        locked_tokens = balance.locked.value

        unconfirmed_unlocked_tokens = balance.unconfirmed.value
        unconfirmed_locked_tokens = balance.unconfirmed_locked.value

        if not unconfirmed_unlocked_tokens.is_zero():
            raise Exception("Can't migrate right now, address had unconfirmed unlocked balance.")

        if not unconfirmed_locked_tokens.is_zero():
            raise Exception("Can't migrate right now, address had unconfirmed locked balance.")

        if not unlocked_tokens.is_zero():
            return converter_wallet.transfer(stellar_address, unlocked_tokens, asset, memo_text=memo_text)

        def format_output(lock_time, unlock_tx_xdr):
            return {"unlocks_at": lock_time, "unlock_tx_xdr": unlock_tx_xdr}

        unlock_tx_xdrs = []
        if not locked_tokens.is_zero():
            for tx in unlockhash.transactions:
                for coin_output in tx.coin_outputs:
                    lock_time = coin_output.condition.lock.value
                    if time.time() < lock_time:
                        unlock_tx_xdr = converter_wallet.transfer(stellar_address, coin_output.value, asset, lock_time, memo_text=memo_text)
                        unlock_tx_xdrs.append(format_output(lock_time, unlock_tx_xdr))

        return json.dumps(unlock_tx_xdrs)