import stellar_sdk

from jumpscale.loader import j
from jumpscale.servers.gedis.baseactor import BaseActor, actor_method
from jumpscale.core.exceptions import JSException
from jumpscale.clients.stellar.stellar import Stellar

stellar_client = Stellar()

class ActivationService(BaseActor):

    def _stellar_address_used_before(self, stellar_address):
        try:
            transactions = stellar_client.list_transactions(address=stellar_address)
            return len(transactions)!=0
        except stellar_sdk.exceptions.NotFoundError:
            return False

    def _activate_account(self, address):
        if self._stellar_address_used_before(address):
            raise j.exceptions.Base("This address is not new")
        stellar_client.activate_account(address)
    
    @actor_method
    def create_activation_code(self, address: str) -> str:
        self._activate_account(address)
        response = j.data.serializers.json.dumps(
            {"activation_code": "abcd", "address": address, "phonenumbers": ["+1234567890"]}
        )
        return response

    @actor_method
    def activate_account(self, activation_code: str) -> str:
        return None

Actor = ActivationService
