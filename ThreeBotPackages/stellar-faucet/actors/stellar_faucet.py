from Jumpscale import j
from urllib.request import urlopen
import nacl
import json
import base64


class stellar_faucet(j.baseclasses.threebot_actor):
    @j.baseclasses.actor_method
    def transfer(self, destination, signed_attempt_object, schema_out=None, user_session=None):
        if not is_3bot_user(signed_attempt_object):
            raise Exception("not a valid user")
        
        distributor = j.clients.stellar.get("distributor")

        distributor.network = self.package.install_kwargs.get("network")
        distributor.secret = self.package.install_kwargs.get("secret")

        asset = self.package.install_kwargs.get("asset")
        amount = self.package.install_kwargs.get("amount")

        double_name = signed_attempt_object["doubleName"]
        txes = distributor.list_transaction(address=destination)
        for tx in txes:
            if tx.memo_text == double_name:
                raise Exception("user already requested token")

        try:
            distributor.transfer(destination_address=destination, amount=amount, asset=asset, memo_text=double_name)
        except Exception as e:
            raise e

    def is_3bot_user(signed_attempt_object):
        auth_response = urlopen("https://login.threefold.me/api/users/{}".format(signed_attempt_object["doubleName"]))
        data = json.loads(auth_response.read())
        user_public = data['publicKey']
        verify_key = nacl.signing.VerifyKey(user_public, encoder=nacl.encoding.Base64Encoder)

        try:
            verify_key.verify(base64.b64decode(signed_attempt_object["signedAttempt"]))
        except:
            return False
        return True