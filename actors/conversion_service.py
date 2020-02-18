from Jumpscale import j
from decimal import Decimal, getcontext
import time
import gevent


class Conversion_service(j.baseclasses.threebot_actor):
    @j.baseclasses.actor_method
    def activate_account(self, address, schema_out=None, user_session=None):
        converter = j.clients.stellar.get("converter")
        return converter.activate_account(address)

    @j.baseclasses.actor_method
    def transfer_tokens(self, threefold_address, stellar_address, asset_code, issuer, schema_out=None, user_session=None):
        if asset_code == "":
            raise Exception("Asset code should be a valid string")
        if issuer == "":
            raise Exception("Issuer should be a valid string")

        asset = asset_code + ":" + issuer

        converter = j.clients.stellar.get("converter")
        tfchain_client = j.clients.tfchain.get("tfchain")

        # get balance from tfchain
        result = tfchain_client.unlockhash_get(threefold_address)
        balance = result.balance()

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
            converter.transfer(stellar_address, unlocked_tokens, asset)

        unlock_tx_xdrs = []
        if not locked_tokens.is_zero():
            for tx in result.transactions:
                for coin_output in tx.coin_outputs:
                    lock_time = coin_output.condition.lock.value
                    if time.time() < lock_time:
                        unlock_tx_xdr = converter.transfer_locked_funds(stellar_address, coin_output.value, asset, lock_time)
                        unlock_tx_xdrs.append(unlock_tx_xdr)

        return unlock_tx_xdrs
