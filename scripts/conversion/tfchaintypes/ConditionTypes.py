import hashlib
from pyblake2 import blake2b
from datetime import datetime, timedelta

from .PrimitiveTypes import BinaryData, Hash
from .rivine.RivineDataFactory import RivineDataFactory
from .TFChainTypesFactory import TFChainTypesFactory


_CONDITION_TYPE_NIL = 0
_CONDITION_TYPE_UNLOCK_HASH = 1
_CONDITION_TYPE_ATOMIC_SWAP = 2
_CONDITION_TYPE_LOCKTIME = 3
_CONDITION_TYPE_MULTI_SIG = 4


class ConditionFactory(object):
    """
    Condition Factory class
    """

    @classmethod
    def from_json(cls, obj):
        ct = obj.get("type", 0)
        if ct == _CONDITION_TYPE_NIL:
            return ConditionNil.from_json(obj)
        if ct == _CONDITION_TYPE_UNLOCK_HASH:
            return ConditionUnlockHash.from_json(obj)
        if ct == _CONDITION_TYPE_ATOMIC_SWAP:
            return ConditionAtomicSwap.from_json(obj)
        if ct == _CONDITION_TYPE_LOCKTIME:
            return ConditionLockTime.from_json(obj)
        if ct == _CONDITION_TYPE_MULTI_SIG:
            return ConditionMultiSignature.from_json(obj)
        raise Exception("unsupport condition type {}".format(ct))

    @classmethod
    def from_recipient(cls, recipient, lock=None):
        """
        Create automatically a recipient condition based on any accepted pythonic value (combo).
        """

        # define base condition
        if isinstance(recipient, ConditionBaseClass):
            condition = recipient
        else:
            condition = None
            if recipient is None:
                # free-for-all wallet
                condition = cls.nil_new()
            elif isinstance(recipient, (UnlockHash, str)):
                # single sig wallet
                condition = cls.unlockhash_new(unlockhash=recipient)
            elif isinstance(recipient, (bytes, bytearray)):
                # single sig wallet
                condition = cls.unlockhash_new(unlockhash=recipient.hex())
            elif isinstance(recipient, list):
                # multisig to an all-for-all wallet
                condition = cls.multi_signature_new(min_nr_sig=len(recipient), unlockhashes=recipient)
            elif isinstance(recipient, tuple):
                # multisig wallet with custom x-of-n definition
                if len(recipient) != 2:
                    raise Exception(
                        "recipient is expected to be a tupple of 2 values in the form (sigcount,hashes) or (hashes,sigcount), cannot be of length {}".format(
                            len(recipient)
                        )
                    )
                # allow (sigs,hashes) as well as (hashes,sigs)
                if isinstance(recipient[0], int):
                    condition = cls.multi_signature_new(min_nr_sig=recipient[0], unlockhashes=recipient[1])
                else:
                    condition = cls.multi_signature_new(min_nr_sig=recipient[1], unlockhashes=recipient[0])
            else:
                raise Exception("invalid type for recipient parameter: {}".format(type(recipient)))

        # if lock is defined, define it as a locktime value
        if lock is not None:
            condition = cls.locktime_new(lock=lock, condition=condition)

        # return condition
        return condition

    @classmethod
    def nil_new(cls):
        """
        Create a new Nil Condition, which can be fulfilled by any SingleSig. Fulfillment.
        """
        return ConditionNil()

    @classmethod
    def unlockhash_new(cls, unlockhash=None):
        """
        Create a new UnlockHash Condition, which can be
        fulfilled by the matching SingleSig. Fulfillment.
        """
        return ConditionUnlockHash(unlockhash=unlockhash)

    @classmethod
    def atomic_swap_new(cls, sender=None, receiver=None, hashed_secret=None, lock_time=None):
        """
        Create a new AtomicSwap Condition, which can be
        fulfilled by the AtomicSwap Fulfillment.
        """
        return ConditionAtomicSwap(sender=sender, receiver=receiver, hashed_secret=hashed_secret, lock_time=lock_time)

    @classmethod
    def locktime_new(cls, lock=None, condition=None):
        """
        Create a new LockTime Condition, which can be fulfilled by a fulfillment
        when the relevant timestamp/block has been reached as well as the fulfillment fulfills the internal condition.
        """
        return ConditionLockTime(lock=lock, condition=condition)

    @classmethod
    def multi_signature_new(cls, min_nr_sig=0, unlockhashes=None):
        """
        Create a new MultiSignature Condition, which can be fulfilled by a matching MultiSignature Fulfillment.
        """
        return ConditionMultiSignature(unlockhashes=unlockhashes, min_nr_sig=min_nr_sig)

    @classmethod
    def output_lock_new(cls, value):
        """
        Creates a new output lock.
        """
        return OutputLock(value=value)


