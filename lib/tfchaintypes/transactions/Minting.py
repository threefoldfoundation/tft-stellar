import random
from .Base import TransactionBaseClass, TransactionVersion

from ..FulfillmentTypes import FulfillmentBaseClass, FulfillmentSingleSignature, FulfillmentFactory
from ..ConditionTypes import ConditionBaseClass, ConditionNil, ConditionFactory
from ..PrimitiveTypes import BinaryData, Currency
from ..IO import CoinInput, CoinOutput


def _generateXByteID(x):
    out = bytearray()
    for i in range(0, x):
        out.append(random.randint(0, 255))
    return out


class TransactionV128(TransactionBaseClass):
    _SPECIFIER = b"minter defin tx\0"

    def __init__(self):
        self._mint_fulfillment = None
        self._mint_condition = None
        self._miner_fees = []
        self._data = None

        self._nonce = BinaryData(_generateXByteID(8), strencoding="base64")

        # current mint condition
        self._parent_mint_condition = None

        super().__init__()

    @property
    def version(self):
        return TransactionVersion.MINTER_DEFINITION

    @property
    def miner_fees(self):
        """
        Miner fees, paid to the block creator of this Transaction,
        funded by this Transaction's coin inputs.
        """
        return self._miner_fees

    @property
    def data(self):
        """
        Optional binary data attached to this Transaction,
        with a max length of 83 bytes.
        """
        if self._data is None:
            return BinaryData(strencoding="base64")
        return self._data

    @data.setter
    def data(self, value):
        if value is None:
            self._data = None
            return
        if isinstance(value, BinaryData):
            value = value.value
        elif isinstance(value, str):
            value = value.encode("utf-8")
        if len(value) > 83:
            raise Exception(
                "arbitrary data can have a maximum bytes length of 83, {} exceeds this limit".format(len(value))
            )
        self._data = BinaryData(value=value, strencoding="base64")

    @property
    def mint_condition(self):
        """
        Retrieve the new mint condition which will be set
        """
        if self._mint_condition is None:
            return ConditionNil()
        return self._mint_condition

    @mint_condition.setter
    def mint_condition(self, value):
        if value is None:
            self._mint_condition = None
            return
        if not isinstance(value, ConditionBaseClass):
            raise Exception(
                "MintDefinition (v128) Transaction's mint condition has to be a subtype of ConditionBaseClass, not {}".format(
                    type(value)
                )
            )
        self._mint_condition = value

    @property
    def parent_mint_condition(self):
        """
        Retrieve the parent mint condition which will be set
        """
        if self._parent_mint_condition is None:
            return ConditionNil()
        return self._parent_mint_condition

    @parent_mint_condition.setter
    def parent_mint_condition(self, value):
        if value is None:
            self._parent_mint_condition = None
            return
        if not isinstance(value, ConditionBaseClass):
            raise Exception(
                "MintDefinition (v128) Transaction's parent mint condition has to be a subtype of ConditionBaseClass, not {}".format(
                    type(value)
                )
            )
        self._parent_mint_condition = value

    def mint_fulfillment_defined(self):
        return self._mint_fulfillment is not None

    @property
    def mint_fulfillment(self):
        """
        Retrieve the current mint fulfillment
        """
        if self._mint_fulfillment is None:
            return FulfillmentSingleSignature()
        return self._mint_fulfillment

    @mint_fulfillment.setter
    def mint_fulfillment(self, value):
        if value is None:
            self._mint_fulfillment = None
            return
        if not isinstance(value, FulfillmentBaseClass):
            raise Exception(
                "MintDefinition (v128) Transaction's mint fulfillment has to be a subtype of FulfillmentBaseClass, not {}".format(
                    type(value)
                )
            )
        self._mint_fulfillment = value

    def miner_fee_add(self, value):
        self._miner_fees.append(Currency(value=value))

    def _signature_hash_input_get(self, *extra_objects):
        e = j.data.rivine.encoder_sia_get()

        # encode the transaction version
        e.add_byte(self.version)

        # encode the specifier
        e.add_array(TransactionV128._SPECIFIER)

        # encode nonce
        e.add_array(self._nonce.value)

        # extra objects if any
        if extra_objects:
            e.add_all(*extra_objects)

        # encode new mint condition
        e.add(self.mint_condition)

        # encode miner fees
        e.add_slice(self.miner_fees)

        # encode custom data
        e.add(self.data)

        # return the encoded data
        return e.data

    def _id_input_compute(self):
        return bytearray(TransactionV128._SPECIFIER) + self._binary_encode_data()

    def _binary_encode_data(self):
        encoder = j.data.rivine.encoder_sia_get()
        encoder.add_array(self._nonce.value)
        encoder.add_all(self.mint_fulfillment, self.mint_condition, self.miner_fees, self.data)
        return encoder.data

    def _from_json_data_object(self, data):
        self._nonce = BinaryData.from_json(data.get("nonce", ""), strencoding="base64")
        self._mint_condition = ConditionFactory.from_json(data.get("mintcondition", {}))
        self._mint_fulfillment = FulfillmentFactory.from_json(data.get("mintfulfillment", {}))
        self._miner_fees = [Currency.from_json(fee) for fee in data.get("minerfees", []) or []]
        self._data = BinaryData.from_json(data.get("arbitrarydata", None) or "", strencoding="base64")

    def _json_data_object(self):
        return {
            "nonce": self._nonce.json(),
            "mintfulfillment": self.mint_fulfillment.json(),
            "mintcondition": self.mint_condition.json(),
            "minerfees": [fee.json() for fee in self._miner_fees],
            "arbitrarydata": self.data.json(),
        }

    def _extra_signature_requests_new(self):
        if self._parent_mint_condition is None:
            return []  # nothing to be signed
        return self._mint_fulfillment.signature_requests_new(
            input_hash_func=self.signature_hash_get,  # no extra objects are to be included within txn scope
            parent_condition=self._parent_mint_condition,
        )

    def _extra_is_fulfilled(self):
        if self._parent_mint_condition is None:
            return False
        return self.mint_fulfillment.is_fulfilled(parent_condition=self._parent_mint_condition)


