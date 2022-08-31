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

from tfchainmigration_sal import activate_account as activate_account_sal, get_wallet
from tfchaintypes.CryptoTypes import PublicKey, PublicKeySpecifier
from tfchainexplorer import unlockhash_get

TFCHAIN_EXPLORER = "https://explorer2.threefoldtoken.com"


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

    
    @actor_method
    def migrate_tokens(self, tfchain_address=None, stellar_address=None, args: dict = None) -> str:
        raise j.exceptions.Value(f"Contact support for tfchain to stellar migrations") 
       


Actor = TFchainmigration_service