class OutputLock:
    # as defined by Rivine
    _MIN_TIMESTAMP_VALUE = 500 * 1000 * 1000

    def __init__(self, value=None, current_timestamp=None):
        if current_timestamp is None:
            current_timestamp = int(datetime.now().timestamp())
        elif not isinstance(current_timestamp, int):
            raise Exception("current timestamp has to be an integer")

        if value is None:
            self._value = 0
        elif isinstance(value, OutputLock):
            self._value = value.value
        elif isinstance(value, int):
            if value < 0:
                raise Exception("output lock value cannot be negative")
            self._value = int(value)
        elif isinstance(value, str):
            value = value.lstrip()
            if value[0] == "+":
                # interpret string as a duration
                offset = j.data.types.duration.fromString(value[1:])
                self._value = current_timestamp + offset
            else:
                # interpret string as a datetime
                self._value = j.data.types.datetime.fromString(value)
        elif isinstance(value, timedelta):
            self._value = current_timestamp + int(value.total_seconds())
        elif isinstance(value, datetime):
            self._value = int(value.timestamp())
        else:
            raise Exception("cannot set OutputLock using invalid type {}".format(type(value)))

    def __int__(self):
        return self._value

    def __str__(self):
        if self.is_timestamp:
            return j.data.time.epoch2HRDateTime(self._value)
        return str(self._value)

    __repr__ = __str__

    @property
    def value(self):
        """
        The internal lock (integral) value.
        """
        return self._value

    @property
    def is_timestamp(self):
        """
        Returns whether or not this value is a timestamp.
        """
        return self._value >= OutputLock._MIN_TIMESTAMP_VALUE

    def locked_check(self, height, time):
        """
        Check if the the output is still locked on the given block height/time.
        """
        if self.is_timestamp:
            return time < self._value
        return height < self._value


from abc import abstractmethod

from .BaseDataType import BaseDataTypeClass


class ConditionBaseClass(BaseDataTypeClass):
    @classmethod
    def from_json(cls, obj):
        ff = cls()
        ct = obj.get("type", 0)
        if ff.type != ct:
            raise Exception("condition is expected to be of type {}, not {}".format(ff.type, ct))
        ff.from_json_data_object(obj.get("data", {}))
        return ff

    @property
    @abstractmethod
    def type(self):
        pass

    @property
    def lock(self):
        return OutputLock()

    @property
    @abstractmethod
    def unlockhash(self):
        """
        The unlock hash for this condition.
        """
        pass

    def unwrap(self):
        """
        Return the most inner condition, should it apply to this condition,
        otherwise the condition itself will be returned.
        """
        return self

    @abstractmethod
    def from_json_data_object(self, data):
        pass

    @abstractmethod
    def json_data_object(self):
        pass

    def json(self):
        obj = {"type": self.type}
        data = self.json_data_object()
        if data:
            obj["data"] = data
        return obj

    @abstractmethod
    def sia_binary_encode_data(self, encoder):
        pass

    def sia_binary_encode(self, encoder):
        """
        Encode this Condition according to the Sia Binary Encoding format.
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
        Encode this Condition according to the Rivine Binary Encoding format.
        """
        encoder.add_int8(int(self.type))
        data_enc = j.data.rivine.encoder_rivine_get()
        self.rivine_binary_encode_data(data_enc)
        encoder.add_slice(data_enc.data)


from enum import IntEnum


