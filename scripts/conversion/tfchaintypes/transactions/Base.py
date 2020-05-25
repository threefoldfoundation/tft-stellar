from functools import reduce
from enum import IntEnum
from abc import ABC, abstractmethod, abstractclassmethod


class TransactionVersion(IntEnum):
    """
    The valid Transaction versions as known by the TFChain network.
    """

    LEGACY = 0
    STANDARD = 1

    MINTER_DEFINITION = 128
    MINTER_COIN_CREATION = 129

    THREEBOT_REGISTRATION = 144
    THREEBOT_RECORD_UPDATE = 145
    THREEBOT_NAME_TRANSFER = 146

    AUTH_ADDRESS_UPDATE = 176
    AUTH_CONDITION_UPDATE = 177

    ERC20_CONVERT = 208
    ERC20_COIN_CREATION = 209
    ERC20_ADDRESS_REGISTRATION = 210


from ..PrimitiveTypes import Hash


class TransactionBaseClass(ABC):
    def __init__(self):
        self._id = None
        self._height = -1
        self._unconfirmed = False

    @classmethod
    def from_json(cls, obj):
        """
        Create this transaction from a raw JSON Tx
        """
        txn = cls()
        tv = obj.get("version", -1)
        if txn.version != tv:
            raise Exception("transaction is expected to be of version {}, not version {}".format(txn.version, tv))
        txn._from_json_data_object(obj.get("data", {}))
        return txn

    @property
    @abstractmethod
    def version(self):
        """
        Version of this Transaction.
        """
        pass

    @property
    def unconfirmed(self):
        return self._unconfirmed

    @unconfirmed.setter
    def unconfirmed(self, value):
        if not isinstance(value, bool):
            raise j.exceptions.Value(
                "unconfirmed status of a Transaction is expected to be of type bool, not {}".format(type(bool))
            )
        self._unconfirmed = bool(value)

    @property
    def id(self):
        """
        ID of this transaction.
        """
        return str(self._id)

    @id.setter
    def id(self, id):
        if isinstance(id, Hash):
            self._id = Hash(value=id.value)
        self._id = Hash(value=id)

    def __hash__(self):
        if self._id is None:
            return hash(j.data.serializers.json.dumps(self.json()))
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, TransactionBaseClass):
            raise j.exceptions.Value(
                "other is expected to be subtype of TransactionBaseClass, not {}".format(type(other))
            )
        return hash(self) == hash(other)

    @property
    def height(self):
        """
        Height of the block this transaction is part of,
        if not yet part of a block it will be negative (-1 is the default value).
        """
        return self._height

    @height.setter
    def height(self, value):
        if not (isinstance(value, int) and not isinstance(value, bool)):
            raise j.exceptions.Value("value should be of type int or bool, not {}".format(type(value)))
        if value < 0:
            raise j.exceptions.Value("a block height cannot be negative")
        self._height = value

    @property
    def coin_inputs(self):
        """
        Coin inputs of this Transaction,
        used as funding for coin outputs, fees and any other kind of coin output.
        """
        return []

    @property
    def coin_outputs(self):
        """
        Coin outputs of this Transaction,
        funded by the Transaction's coin inputs.
        """
        return []

    @property
    def blockstake_inputs(self):
        """
        Blockstake inputs of this Transaction,
        used mainly as funding for block creations.
        """
        return []

    @property
    def blockstake_outputs(self):
        """
        BLockstake outputs of this Transaction,
        funded by the Transaction's blockstake inputs.
        """
        return []

    @property
    def miner_fees(self):
        """
        Miner fees, paid to the block creator of this Transaction,
        funded by this Transaction's coin inputs.
        """
        return []

    @property
    def data(self):
        """
        Optional binary data attached to this Transaction,
        with a max length of 83 bytes.
        """
        return bytes()

    @abstractmethod
    def _signature_hash_input_get(self, *extra_objects):
        """
        signature_hash_get is used to get the input
        """
        pass

    def signature_hash_get(self, *extra_objects):
        """
        signature_hash_get is used to get the signature hash for this Transaction,
        which are used to proof the authenticity of the transaction.
        """
        input = self._signature_hash_input_get(*extra_objects)
        return bytes.fromhex(j.data.hash.blake2_string(input))

    @abstractmethod
    def _from_json_data_object(self, data):
        pass

    @abstractmethod
    def _json_data_object(self):
        pass

    def json(self):
        obj = {"version": self.version.value}
        data = self._json_data_object()
        if data:
            obj["data"] = data
        return obj

    def __str__(self):
        s = "transaction v{}".format(self.version)
        if self.id:
            s += " {}".format(self.id)
        return s

    __repr__ = __str__

    @property
    def _coin_outputid_specifier(self):
        return b"coin output\0\0\0\0\0"

    @property
    def _blockstake_outputid_specifier(self):
        return b"blstake output\0\0"

    def coin_outputid_new(self, index):
        """
        Compute the ID of a Coin Output within this transaction.
        """
        if index < 0 or index >= len(self.coin_outputs):
            raise j.exceptions.Value("coin output index is out of range")
        return self._outputid_new(specifier=self._coin_outputid_specifier, index=index)

    def blockstake_outputid_new(self, index):
        """
        Compute the ID of a Coin Output within this transaction.
        """
        if index < 0 or index >= len(self.coin_outputs):
            raise j.exceptions.Value("coin output index is out of range")
        return self._outputid_new(specifier=self._blockstake_outputid_specifier, index=index)

    def _outputid_new(self, specifier, index):
        encoder = j.data.rivine.encoder_sia_get()
        encoder.add_array(specifier)
        encoder.add_array(self._id_input_compute())
        encoder.add_int(index)
        hash = bytearray.fromhex(j.data.hash.blake2_string(encoder.data))
        return Hash(value=hash)

    def _id_input_compute(self):
        """
        Compute the core input data used for any ID computation.
        The default can be overriden by Transaction Classes should it be required.
        """
        return self.binary_encode()

    def binary_encode(self):
        """
        Binary encoding of a Transaction,
        the transaction type defines if it is done using Sia or Rivine encoding.
        """
        return bytearray([self.version]) + self._binary_encode_data()

    def _binary_encode_data(self):
        """
        Default Binary encoding of a Transaction Data,
        can be overriden if required.
        """
        encoder = j.data.rivine.encoder_sia_get()
        encoder.add_all(
            self.coin_inputs,
            self.coin_outputs,
            self.blockstake_inputs,
            self.blockstake_outputs,
            self.miner_fees,
            self.data,
        )
        return encoder.data

    def signature_requests_new(self):
        """
        Returns all signature requests still open for this Transaction.
        """
        requests = []
        for (index, ci) in enumerate(self.coin_inputs):
            f = InputSignatureHashFactory(self, index).signature_hash_new
            requests += ci.signature_requests_new(input_hash_func=f)
        for (index, bsi) in enumerate(self.blockstake_inputs):
            f = InputSignatureHashFactory(self, index).signature_hash_new
            requests += bsi.signature_requests_new(input_hash_func=f)
        return requests + self._extra_signature_requests_new()

    def _extra_signature_requests_new(self):
        """
        Optional signature requests that can be defined by the transaction,
        outside of the ordinary, returns an empty list by default.
        """
        return []

    def is_fulfilled(self):
        """
        Returns if the entire transaction is fulfilled,
        meaning it has all the required signatures in all the required places.
        """
        return reduce((lambda r, ci: r and ci.is_fulfilled()), self.coin_inputs, self._extra_is_fulfilled())

    def _extra_is_fulfilled(self):
        """
        Optional check that can be defined by specific transactions,
        in case there are signatures required in other scenarios.

        Returns True by default.
        """
        return True


class InputSignatureHashFactory:
    """
    Class that can be used by Transaction consumers,
    to generate a factory that can provide the signature_hash_func callback
    used during the creation of signature requests,
    only useful if some extra objects needs to be included that are outside the Txn scope.
    """

    def __init__(self, txn, *extra_objects):
        if not isinstance(txn, TransactionBaseClass):
            raise j.exceptions.Value("txn has an invalid type {}".format(type(txn)))
        self._txn = txn
        self._extra_objects = extra_objects

    def signature_hash_new(self, *extra_objects):
        objects = list(self._extra_objects)
        objects += extra_objects
        return self._txn.signature_hash_get(*objects)
