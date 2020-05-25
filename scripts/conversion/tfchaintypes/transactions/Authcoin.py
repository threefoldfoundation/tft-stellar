from Jumpscale import j

from .Base import TransactionBaseClass, TransactionVersion

from ..FulfillmentTypes import FulfillmentBaseClass, FulfillmentSingleSignature
from ..ConditionTypes import ConditionBaseClass, ConditionNil, UnlockHash
from ..PrimitiveTypes import BinaryData, Currency
from ..IO import CoinInput, CoinOutput


class TransactionV176(TransactionBaseClass):
    _SPECIFIER = b"auth addr update"

    def __init__(self):
        self._nonce = BinaryData(j.data.idgenerator.generateXByteID(8), strencoding="base64")
        self._auth_fulfillment = None
        self._auth_addresses = []
        self._deauth_addresses = []
        self._data = None
        self._miner_fees = []

        # current mint condition
        self._parent_auth_condition = None

        super().__init__()

    @property
    def version(self):
        return TransactionVersion.AUTH_ADDRESS_UPDATE

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
    def auth_addresses(self):
        """
        Unlock hashes to be authorized by this transaction
        """
        return self._auth_addresses

    @auth_addresses.setter
    def auth_addresses(self, value):
        self._auth_addresses = []
        if not value:
            return
        for uh in value:
            self.auth_addresses_add(uh)

    def auth_addresses_add(self, uh):
        if isinstance(uh, UnlockHash):
            self._auth_addresses.append(uh)
        elif isinstance(uh, str):
            self._auth_addresses.append(UnlockHash.from_json(uh))
        else:
            raise j.exceptions.Value("invalid type of uh {} (expected: UnlockHash or str)".format(type(uh)))

    @property
    def deauth_addresses(self):
        """
        Unlock hashes to be deauthorized by this transaction
        """
        return self._deauth_addresses

    @deauth_addresses.setter
    def deauth_addresses(self, value):
        self._deauth_addresses = []
        if not value:
            return
        for uh in value:
            self.deauth_addresses_add(uh)

    def deauth_addresses_add(self, uh):
        if isinstance(uh, UnlockHash):
            self._deauth_addresses.append(uh)
        elif isinstance(uh, str):
            self._deauth_addresses.append(UnlockHash.from_json(uh))
        else:
            raise j.exceptions.Value("invalid type of uh {} (expected: UnlockHash or str)".format(type(uh)))

    def auth_fulfillment_defined(self):
        return self._auth_fulfillment is not None

    @property
    def auth_fulfillment(self):
        """
        Retrieve the current auth fulfillment
        """
        if self._auth_fulfillment is None:
            return FulfillmentSingleSignature()
        return self._auth_fulfillment

    @auth_fulfillment.setter
    def auth_fulfillment(self, value):
        if value is None:
            self._auth_fulfillment = None
            return
        if not isinstance(value, FulfillmentBaseClass):
            raise j.exceptions.Value(
                "AuthAddressUpdate (v176) Transaction's auth fulfillment has to be a subtype of FulfillmentBaseClass, not {}".format(
                    type(value)
                )
            )
        self._auth_fulfillment = value

    @property
    def parent_auth_condition(self):
        """
        Retrieve the parent auth condition which will be set
        """
        if self._parent_auth_condition is None:
            return ConditionNil()
        return self._parent_auth_condition

    @parent_auth_condition.setter
    def parent_auth_condition(self, value):
        if value is None:
            self._parent_auth_condition = None
            return
        if not isinstance(value, ConditionBaseClass):
            raise j.exceptions.Value(
                "AuthAddressUpdate (v176) Transaction's parent auth condition has to be a subtype of ConditionBaseClass, not {}".format(
                    type(value)
                )
            )
        self._parent_auth_condition = value

    def miner_fee_add(self, value):
        self._miner_fees.append(Currency(value=value))

    @property
    def miner_fees(self):
        """
        Miner fees, paid to the block creator of this Transaction,
        funded by this Transaction's coin inputs.
        """
        return self._miner_fees

    def _signature_hash_input_get(self, *extra_objects):
        e = j.data.rivine.encoder_sia_get()

        # encode the transaction version
        e.add_byte(self.version)

        # encode the specifier
        e.add_array(TransactionV176._SPECIFIER)

        # encode nonce
        e.add_array(self._nonce.value)

        # extra objects if any
        # TODO: is this needed??
        if extra_objects:
            e.add_all(*extra_objects)

        # encode auth addresses
        e.add_slice(self.auth_addresses)

        # encode deauth addresses
        e.add_slice(self.deauth_addresses)

        # encode miner fees
        e.add_slice(self.miner_fees)

        # encode custom data
        e.add(self.data)

        # return the encoded data
        return e.data

    def _id_input_compute(self):
        return bytearray(TransactionV176._SPECIFIER) + self._binary_encode_data()

    def _binary_encode_data(self):
        encoder = j.data.rivine.encoder_rivine_get()
        encoder.add_array(self._nonce.value)
        encoder.add_all(self.auth_addresses, self.deauth_addresses, self.data, self.auth_fulfillment, self.miner_fees)
        return encoder.data

    def _from_json_data_object(self, data):
        self._nonce = BinaryData.from_json(data.get("nonce", ""), strencoding="base64")
        self._auth_addresses = [UnlockHash.from_json(uh) for uh in data.get("authaddresses", []) or []]
        self._deauth_addresses = [UnlockHash.from_json(uh) for uh in data.get("deauthaddresses", []) or []]
        self._auth_fulfillment = j.clients.tfchain.types.fulfillments.from_json(data.get("authfulfillment", {}))
        self._miner_fees = [Currency.from_json(fee) for fee in data.get("minerfees", []) or []]
        self._data = BinaryData.from_json(data.get("arbitrarydata", None) or "", strencoding="base64")

    def _json_data_object(self):
        return {
            "nonce": self._nonce.json(),
            "authaddresses": [uh.json() for uh in self.auth_addresses],
            "deauthaddresses": [uh.json() for uh in self.deauth_addresses],
            "arbitrarydata": self.data.json(),
            "authfulfillment": self.auth_fulfillment.json(),
            "minerfees": [fee.json() for fee in self._miner_fees],
        }

    def _extra_signature_requests_new(self):
        if self._parent_auth_condition is None:
            return []  # nothing to be signed
        return self._auth_fulfillment.signature_requests_new(
            input_hash_func=self.signature_hash_get,  # no extra objects are to be included within txn scope
            parent_condition=self._parent_auth_condition,
        )

    def _extra_is_fulfilled(self):
        if self._parent_auth_condition is None:
            return False
        return self.auth_fulfillment.is_fulfilled(parent_condition=self._parent_auth_condition)


