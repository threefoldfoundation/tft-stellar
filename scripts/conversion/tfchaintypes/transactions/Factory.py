import json
from .Base import TransactionBaseClass, TransactionVersion
from .Standard import TransactionV1
from .Minting import TransactionV128, TransactionV129
from .ThreeBot import BotTransactionBaseClass, TransactionV144, TransactionV145, TransactionV146
from .ERC20 import TransactionV208, TransactionV209, TransactionV210
from .Authcoin import TransactionV176, TransactionV177


class TransactionFactory(object):
    """
    TFChain Transaction Factory class
    """

    @classmethod
    def from_json(cls, obj, id=None):
        """
        Create a TFChain transaction from a JSON string or dictionary.

        @param obj: JSON-encoded str, bytes, bytearray or JSON-decoded dict that contains a raw JSON Tx.
        """
        if isinstance(obj, (str, bytes, bytearray)):
            obj = json.loads(obj)
        if not isinstance(obj, dict):
            raise Exception(
                f"only a dictionary or JSON-encoded dictionary is supported as input: type {type(obj)} is not supported"
            )
        tt = obj.get("version", -1)

        txn = None
        if tt == TransactionVersion.STANDARD:
            txn = TransactionV1.from_json(obj)
        elif tt == TransactionVersion.THREEBOT_REGISTRATION:
            txn = TransactionV144.from_json(obj)
        elif tt == TransactionVersion.THREEBOT_RECORD_UPDATE:
            txn = TransactionV145.from_json(obj)
        elif tt == TransactionVersion.THREEBOT_NAME_TRANSFER:
            txn = TransactionV146.from_json(obj)
        elif tt == TransactionVersion.ERC20_CONVERT:
            txn = TransactionV208.from_json(obj)
        elif tt == TransactionVersion.ERC20_COIN_CREATION:
            txn = TransactionV209.from_json(obj)
        elif tt == TransactionVersion.ERC20_ADDRESS_REGISTRATION:
            txn = TransactionV210.from_json(obj)
        elif tt == TransactionVersion.MINTER_DEFINITION:
            txn = TransactionV128.from_json(obj)
        elif tt == TransactionVersion.AUTH_ADDRESS_UPDATE:
            txn = TransactionV176.from_json(obj)
        elif tt == TransactionVersion.AUTH_CONDITION_UPDATE:
            txn = TransactionV177.from_json(obj)
        elif tt == TransactionVersion.MINTER_COIN_CREATION:
            txn = TransactionV129.from_json(obj)
        elif tt == TransactionVersion.LEGACY:
            txn = TransactionV1.legacy_from_json(obj)

        if isinstance(txn, TransactionBaseClass):
            txn.id = id
            return txn

        raise Exception("transactionversion {} is unknown".format(tt))