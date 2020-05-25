from .PrimitiveTypes import BinaryData, Hash, Currency, Blockstake
from .CryptoTypes import PublicKey, PublicKeySpecifier

from .crypto.MerkleTree import Tree


class TFChainTypesFactory(object):
    """
    TFChain Types Factory class
    """

    @staticmethod
    def currency_new(value=0):
        """
        Create a new currency value.
        
        @param value: str or int that defines the value to be set, 0 by default
        """
        return Currency(value=value)

    @staticmethod
    def blockstake_new(value=0):
        """
        Create a new block stake value.

        @param value: str or int that defines the value to be set, 0 by default
        """
        return Blockstake(value=value)

    @staticmethod
    def binary_data_new(value=None, fixed_size=None, strencoding=None):
        """
        Create a new binary data value.
        
        @param value: bytearray, bytes or str that defines the hash value to be set, nil hash by default
        """
        return BinaryData(value=value, fixed_size=fixed_size, strencoding=strencoding)

    @staticmethod
    def public_key_new(hash=None):
        """
        Create a new NIL or ED25519 public key.
        
        @param hash: bytearray, bytes or str that defines the hash value to be set, nil hash by default
        """
        if not hash:
            return PublicKey()
        return PublicKey(specifier=PublicKeySpecifier.ED25519, hash=hash)

    @staticmethod
    def public_key_from_json(self, obj):
        """
        Create a new public key from a json string.
        
        @param obj: str that contains a nil str or a json string
        """
        return PublicKey.from_json(obj)

    @staticmethod
    def merkle_tree_new():
        """
        Create a new MerkleTree
        """
        return Tree(hash_func=lambda o: bytes.fromhex(j.data.hash.blake2_string(o)))