class TransactionV129(TransactionBaseClass):
    _SPECIFIER = b"coin mint tx\0\0\0\0"

    def __init__(self):
        self._mint_fulfillment = None
        self._coin_outputs = []
        self._miner_fees = []
        self._data = None
        self._nonce = BinaryData(_generateXByteID(8), strencoding="base64")

        # current mint condition
        self._parent_mint_condition = None

        super().__init__()

    @property
    def version(self):
        return TransactionVersion.MINTER_COIN_CREATION

    @property
    def miner_fees(self):
        """
        Miner fees, paid to the block creator of this Transaction,
        funded by this Transaction's coin inputs.
        """
        return self._miner_fees

    @property
    def data(self):
        """
        Optional binary data attached to this Transaction,
        with a max length of 83 bytes.
        """
        if self._data is None:
            return BinaryData(strencoding="base64")
        return self._data

    @data.setter
    def data(self, value):
        if value is None:
            self._data = None
            return
        if isinstance(value, BinaryData):
            value = value.value
        elif isinstance(value, str):
            value = value.encode("utf-8")
        if len(value) > 83:
            raise j.exceptions.Value(
                "arbitrary data can have a maximum bytes length of 83, {} exceeds this limit".format(len(value))
            )
        self._data = BinaryData(value=value, strencoding="base64")

    @property
    def coin_outputs(self):
        """
        Coin outputs of this Transaction,
        funded by the Transaction's coin inputs.
        """
        return self._coin_outputs

    @coin_outputs.setter
    def coin_outputs(self, value):
        self._coin_outputs = []
        if not value:
            return
        for co in value:
            self.coin_output_add(co.value, co.condition, id=co.id)

    def coin_output_add(self, value, condition, id=None):
        co = CoinOutput(value=value, condition=condition)
        co.id = id
        self._coin_outputs.append(co)

    def miner_fee_add(self, value):
        self._miner_fees.append(Currency(value=value))

    def mint_fulfillment_defined(self):
        return self._mint_fulfillment is not None

    @property
    def mint_fulfillment(self):
        """
        Retrieve the current mint fulfillment
        """
        if self._mint_fulfillment is None:
            return FulfillmentSingleSignature()
        return self._mint_fulfillment

    @mint_fulfillment.setter
    def mint_fulfillment(self, value):
        if value is None:
            self._mint_fulfillment = None
            return
        if not isinstance(value, FulfillmentBaseClass):
            raise j.exceptions.Value(
                "CoinCreation (v129) Transaction's mint fulfillment has to be a subtype of FulfillmentBaseClass, not {}".format(
                    type(value)
                )
            )
        self._mint_fulfillment = value

    @property
    def parent_mint_condition(self):
        """
        Retrieve the parent mint condition which will be set
        """
        if self._parent_mint_condition is None:
            return ConditionNil()
        return self._parent_mint_condition

    @parent_mint_condition.setter
    def parent_mint_condition(self, value):
        if value is None:
            self._parent_mint_condition = None
            return
        if not isinstance(value, ConditionBaseClass):
            raise j.exceptions.Value(
                "CoinCreation (v129) Transaction's parent mint condition has to be a subtype of ConditionBaseClass, not {}".format(
                    type(value)
                )
            )
        self._parent_mint_condition = value

    def _signature_hash_input_get(self, *extra_objects):
        e = j.data.rivine.encoder_sia_get()

        # encode the transaction version
        e.add_byte(self.version)

        # encode the specifier
        e.add_array(TransactionV129._SPECIFIER)

        # encode nonce
        e.add_array(self._nonce.value)

        # extra objects if any
        if extra_objects:
            e.add_all(*extra_objects)

        # encode coin outputs
        e.add_slice(self.coin_outputs)

        # encode miner fees
        e.add_slice(self.miner_fees)

        # encode custom data
        e.add(self.data)

        # return the encoded data
        return e.data

    def _id_input_compute(self):
        return bytearray(TransactionV129._SPECIFIER) + self._binary_encode_data()

    def _binary_encode_data(self):
        encoder = j.data.rivine.encoder_sia_get()
        encoder.add_array(self._nonce.value)
        encoder.add_all(self.mint_fulfillment, self.coin_outputs, self.miner_fees, self.data)
        return encoder.data

    def _from_json_data_object(self, data):
        self._nonce = BinaryData.from_json(data.get("nonce", ""), strencoding="base64")
        self._mint_fulfillment = FulfillmentFactory.from_json(data.get("mintfulfillment", {}))
        self._coin_outputs = [CoinOutput.from_json(co) for co in data.get("coinoutputs", []) or []]
        self._miner_fees = [Currency.from_json(fee) for fee in data.get("minerfees", []) or []]
        self._data = BinaryData.from_json(data.get("arbitrarydata", None) or "", strencoding="base64")

    def _json_data_object(self):
        return {
            "nonce": self._nonce.json(),
            "mintfulfillment": self.mint_fulfillment.json(),
            "coinoutputs": [co.json() for co in self.coin_outputs],
            "minerfees": [fee.json() for fee in self.miner_fees],
            "arbitrarydata": self.data.json(),
        }

    def _extra_signature_requests_new(self):
        if self._parent_mint_condition is None:
            return []  # nothing to be signed
        return self._mint_fulfillment.signature_requests_new(
            input_hash_func=self.signature_hash_get,  # no extra objects are to be included within txn scope
            parent_condition=self._parent_mint_condition,
        )

    def _extra_is_fulfilled(self):
        if self._parent_mint_condition is None:
            return False
        return self.mint_fulfillment.is_fulfilled(parent_condition=self._parent_mint_condition)