class UnlockHashType(IntEnum):
    NIL = 0
    PUBLIC_KEY = 1
    ATOMIC_SWAP = 2
    MULTI_SIG = 3

    @classmethod
    def from_json(cls, obj):
        if type(obj) is str:
            obj = int(obj)
        elif not isinstance(obj, int):
            raise Exception(
                "UnlockHashType is expected to be JSON-encoded as an int, not {}".format(type(obj))
            )
        return cls(obj)  # int -> enum

    def json(self):
        return int(self)


class UnlockHash(BaseDataTypeClass):
    """
    An UnlockHash is a specially constructed hash of the UnlockConditions type,
    with a fixed binary length of 33 and a fixed string length of 78 (string version includes a checksum).
    """

    _TYPE_SIZE_HEX = 2
    _CHECKSUM_SIZE = 6
    _CHECKSUM_SIZE_HEX = _CHECKSUM_SIZE * 2
    _HASH_SIZE = 32
    _HASH_SIZE_HEX = _HASH_SIZE * 2
    _TOTAL_SIZE_HEX = _TYPE_SIZE_HEX + _CHECKSUM_SIZE_HEX + _HASH_SIZE_HEX

    def __init__(self, type=None, hash=None):
        self._type = UnlockHashType.NIL
        self.type = type
        self._hash = Hash()
        self.hash = hash

    @classmethod
    def from_json(cls, obj):
        if not isinstance(obj, str):
            raise Exception("UnlockHash is expected to be JSON-encoded as an str, not {}".format(type(obj)))
        if len(obj) != UnlockHash._TOTAL_SIZE_HEX:
            raise Exception(
                "UnlockHash is expexcted to be of length {} when JSON-encoded, not of length {}".format(
                    UnlockHash._TOTAL_SIZE_HEX, len(obj)
                )
            )

        t = UnlockHashType(int(obj[: UnlockHash._TYPE_SIZE_HEX]))
        h = Hash(obj[UnlockHash._TYPE_SIZE_HEX : UnlockHash._TYPE_SIZE_HEX + UnlockHash._HASH_SIZE_HEX])
        uh = cls(type=t, hash=h)

        if t == UnlockHashType.NIL:
            expectedNH = b"\x00" * UnlockHash._HASH_SIZE
            if h.value != expectedNH:
                raise Exception("unexpected nil hash {}".format(h.value.hex()))
        else:
            expected_checksum = uh._checksum()[: UnlockHash._CHECKSUM_SIZE].hex()
            checksum = obj[-UnlockHash._CHECKSUM_SIZE_HEX :]
            if expected_checksum != checksum:
                raise Exception("unexpected checksum {}, expected {}".format(checksum, expected_checksum))

        return uh

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value == None:
            value = UnlockHashType.NIL
        elif not isinstance(value, UnlockHashType):
            raise Exception("UnlockHash's type has to be of type UnlockHashType, not {}".format(type(value)))
        self._type = value

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, value):
        self._hash.value = value

    def __str__(self):
        checksum = self._checksum()[: UnlockHash._CHECKSUM_SIZE].hex()
        return "{}{}{}".format(bytearray([int(self._type)]).hex(), str(self._hash), checksum)

    def _checksum(self):
        if self._type == UnlockHashType.NIL:
            return b"\x00" * UnlockHash._CHECKSUM_SIZE
        e = RivineDataFactory.encoder_rivine_get()
        e.add_int8(int(self._type))
        e.add(self._hash)
        h = blake2b(e.data, digest_size=32)
        return bytearray.fromhex(h.hexdigest())

    __repr__ = __str__

    json = __str__

    def __eq__(self, other):
        try:
            other = UnlockHash._op_other_as_unlockhash(other)
        except:
            return False
        other = UnlockHash._op_other_as_unlockhash(other)
        return self.type == other.type and self.hash == other.hash

    def __ne__(self, other):
        try:
            other = UnlockHash._op_other_as_unlockhash(other)
        except:
            return True

        return self.type != other.type or self.hash != other.hash

    def __hash__(self):
        return hash(str(self))

    @staticmethod
    def _op_other_as_unlockhash(other):
        if isinstance(other, str):
            other = UnlockHash.from_json(other)
        elif not isinstance(other, UnlockHash):
            raise Exception("UnlockHash of type {} is not supported".format(type(other)))
        return other

    def sia_binary_encode(self, encoder):
        """
        Encode this unlock hash according to the Sia Binary Encoding format.
        """
        encoder.add_byte(int(self._type))
        encoder.add(self._hash)

    def rivine_binary_encode(self, encoder):
        """
        Encode this unlock hash according to the Rivine Binary Encoding format.
        """
        encoder.add_int8(int(self._type))
        encoder.add(self._hash)