class TransactionV177(TransactionBaseClass):
    _SPECIFIER = b"auth cond update"

    def __init__(self):
        self._nonce = BinaryData(j.data.idgenerator.generateXByteID(8), strencoding="base64")
        self._auth_fulfillment = None
        self._auth_condition = None
        self._data = None
        self._miner_fees = []

        # current auth condition
        self._parent_auth_condition = None

        super().__init__()

    @property
    def version(self):
        return TransactionVersion.AUTH_CONDITION_UPDATE

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
    def auth_condition(self):
        """
        Retrieve the new auth condition which will be set
        """
        if self._auth_condition is None:
            return ConditionNil()
        return self._auth_condition

    @auth_condition.setter
    def auth_condition(self, value):
        if value is None:
            self._auth_condition = None
            return
        if not isinstance(value, ConditionBaseClass):
            raise j.exceptions.Value(
                "AuthConditionDefinition (v177) Transaction's auth condition has to be a subtype of ConditionBaseClass, not {}".format(
                    type(value)
                )
            )
        self._auth_condition = value

    @property
    def parent_auth_condition(self):
        """
        Retrieve the parent auth condition which will be set
        """
        if self._parent_auth_condition is None:
            return ConditionNil()
        return self._parent_auth_condition

    @parent_auth_condition.setter
    def parent_auth_condition(self, value):
        if value is None:
            self._parent_auth_condition = None
            return
        if not isinstance(value, ConditionBaseClass):
            raise j.exceptions.Value(
                "AuthCondtionDefinition (v177) Transaction's parent auth condition has to be a subtype of ConditionBaseClass, not {}".format(
                    type(value)
                )
            )
        self._parent_auth_condition = value

    def auth_fulfillment_defined(self):
        return self._auth_fulfillment is not None

    @property
    def auth_fulfillment(self):
        """
        Retrieve the current auth fulfillment
        """
        if self._auth_fulfillment is None:
            return FulfillmentSingleSignature()
        return self._auth_fulfillment

    @auth_fulfillment.setter
    def auth_fulfillment(self, value):
        if value is None:
            self._auth_fulfillment = None
            return
        if not isinstance(value, FulfillmentBaseClass):
            raise j.exceptions.Value(
                "AuthConditionDefinition (v177) Transaction's auth fulfillment has to be a subtype of FulfillmentBaseClass, not {}".format(
                    type(value)
                )
            )
        self._auth_fulfillment = value

    def miner_fee_add(self, value):
        self._miner_fees.append(Currency(value=value))

    @property
    def miner_fees(self):
        """
        Miner fees, paid to the block creator of this Transaction,
        funded by this Transaction's coin inputs.
        """
        return self._miner_fees

    def _signature_hash_input_get(self, *extra_objects):
        e = j.data.rivine.encoder_sia_get()

        # encode the transaction version
        e.add_byte(self.version)

        # encode the specifier
        e.add_array(TransactionV177._SPECIFIER)

        # encode nonce
        e.add_array(self._nonce.value)

        # extra objects if any
        if extra_objects:
            e.add_all(*extra_objects)

        # encode new mint condition
        e.add(self.auth_condition)

        # encode custom data
        e.add(self.data)

        # encode miner fees
        e.add_slice(self.miner_fees)

        # return the encoded data
        return e.data

    def _id_input_compute(self):
        return bytearray(TransactionV177._SPECIFIER) + self._binary_encode_data()

    def _binary_encode_data(self):
        encoder = j.data.rivine.encoder_rivine_get()
        encoder.add_array(self._nonce.value)
        encoder.add_all(self.data, self.auth_condition, self.auth_fulfillment, self.miner_fees)
        return encoder.data

    def _from_json_data_object(self, data):
        self._nonce = BinaryData.from_json(data.get("nonce", ""), strencoding="base64")
        self._auth_condition = j.clients.tfchain.types.conditions.from_json(data.get("authcondition", {}))
        self._auth_fulfillment = j.clients.tfchain.types.fulfillments.from_json(data.get("authfulfillment", {}))
        self._miner_fees = [Currency.from_json(fee) for fee in data.get("minerfees", []) or []]
        self._data = BinaryData.from_json(data.get("arbitrarydata", None) or "", strencoding="base64")

    def _json_data_object(self):
        return {
            "nonce": self._nonce.json(),
            "authfulfillment": self.auth_fulfillment.json(),
            "authcondition": self.auth_condition.json(),
            "minerfees": [fee.json() for fee in self._miner_fees],
            "arbitrarydata": self.data.json(),
        }

    def _extra_signature_requests_new(self):
        if self._parent_auth_condition is None:
            return []  # nothing to be signed
        return self._auth_fulfillment.signature_requests_new(
            input_hash_func=self.signature_hash_get,  # no extra objects are to be included within txn scope
            parent_condition=self._parent_auth_condition,
        )

    def _extra_is_fulfilled(self):
        if self._parent_auth_condition is None:
            return False
        return self.auth_fulfillment.is_fulfilled(parent_condition=self._parent_auth_condition)
