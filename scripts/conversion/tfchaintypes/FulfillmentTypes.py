from .BaseDataType import BaseDataTypeClass
from .CryptoTypes import PublicKey
from .PrimitiveTypes import BinaryData, Hash
from .ConditionTypes import (
    UnlockHash,
    UnlockHashType,
    ConditionNil,
    ConditionUnlockHash,
    ConditionAtomicSwap,
    ConditionMultiSignature,
    AtomicSwapSecret,
)


class ED25519Signature(BinaryData):
    SIZE = 64

    """
    ED25519 Signature, used in TFChain.
    """

    def __init__(self, value=None, as_array=False):
        super().__init__(value, fixed_size=ED25519Signature.SIZE, strencoding="hex")
        if not isinstance(as_array, bool):
            raise Exception("as_array has to be of type bool, not type {}".format(type(as_array)))
        self._as_array = as_array

    @classmethod
    def from_json(cls, obj, as_array=False):
        if obj is not None and not isinstance(obj, str):
            raise Exception(
                "ed25519 signature is expected to be an encoded string when part of a JSON object, not {}".format(
                    type(obj)
                )
            )
        if obj == "":
            obj = None
        return cls(value=obj, as_array=as_array)

    def sia_binary_encode(self, encoder):
        """
        Encode this binary data according to the Sia Binary Encoding format.
        Always encoded as a slice.
        """
        encoder.add_slice(self._value)

    def rivine_binary_encode(self, encoder):
        """
        Encode this binary data according to the Rivine Binary Encoding format.
        Usually encoded as a slice, except when as part of a context where it is not needed.
        """
        if self._as_array:
            encoder.add_array(self._value)
        else:
            encoder.add_slice(self._value)


_FULFULLMENT_TYPE_SINGLE_SIG = 1
_FULFILLMENT_TYPE_ATOMIC_SWAP = 2
_FULFILLMENT_TYPE_MULTI_SIG = 3

from abc import ABC, abstractmethod


class SignatureCallbackBase(ABC):
    @abstractmethod
    def signature_add(self, public_key, signature):
        pass


class SignatureRequest:
    """
    SignatureRequest can be used to create a one-time-use individual sign request.
    """

    def __init__(self, unlockhash, input_hash_gen, callback):
        # set defined properties
        if not isinstance(unlockhash, UnlockHash):
            raise Exception(
                "signature request requires an unlock hash of Type UnlockHash, not: {}".format(type(unlockhash))
            )
        self._unlockhash = unlockhash
        if not callable(input_hash_gen):
            raise Exception(
                "signature request requires a generator function with the signature `f(PublicKey) -> Hash"
            )
        self._input_hash_gen = input_hash_gen
        if not isinstance(callback, SignatureCallbackBase):
            raise Exception(
                "signature request requires a callback of Type SignatureCallbackBase, not: {}".format(type(unlockhash))
            )
        self._callback = callback
        # property to ensure this request is only fulfilled once
        self._signed = False

    @property
    def fulfilled(self):
        """
        Returns True if this request was already fulfilled,
        False otherwise.
        """
        return self._signed

    @property
    def wallet_address(self):
        """
        Returns the wallet address of the owner who requested the signature.
        """
        return str(self._unlockhash)

    def input_hash_new(self, public_key):
        """
        Create an input hash for the public key of the fulfiller.
        """
        input_hash = self._input_hash_gen(public_key)
        if isinstance(input_hash, (str, bytearray, bytes)):
            input_hash = Hash(value=input_hash)
        elif not isinstance(input_hash, Hash):
            raise Exception(
                "signature request requires an input hash of Type Hash, not: {}".format(type(input_hash))
            )
        return input_hash

    def signature_fulfill(self, public_key, signature):
        """
        Fulfill the signature, once and once only.
        """
        # guarantee base conditions
        if self.fulfilled:
            raise Exception(
                "SignatureRequest is already fulfilled for address {}".format(self.wallet_address)
            )

        # ensure public key is the key of the wallet who owns this request
        if not isinstance(public_key, PublicKey):
            raise Exception("public key is expected to be of type PublicKey, not {}".format(type(public_key)))
        address = str(public_key.unlockhash)
        if (
            self._unlockhash.type != UnlockHashType.NIL and self.wallet_address != address
        ):  # only check if the request is not using a NIL Condition
            raise Exception(
                "signature request cannot be fulfilled using address {}, expected address {}".format(
                    address, self.wallet_address
                )
            )

        # add the signature to the callback
        self._callback.signature_add(public_key=public_key, signature=signature)
        # ensure this was the one and only time we signed
        self._signed = True