class ConditionNil(ConditionBaseClass):
    """
    ConditionNil class
    """

    @property
    def type(self):
        return _CONDITION_TYPE_NIL

    @property
    def unlockhash(self):
        return UnlockHash(type=UnlockHashType.NIL)

    def from_json_data_object(self, data):
        if data not in (None, {}):
            raise Exception("unexpected JSON-encoded nil condition {} (type: {})".format(data, type(data)))

    def json_data_object(self):
        return None

    def sia_binary_encode_data(self, encoder):
        pass  # nothing to do

    def rivine_binary_encode_data(self, encoder):
        pass  # nothing to do


class ConditionUnlockHash(ConditionBaseClass):
    """
    ConditionUnlockHash class
    """

    def __init__(self, unlockhash=None):
        self._unlockhash = None
        self.unlockhash = unlockhash

    @property
    def type(self):
        return _CONDITION_TYPE_UNLOCK_HASH

    @property
    def unlockhash(self):
        if self._unlockhash is None:
            return UnlockHash()
        return self._unlockhash

    @unlockhash.setter
    def unlockhash(self, value):
        if value is None:
            self._unlockhash = None
            return
        if isinstance(value, UnlockHash):
            self._unlockhash = value
            return
        self._unlockhash = UnlockHash.from_json(value)

    def from_json_data_object(self, data):
        self.unlockhash = UnlockHash.from_json(data["unlockhash"])

    def json_data_object(self):
        return {"unlockhash": self.unlockhash.json()}

    def sia_binary_encode_data(self, encoder):
        encoder.add(self.unlockhash)

    def rivine_binary_encode_data(self, encoder):
        encoder.add(self.unlockhash)


class AtomicSwapSecret(BinaryData):
    SIZE = 32

    """
    Atomic Swap Secret Object, a special type of BinaryData
    """

    def __init__(self, value=None):
        super().__init__(value, fixed_size=AtomicSwapSecret.SIZE, strencoding="hex")

    @classmethod
    def from_json(cls, obj):
        if not isinstance(obj, str):
            raise Exception("secret is expected to be an encoded string when part of a JSON object")
        return cls(value=obj)

    @classmethod
    def random(cls):
        return cls(value=j.data.idgenerator.generateXByteID(AtomicSwapSecret.SIZE))


class AtomicSwapSecretHash(BinaryData):
    SIZE = 32

    """
    Atomic Swap Secret Hash, a special type of BinaryData
    """

    def __init__(self, value=None):
        super().__init__(value, fixed_size=AtomicSwapSecretHash.SIZE, strencoding="hex")

    @classmethod
    def from_json(cls, obj):
        if not isinstance(obj, str):
            raise Exception("secret hash is expected to be an encoded string when part of a JSON object")
        return cls(value=obj)

    @classmethod
    def from_secret(cls, secret):
        if not isinstance(secret, AtomicSwapSecret):
            raise Exception(
                "secret is expected to be of type AtomicSwapSecret, not to be of type {}".format(type(secret))
            )
        return cls(value=hashlib.sha256(secret.value).digest())


