from .BaseDataType import BaseDataTypeClass
from .PrimitiveTypes import Hash
from .ConditionTypes import UnlockHash, UnlockHashType

from enum import IntEnum

_SIG_Ed25519 = "ed25519"


class PublicKeySpecifier(IntEnum):
    NIL = 0
    ED25519 = 1

    @classmethod
    def from_json(cls, obj):
        if not obj:
            return PublicKeySpecifier.NIL
        if obj == _SIG_Ed25519:
            return PublicKeySpecifier.ED25519
        raise Exception("{} is an invalid Public Key specifier".format(obj))

    def __str__(self):
        if self == PublicKeySpecifier.ED25519:
            return _SIG_Ed25519
        return ""

    __repr__ = __str__

    json = __str__


class PublicKey(BaseDataTypeClass):
    """
    A PublicKey is a public key prefixed by a Specifier. The Specifier
	indicates the algorithm used for signing and verification.
    The other part of the PublicKey is the hash itself.
    """

    def __init__(self, specifier=None, hash=None):
        self._specifier = PublicKeySpecifier.NIL
        self._hash = None

        self.specifier = specifier
        self.hash = hash

    @classmethod
    def from_json(cls, obj):
        if not obj:
            return cls()
        if not isinstance(obj, str):
            raise Exception("expected JSON-encoded PublicKey to be a string, not {}".format(type(obj)))
        parts = obj.split(sep=":", maxsplit=2)
        if len(parts) != 2:
            raise Exception("invalid JSON-encoded PublicKey: {}".format(obj))
        pk = cls()
        pk._specifier = PublicKeySpecifier.from_json(parts[0])
        pk._hash = Hash.from_json(parts[1])
        return pk

    @property
    def specifier(self):
        return self._specifier

    @specifier.setter
    def specifier(self, value):
        if value == None:
            value = PublicKeySpecifier.NIL
        elif not isinstance(value, PublicKeySpecifier):
            raise Exception("expected value to be a PublicKeySpecifier, not {}".format(type(value)))
        self._specifier = value

    @property
    def hash(self):
        if self._hash is None:
            return Hash()
        return self._hash

    @hash.setter
    def hash(self, value):
        if value is None:
            self._hash = None
        elif isinstance(value, Hash):
            self._hash = value
        else:
            self._hash = Hash(value=value)

    def __str__(self):
        return str(self.specifier) + ":" + str(self.hash)

    __repr__ = __str__

    json = __str__

    @property
    def unlockhash(self):
        """
        Return the unlock hash generated from this public key.
        """
        e = j.data.rivine.encoder_sia_get()
        self.sia_binary_encode(e)
        # need to encode again to add the length
        data = e.data
        e = j.data.rivine.encoder_sia_get()
        e.add_slice(data)
        hash = bytearray.fromhex(j.data.hash.blake2_string(e.data))
        return UnlockHash(type=UnlockHashType.PUBLIC_KEY, hash=hash)

    @staticmethod
    def _pad_specifier(specifier):
        _SPECIFIER_SIZE = 16
        value = specifier.encode("utf-8")
        return value + b"\0" * (_SPECIFIER_SIZE - len(value))

    def sia_binary_encode(self, encoder):
        """
        Encode this binary data according to the Sia Binary Encoding format.
        """
        encoder.add_array(PublicKey._pad_specifier(str(self.specifier)))
        encoder.add_slice(self.hash.value)

    def rivine_binary_encode(self, encoder):
        """
        Encode this binary data according to the Rivine Binary Encoding format.
        """
        encoder.add_int8(int(self.specifier))
        encoder.add(self.hash)