class FulfillmentFactory(object):
    """
    Fulfillment Factory class
    """

    def from_json(self, obj):
        ft = obj.get("type", 0)
        if ft == _FULFULLMENT_TYPE_SINGLE_SIG:
            return FulfillmentSingleSignature.from_json(obj)
        if ft == _FULFILLMENT_TYPE_MULTI_SIG:
            return FulfillmentMultiSignature.from_json(obj)
        if ft == _FULFILLMENT_TYPE_ATOMIC_SWAP:
            return FulfillmentAtomicSwap.from_json(obj)
        raise Exception("unsupport fulfillment type {}".format(ft))

    def from_condition(self, condition):
        """
        Create a fresh fulfillment from its parent condition.
        """
        if condition is None:
            return FulfillmentSingleSignature()
        if isinstance(condition, ConditionAtomicSwap):
            return FulfillmentAtomicSwap()
        icondition = condition.unwrap()
        if isinstance(icondition, (ConditionUnlockHash, ConditionNil)):
            return FulfillmentSingleSignature()
        if isinstance(icondition, ConditionMultiSignature):
            return FulfillmentMultiSignature()
        raise j.exceptions.Value(
            "invalid condition type {} cannot be used to create a fulfillment".format(type(condition))
        )

    def single_signature_new(self, pub_key=None, signature=None):
        """
        Create a new single signature fulfillment,
        used to unlock an UnlockHash Condition of type 1.
        """
        return FulfillmentSingleSignature(pub_key=pub_key, signature=signature)

    def atomic_swap_new(self, pub_key=None, signature=None, secret=None):
        """
        Create a new atomic swap fulfillment,
        used to unlock an atomic swap condition.
        """
        return FulfillmentAtomicSwap(pub_key=pub_key, signature=signature, secret=secret)

    def multi_signature_new(self, pairs=None):
        """
        Create a new multi signature fulfillment,
        used to unlock a multi signature condition.
        """
        return FulfillmentMultiSignature(pairs=pairs)



class FulfillmentBaseClass(SignatureCallbackBase, BaseDataTypeClass):
    @classmethod
    def from_json(cls, obj):
        ff = cls()
        t = obj.get("type", 0)
        if ff.type != t:
            raise Exception("invalid fulfillment type {}, expected it to be of type {}".format(t, ff.type))
        ff.from_json_data_object(obj.get("data", {}))
        return ff

    @property
    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def from_json_data_object(self, data):
        pass

    @abstractmethod
    def json_data_object(self):
        pass

    def json(self):
        return {"type": self.type, "data": self.json_data_object()}

    @abstractmethod
    def sia_binary_encode_data(self, encoder):
        pass

    def sia_binary_encode(self, encoder):
        """
        Encode this Fulfillment according to the Sia Binary Encoding format.
        """
        encoder.add_array(bytearray([int(self.type)]))
        data_enc = j.data.rivine.encoder_sia_get()
        self.sia_binary_encode_data(data_enc)
        encoder.add_slice(data_enc.data)

    @abstractmethod
    def rivine_binary_encode_data(self, encoder):
        pass

    def rivine_binary_encode(self, encoder):
        """
        Encode this Fulfillment according to the Rivine Binary Encoding format.
        """
        encoder.add_int8(int(self.type))
        data_enc = j.data.rivine.encoder_rivine_get()
        self.rivine_binary_encode_data(data_enc)
        encoder.add_slice(data_enc.data)

    @abstractmethod
    def signature_requests_new(self, input_hash_func, parent_condition):
        pass

    @abstractmethod
    def is_fulfilled(self, parent_condition):
        pass