class ConditionAtomicSwap(ConditionBaseClass):
    """
    ConditionAtomicSwap class
    """

    def __init__(self, sender=None, receiver=None, hashed_secret=None, lock_time=None):
        self._sender = None
        self.sender = sender
        self._receiver = None
        self.receiver = receiver
        self._hashed_secret = None
        self.hashed_secret = hashed_secret
        self._lock_time = 0
        self.lock_time = lock_time

    @property
    def type(self):
        return _CONDITION_TYPE_ATOMIC_SWAP

    @property
    def unlockhash(self):
        e = j.data.rivine.encoder_rivine_get()
        self.sia_binary_encode_data(e)
        # need to encode again to add the length
        data = e.data
        e = j.data.rivine.encoder_sia_get()
        e.add_slice(data)
        hash = bytearray.fromhex(j.data.hash.blake2_string(e.data))
        return UnlockHash(type=UnlockHashType.ATOMIC_SWAP, hash=hash)

    @property
    def sender(self):
        if self._sender is None:
            return UnlockHash()
        return self._sender

    @sender.setter
    def sender(self, value):
        if value is None:
            self._sender = None
        else:
            if isinstance(value, str):
                value = UnlockHash.from_json(value)
            elif not isinstance(value, UnlockHash):
                raise Exception(
                    "Atomic Swap's sender unlock hash has to be of type UnlockHash, not {}".format(type(value))
                )
            if value.type not in (UnlockHashType.PUBLIC_KEY, UnlockHashType.NIL):
                raise Exception(
                    "Atomic Swap's sender unlock hash type cannot be {} (expected: 0 or 1)".format(value.type)
                )
            self._sender = value

    @property
    def receiver(self):
        if self._receiver is None:
            return UnlockHash()
        return self._receiver

    @receiver.setter
    def receiver(self, value):
        if value is None:
            self._receiver = None
        else:
            if isinstance(value, str):
                value = UnlockHash.from_json(value)
            elif not isinstance(value, UnlockHash):
                raise Exception(
                    "Atomic Swap's receiver unlock hash has to be of type UnlockHash, not {}".format(type(value))
                )
            if value.type not in (UnlockHashType.PUBLIC_KEY, UnlockHashType.NIL):
                raise Exception(
                    "Atomic Swap's receiver unlock hash type cannot be {} (expected: 0 or 1)".format(value.type)
                )
            self._receiver = value

    @property
    def hashed_secret(self):
        if self._hashed_secret is None:
            return BinaryData()
        return self._hashed_secret

    @hashed_secret.setter
    def hashed_secret(self, value):
        if value is None:
            self._hashed_secret = None
        else:
            self._hashed_secret = AtomicSwapSecretHash(value=value)

    @property
    def lock_time(self):
        return self._lock_time

    @lock_time.setter
    def lock_time(self, value):
        if value is None:
            self._lock_time = 0
        else:
            lock = OutputLock(value=value)
            if not lock.is_timestamp:
                raise Exception(
                    "ConditionAtomicSwap only accepts timestamps as the lock value, not block heights: {} is invalid".format(
                        value
                    )
                )
            self._lock_time = lock.value

    def from_json_data_object(self, data):
        self.sender = UnlockHash.from_json(data["sender"])
        self.receiver = UnlockHash.from_json(data["receiver"])
        self.hashed_secret = AtomicSwapSecretHash(value=data["hashedsecret"])
        self.lock_time = int(data["timelock"])

    def json_data_object(self):
        return {
            "sender": self.sender.json(),
            "receiver": self.receiver.json(),
            "hashedsecret": self.hashed_secret.json(),
            "timelock": self.lock_time,
        }

    def sia_binary_encode_data(self, encoder):
        encoder.add_all(self.sender, self.receiver, self.hashed_secret, self.lock_time)

    def rivine_binary_encode_data(self, encoder):
        encoder.add_all(self.sender, self.receiver, self.hashed_secret, self.lock_time)


