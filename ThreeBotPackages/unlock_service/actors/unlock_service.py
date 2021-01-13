import os
import sys
from jumpscale.loader import j
from jumpscale.core.base import StoredFactory
from jumpscale.servers.gedis.baseactor import BaseActor, actor_method


current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../models/")
from models import UnlockhashTransaction

unlock_transaction_hash_model = StoredFactory(UnlockhashTransaction)
unlock_transaction_hash_model.always_reload = True


class unlock_service(BaseActor):
    @actor_method
    def create_unlockhash_transaction(
        self, unlockhash: str = None, transaction_xdr: str = None, args: dict = None
    ) -> str:
        """
        param:unlockhash (str)
        param:transaction_xdr (str)

        return: unlockhash_transaction obj dict

        """
        # Backward compatibility with jsx service for request body {'args': ....}
        if (not unlockhash or not transaction_xdr) and not args:
            raise j.exceptions.Value(f"missing a required argument: 'unlockhash' and 'transaction_xdr'")
        if args:
            try:
                if "unlockhash" in args:
                    unlockhash = args.get("unlockhash", None)
                else:
                    raise j.exceptions.Value(f"missing a required argument: 'unlockhash' in args dict")
                if "transaction_xdr" in args:
                    transaction_xdr = args.get("transaction_xdr", None)
                else:
                    raise j.exceptions.Value(f"missing a required argument: 'transaction_xdr' in args dict")
            except j.data.serializers.json.json.JSONDecodeError:
                pass
        unlockhash_transaction = unlock_transaction_hash_model.new(unlockhash)

        unlockhash_transaction.unlockhash = unlockhash
        unlockhash_transaction.transaction_xdr = transaction_xdr

        unlockhash_transaction.save()

        return j.data.serializers.json.dumps(unlockhash_transaction.to_dict())

    @actor_method
    def get_unlockhash_transaction(self, unlockhash: str = None, args: dict = None) -> str:
        """
        param:unlockhash (str)

        return: unlockhash_transaction obj dict

        """
        # Backward compatibility with jsx service for request body {'args': ....}
        if not unlockhash and not args:
            raise j.exceptions.Value(f"missing a required argument: 'unlockhash'")
        if args:
            try:
                if "unlockhash" in args:
                    unlockhash = args.get("unlockhash", None)
                else:
                    raise j.exceptions.Value(f"missing a required argument: 'unlockhash' in args dict")
            except j.data.serializers.json.json.JSONDecodeError:
                pass
        try:
            if unlockhash not in unlock_transaction_hash_model.list_all():
                raise j.exceptions.NotFound("Transaction not found")
            transactions = unlock_transaction_hash_model.find_many(unlockhash=unlockhash)
            for transaction in transactions[2]:
                if transaction:
                    return j.data.serializers.json.dumps(transaction.to_dict())
        except j.exceptions.NotFound:
            raise j.exceptions.NotFound("unlocktransaction with hash %s not found" % unlockhash)


Actor = unlock_service