class FulfillmentSingleSignature(FulfillmentBaseClass):
    """
    SingleSignature Fulfillment, used to unlock
    an UnlockHash Condition of type 1.
    """

    def __init__(self, pub_key=None, signature=None):
        self._pub_key = None
        self.public_key = pub_key
        self._signature = None
        self.signature = signature

    @property
    def type(self):
        return _FULFULLMENT_TYPE_SINGLE_SIG

    @property
    def fulfilled(self):
        return self._signature is not None

    @property
    def public_key(self):
        if self._pub_key is None:
            return PublicKey()
        return self._pub_key

    @public_key.setter
    def public_key(self, value):
        if value is None:
            self._pub_key = None
            return
        if not isinstance(value, PublicKey):
            raise Exception(
                "cannot assign value of type {} as FulfillmentSingleSignature's public key (expected type: PublicKey)".format(
                    type(value)
                )
            )
        self._pub_key = PublicKey(specifier=value.specifier, hash=value.hash)

    @property
    def signature(self):
        if self._signature is None:
            return ED25519Signature()
        return self._signature

    @signature.setter
    def signature(self, value):
        if value is None:
            self._signature = None
        else:
            self._signature = ED25519Signature(value=value)

    def signature_add(self, public_key, signature):
        """
        Implements SignatureCallbackBase.
        """
        self.public_key = public_key
        self.signature = signature

    def from_json_data_object(self, data):
        self._pub_key = PublicKey.from_json(data["publickey"])
        self._signature = ED25519Signature.from_json(data["signature"])

    def json_data_object(self):
        return {"publickey": self.public_key.json(), "signature": self.signature.json()}

    def sia_binary_encode_data(self, encoder):
        encoder.add_all(self.public_key, self.signature)

    def rivine_binary_encode_data(self, encoder):
        encoder.add_all(self.public_key, self.signature)

    def signature_requests_new(self, input_hash_func, parent_condition):
        if not callable(input_hash_func):
            raise Exception(
                "expected input hash generator func with signature `f(*extra_objects) -> Hash`, not {}".format(
                    type(input_hash_func)
                )
            )
        parent_condition = parent_condition.unwrap()
        if not isinstance(parent_condition, (ConditionNil, ConditionUnlockHash)):
            raise Exception(
                "parent condition of FulfillmentSingleSignature cannot be of type {}".format(type(parent_condition))
            )
        unlockhash = parent_condition.unlockhash
        if str(unlockhash) == str(self.public_key.unlockhash):
            return []  # nothing to do
        # define the input_hash_new generator function,
        # used to create the input hash for creating the signature
        def input_hash_gen(public_key):
            return input_hash_func()

        # create the only signature request
        return [SignatureRequest(unlockhash=unlockhash, input_hash_gen=input_hash_gen, callback=self)]

    def is_fulfilled(self, parent_condition):
        parent_condition = parent_condition.unwrap()
        if not isinstance(parent_condition, (ConditionNil, ConditionUnlockHash)):
            raise Exception(
                "parent condition of FulfillmentSingleSignature cannot be of type {}".format(type(parent_condition))
            )
        return self._signature is not None