class ConditionLockTime(ConditionBaseClass):
    """
    ConditionLockTime class
    """

    def __init__(self, condition=None, lock=None):
        self._condition = None
        self.condition = condition
        self._lock = None
        self.lock = lock

    @property
    def type(self):
        return _CONDITION_TYPE_LOCKTIME

    @property
    def unlockhash(self):
        return self.condition.unlockhash

    @property
    def lock(self):
        if self._lock is None:
            return OutputLock()
        return self._lock

    @lock.setter
    def lock(self, value):
        self._lock = OutputLock(value=value)

    @property
    def condition(self):
        if self._condition is None:
            return ConditionUnlockHash()
        return self._condition

    @condition.setter
    def condition(self, value):
        if value is None:
            self._condition = None
            return
        if not isinstance(value, ConditionBaseClass):
            raise Exception(
                "ConditionLockTime's condition is expected to be a subtype of ConditionBaseClass, not of type {}".format(
                    type(value)
                )
            )
        self._condition = value

    def unwrap(self):
        return self.condition

    def from_json_data_object(self, data):
        self.lock = int(data["locktime"])
        cond = ConditionFactory.from_json(obj=data["condition"])
        if cond.type not in (_CONDITION_TYPE_UNLOCK_HASH, _CONDITION_TYPE_MULTI_SIG, _CONDITION_TYPE_NIL):
            raise Exception("internal condition of ConditionLockTime cannot be of type {}".format(cond.type))
        self.condition = cond

    def json_data_object(self):
        return {"locktime": self.lock.value, "condition": self.condition.json()}

    def sia_binary_encode_data(self, encoder):
        encoder.add(self.lock.value)
        encoder.add_array(bytearray([int(self.condition.type)]))
        self.condition.sia_binary_encode_data(encoder)

    def rivine_binary_encode_data(self, encoder):
        encoder.add(self.lock.value)
        encoder.add_int8(int(self.condition.type))
        self.condition.rivine_binary_encode_data(encoder)


class ConditionMultiSignature(ConditionBaseClass):
    """
    ConditionMultiSignature class
    """

    def __init__(self, unlockhashes=None, min_nr_sig=0):
        self._unlockhashes = []
        if unlockhashes:
            for uh in unlockhashes:
                self.add_unlockhash(uh)
        self._min_nr_sig = 0
        self.required_signatures = min_nr_sig

    @property
    def type(self):
        return _CONDITION_TYPE_MULTI_SIG

    @property
    def unlockhash(self):
        uhs = sorted(self.unlockhashes, key=lambda uh: str(uh))
        tree = TFChainTypesFactory.merkle_tree_new()
        tree.push(RivineDataFactory.sia_encode(len(uhs)))
        for uh in uhs:
            tree.push(RivineDataFactory.sia_encode(uh))
        tree.push(RivineDataFactory.sia_encode(self.required_signatures))
        return UnlockHash(type=UnlockHashType.MULTI_SIG, hash=tree.root())

    @property
    def unlockhashes(self):
        return self._unlockhashes

    def add_unlockhash(self, uh):
        if uh is None:
            self._unlockhashes.append(UnlockHash())
        elif isinstance(uh, UnlockHash):
            self._unlockhashes.append(uh)
        elif isinstance(uh, str):
            self._unlockhashes.append(UnlockHash.from_json(uh))
        else:
            raise Exception("cannot add UnlockHash with invalid type {}".format(type(uh)))

    @property
    def required_signatures(self):
        return self._min_nr_sig

    @required_signatures.setter
    def required_signatures(self, value):
        if value is None:
            self._min_nr_sig = 0
            return
        if not isinstance(value, int):
            raise Exception(
                "ConditionMultiSignature's required signatures value is expected to be of type int, not {}".format(
                    type(value)
                )
            )
        self._min_nr_sig = int(value)

    def from_json_data_object(self, data):
        self._min_nr_sig = int(data["minimumsignaturecount"])
        self._unlockhashes = []
        for uh in data["unlockhashes"]:
            uh = UnlockHash.from_json(uh)
            self._unlockhashes.append(uh)

    def json_data_object(self):
        return {"minimumsignaturecount": self._min_nr_sig, "unlockhashes": [uh.json() for uh in self._unlockhashes]}

    def sia_binary_encode_data(self, encoder):
        encoder.add(self._min_nr_sig)
        encoder.add_slice(self._unlockhashes)

    def rivine_binary_encode_data(self, encoder):
        encoder.add_int64(self._min_nr_sig)
        encoder.add_slice(self._unlockhashes)
