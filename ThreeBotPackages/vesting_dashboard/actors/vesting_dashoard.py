import os
import sys
import time

import stellar_sdk
from stellar_sdk.exceptions import Ed25519PublicKeyInvalidError, BadRequestError, SdkError
from jumpscale.core.exceptions import JSException
from jumpscale.loader import j
from jumpscale.servers.gedis.baseactor import BaseActor, actor_method

from .models import VestingEntry
from jumpscale.core.base import StoredFactory


class VestingDashboard(BaseActor):
    @actor_method
    def create_escrow_account(self, owner_address: str) -> str:
        vesting_factory = StoredFactory(VestingEntry)
        # TODO
        vesting_account = ""
        j.data.serializers.json.dumps({"data": vesting_account})

    @actor_method
    def list_vesting_accounts(self, owner_address: str) -> str:
        vesting_factory = StoredFactory(VestingEntry)
        # TODO
        vesting_accounts = []
        j.data.serializers.json.dumps({"data": vesting_accounts})


Actor = VestingDashboard