class FulfillmentMultiSignature(FulfillmentBaseClass):
    """
    MultiSignature Fulfillment, used to unlock
    a MultiSignature Condition.
    """

    def __init__(self, pairs=None):
        self._pairs = []
        if pairs:
            for public_key, signature in pairs:
                self.add_pair(public_key, signature)

    @property
    def type(self):
        return _FULFILLMENT_TYPE_MULTI_SIG

    @property
    def pairs(self):
        return self._pairs

    @pairs.setter
    def pairs(self, value):
        self._pairs = []
        if not value:
            return
        for pair in value:
            self.add_pair(pair.public_key, pair.signature)

    def add_pair(self, public_key, signature):
        spk = str(public_key)
        for pair in self._pairs:
            if str(pair.public_key) == spk:
                raise Exception(
                    "cannot add public_key {} as it already exists within a pair of this MultiSignature Fulfillment".format(
                        spk
                    )
                )
        self._pairs.append(PublicKeySignaturePair(public_key=public_key, signature=signature))

    # Implements SignatureCallbackBase.
    signature_add = add_pair

    def from_json_data_object(self, data):
        self._pairs = []
        for pair in data["pairs"]:
            self._pairs.append(PublicKeySignaturePair.from_json(pair))

    def json_data_object(self):
        return {"pairs": [pair.json() for pair in self._pairs]}

    def sia_binary_encode_data(self, encoder):
        encoder.add(self._pairs)

    def rivine_binary_encode_data(self, encoder):
        encoder.add(self._pairs)

    def signature_requests_new(self, input_hash_func, parent_condition):
        if not callable(input_hash_func):
            raise Exception(
                "expected input hash generator func with signature `f(*extra_objects) -> Hash`, not {}".format(
                    type(input_hash_func)
                )
            )
        parent_condition = parent_condition.unwrap()
        if not isinstance(parent_condition, ConditionMultiSignature):
            raise Exception(
                "parent condition of FulfillmentMultiSignature cannot be of type {}".format(type(parent_condition))
            )
        requests = []
        signed = [str(pair.public_key.unlockhash) for pair in self._pairs]
        # define the input_hash_new generator function,
        # used to create the input hash for creating the signature
        def input_hash_gen(public_key):
            return input_hash_func(public_key)

        # create a signature hash for all signees that haven't signed yet
        for unlockhash in parent_condition.unlockhashes:
            if str(unlockhash) not in signed:
                requests.append(SignatureRequest(unlockhash=unlockhash, input_hash_gen=input_hash_gen, callback=self))
        return requests

    def is_fulfilled(self, parent_condition):
        parent_condition = parent_condition.unwrap()
        if not isinstance(parent_condition, ConditionMultiSignature):
            raise Exception(
                "parent condition of FulfillmentMultiSignature cannot be of type {}".format(type(parent_condition))
            )
        return len(self._pairs) >= parent_condition.required_signatures


class PublicKeySignaturePair(BaseDataTypeClass):
    """
    PublicKeySignaturePair class
    """

    def __init__(self, public_key=None, signature=None):
        self._public_key = None
        self.public_key = public_key
        self._signature = None
        self.signature = signature

    @classmethod
    def from_json(cls, obj):
        return cls(
            public_key=PublicKey.from_json(obj["publickey"]), signature=ED25519Signature.from_json(obj["signature"])
        )

    @property
    def public_key(self):
        if self._public_key is None:
            return PublicKey()
        return self._public_key

    @public_key.setter
    def public_key(self, pk):
        if pk is None:
            self._public_key = None
            return
        if not isinstance(pk, PublicKey):
            raise Exception(
                "cannot assign value of type {} as PublicKeySignaturePair's public key (expected type: PublicKey)".format(
                    type(pk)
                )
            )
        self._public_key = PublicKey(specifier=pk.specifier, hash=pk.hash)

    @property
    def signature(self):
        if self._signature is None:
            return ED25519Signature()
        return self._signature

    @signature.setter
    def signature(self, value):
        if value is None:
            self._signature = None
        else:
            self._signature = ED25519Signature(value=value)

    def json(self):
        return {"publickey": self.public_key.json(), "signature": self.signature.json()}

    def sia_binary_encode(self, encoder):
        """
        Encode this PublicKeySignature Pair according to the Sia Binary Encoding format.
        """
        encoder.add_all(self.public_key, self.signature)

    def rivine_binary_encode(self, encoder):
        """
        Encode this PublicKeySignature Pair according to the Rivine Binary Encoding format.
        """
        encoder.add_all(self.public_key, self.signature)


