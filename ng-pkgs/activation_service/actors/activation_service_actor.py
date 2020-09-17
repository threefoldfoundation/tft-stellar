import os
import sys

import stellar_sdk
from jumpscale.core.exceptions import JSException
from jumpscale.loader import j
from jumpscale.servers.gedis.baseactor import BaseActor, actor_method


current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../sals/")
from activation_sal import activate_account as activate_account_sal

activation_wallet = j.clients.stellar.get("activation_wallet")


class ActivationService(BaseActor):
    def _stellar_address_used_before(self, stellar_address):
        try:
            transactions = activation_wallet.list_transactions(address=stellar_address)
            return len(transactions) != 0
        except stellar_sdk.exceptions.NotFoundError:
            return False

    def _activate_account(self, address):
        if self._stellar_address_used_before(address):
            raise j.exceptions.Base("This address is not new")
        activate_account_sal(address)

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
