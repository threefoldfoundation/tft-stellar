import os
import sys

import stellar_sdk
from stellar_sdk.exceptions import Ed25519PublicKeyInvalidError, BadRequestError, SdkError
from jumpscale.core.exceptions import JSException
from jumpscale.loader import j
from jumpscale.servers.gedis.baseactor import BaseActor, actor_method


current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../sals/")
from activation_sal import activate_account as activate_account_sal, get_wallet



class ActivationService(BaseActor):
    def _stellar_address_used_before(self, stellar_address):
        try:
            transactions = get_wallet().list_transactions(address=stellar_address)
            return len(transactions) != 0
        except stellar_sdk.exceptions.NotFoundError:
            return False

    def _activate_account(self, address, token):
        if self._stellar_address_used_before(address):
            raise j.exceptions.Value("This address is not new")
        activate_account_sal(address, token)

    @actor_method
    def create_activation_code(self, address: str = None, token: str = None, args: dict = None) -> str:
        # Backward compatibility with jsx service for request body {'args': {'address': <address>}}
        if not args:
            if not address:
                raise j.exceptions.Value(f"missing a required argument: 'address'")
            if not token:
                raise j.exceptions.Value(f"missing a required argument: 'token'")
        else:
            try:
                if "address" not in args:
                    raise j.exceptions.Value(f"missing a required argument: 'address' in args dict")
                elif "token" not in args:
                    raise j.exceptions.Value(f"missing a required argument: 'token' in args dict")
                else:
                    address = args.get("address", None)
                    token = args.get("token", None)
            except j.data.serializers.json.json.JSONDecodeError:
                pass

        try:
            self._activate_account(address, token)
            response = j.data.serializers.json.dumps(
                {"activation_code": "abcd", "address": address, "phonenumbers": ["+1234567890"]}
            )
            return response
        except (Ed25519PublicKeyInvalidError, BadRequestError):
            raise j.exceptions.Value(f"Address is invalid")
        except SdkError as e:
            # Return a stellar sdk related error
            raise j.exceptions.Value(f'{{"Stellar sdk error":{(e)}}}')
        except j.exceptions.JSException as e:
            # Return JS exception
            raise j.exceptions.Value(e)

    @actor_method
    def activate_account(self, activation_code: str) -> str:
        return None


Actor = ActivationService
