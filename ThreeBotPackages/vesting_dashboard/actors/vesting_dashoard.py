import os
import sys
import time

import stellar_sdk
from stellar_sdk.exceptions import Ed25519PublicKeyInvalidError, BadRequestError, SdkError
from jumpscale.core.exceptions import JSException
from jumpscale.loader import j
from jumpscale.servers.gedis.baseactor import BaseActor, actor_method
from jumpscale.core.base import StoredFactory

current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../models/")
from models import VestingEntry

vesting_entry_model = StoredFactory(VestingEntry)
vesting_entry_model.always_reload = True


class VestingDashboard(BaseActor):
    @actor_method
    def create_escrow_account(self, owner_address: str) -> str:
        # TODO
        vesting_account = ""
        j.data.serializers.json.dumps({"data": vesting_account})

    @actor_method
    def list_vesting_accounts(self, owner_address: str) -> str:
        # TODO
        vesting_accounts = []
        j.data.serializers.json.dumps({"data": vesting_accounts})


Actor = VestingDashboard
