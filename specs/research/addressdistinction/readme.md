# Distinction between Rivine and Stellar addresses

Rivine uses default ed25519 keys, meaning a private key of 64 bytes from a 32 byte entropy (is actually the private key) and a public key size of 32 bytes. Rivine hashes the public key along with the key alorithm to create an unlockhash. The address is then formed by concatenating the type, the hash and a checksum and hexencoding it.

Stellar also uses uses default ed25519 keys. A Stellar seed is just a base32 encoded concatatantion of a versionbyte, a 32byte private key and a checksum. An address is the rawseed used to create an ed25519 keypair after which the versionbyte is concatenated with the public key and a checksum and base32 encoded.

An easy distinction is to look at the encoding (hex or base32).
