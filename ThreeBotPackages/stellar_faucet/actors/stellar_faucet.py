from Jumpscale import j
from urllib.request import urlopen
import nacl
import json
import base64


class stellar_faucet(j.baseclasses.threebot_actor):
    @j.baseclasses.actor_method
    def transfer(self, destination, signed_attempt_object, schema_out=None, user_session=None):
        if not self.is_3bot_user(signed_attempt_object):
            raise Exception("not a valid user")

        walletname = self.package.install_kwargs.get("wallet", "faucetwallet")
        distributor = j.clients.stellar.get(walletname)

        asset = self.package.install_kwargs.get("asset", "TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3")
        amount = self.package.install_kwargs.get("amount", "1000")

        double_name = signed_attempt_object["doubleName"]
        hashed_double_name = nacl.hash.blake2b(double_name.encode("utf-8"), encoder=nacl.encoding.RawEncoder)
        txes = distributor.list_transactions(address=destination)
        for tx in txes:
            if tx.memo_hash is not None:
                decoded_memo_hash = base64.b64decode(tx.memo_hash)
                if decoded_memo_hash == hashed_double_name:
                    raise j.exceptions.Base("user already requested tokens")

        try:
            distributor.transfer(
                destination_address=destination, amount=amount, asset=asset, memo_hash=hashed_double_name
            )
        except Exception as e:
            raise j.exceptions.Base(e)

    def is_3bot_user(self, signed_attempt_object):
        auth_response = urlopen("https://login.threefold.me/api/users/{}".format(signed_attempt_object["doubleName"]))
        data = json.loads(auth_response.read())
        user_public = data["publicKey"]
        verify_key = nacl.signing.VerifyKey(user_public, encoder=nacl.encoding.Base64Encoder)

        try:
            verify_key.verify(base64.b64decode(signed_attempt_object["signedAttempt"]))
        except:
            return False
        return True