# Legacy AtomicSwap Fulfillments are not supported,
# as these are not used on any active TFChain network


class FulfillmentAtomicSwap(FulfillmentBaseClass):
    """
    AtomicSwap Fulfillment, used to unlock an AtomicSwap Condition.
    """

    def __init__(self, pub_key=None, signature=None, secret=None):
        self._pub_key = None
        self.public_key = pub_key
        self._signature = None
        self.signature = signature
        self._secret = None
        self.secret = secret

    @property
    def type(self):
        return _FULFILLMENT_TYPE_ATOMIC_SWAP

    @property
    def public_key(self):
        if self._pub_key is None:
            return PublicKey()
        return self._pub_key

    @public_key.setter
    def public_key(self, value):
        if value is None:
            self._pub_key = None
            return
        if not isinstance(value, PublicKey):
            raise Exception(
                "cannot assign value of type {} as FulfillmentAtomicSwap's public key (expected type: PublicKey)".format(
                    type(value)
                )
            )
        self._pub_key = PublicKey(specifier=value.specifier, hash=value.hash)

    @property
    def signature(self):
        if self._signature is None:
            return ED25519Signature()
        return self._signature

    @signature.setter
    def signature(self, value):
        if value is None:
            self._signature = None
        else:
            self._signature = ED25519Signature(value=value)

    @property
    def secret(self):
        if self._secret is None:
            return AtomicSwapSecret()
        return self._secret

    @secret.setter
    def secret(self, value):
        if value is None:
            self._secret = None
        else:
            self._secret = AtomicSwapSecret(value=value)

    def signature_add(self, public_key, signature):
        """
        Implements SignatureCallbackBase.
        """
        self.public_key = public_key
        self.signature = signature

    def from_json_data_object(self, data):
        self._pub_key = PublicKey.from_json(data["publickey"])
        self._signature = ED25519Signature.from_json(data["signature"])
        self._secret = None
        if "secret" in data:
            self._secret = AtomicSwapSecret.from_json(data["secret"])

    def json_data_object(self):
        obj = {"publickey": self.public_key.json(), "signature": self.signature.json()}
        if self._secret is not None:
            obj["secret"] = self.secret.json()
        return obj

    def sia_binary_encode_data(self, encoder):
        encoder.add_all(self.public_key, self.signature, self.secret)

    def rivine_binary_encode_data(self, encoder):
        encoder.add_all(self.public_key, self.signature, self.secret)

    def signature_requests_new(self, input_hash_func, parent_condition):
        if not callable(input_hash_func):
            raise Exception(
                "expected input hash generator func with signature `f(*extra_objects) -> Hash`, not {}".format(
                    type(input_hash_func)
                )
            )
        if not isinstance(parent_condition, ConditionAtomicSwap):
            raise Exception(
                "parent condition of FulfillmentAtomicSwap cannot be of type {}".format(type(parent_condition))
            )
        requests = []
        signee = str(self.public_key.unlockhash)
        # define the input_hash_new generator function,
        # used to create the input hash for creating the signature
        def input_hash_gen(public_key):
            if self._secret is not None:
                return input_hash_func(public_key, self.secret)
            return input_hash_func(public_key)

        # create a signature hash for all signees that haven't signed yet
        for unlockhash in [parent_condition.sender, parent_condition.receiver]:
            if str(unlockhash) != signee:
                requests.append(SignatureRequest(unlockhash=unlockhash, input_hash_gen=input_hash_gen, callback=self))
        return requests

    def is_fulfilled(self, parent_condition):
        if not isinstance(parent_condition, ConditionAtomicSwap):
            raise Exception(
                "parent condition of FulfillmentAtomicSwap cannot be of type {}".format(type(parent_condition))
            )
        return self._signature is not None
