from .crypto.MerkleTree import Tree
from hashlib import blake2b


class TFChainTypesFactory(object):
    """
    TFChain Types Factory class
    """

    @staticmethod
    def merkle_tree_new():
        """
        Create a new MerkleTree
        """

        def blake2(s, digest_size=32):
            """Calculate blake2 hash of input string

            @param s: String value to hash
            @type s: string

            @returns: blake2 hash of the input value
            @rtype: string
            """
            if isinstance(s, str):  # check string direct otherwise have to pass in j
                s = s.encode()
            h = blake2b(s, digest_size=digest_size)

            return h.hexdigest()

        return Tree(hash_func=lambda o: bytes.fromhex(blake2(o)))
