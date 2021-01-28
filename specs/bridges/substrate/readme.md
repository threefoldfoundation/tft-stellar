# TFT on Stellar to Substrate bridge

## Substrate Addresses

In Polkadot (and most Substrate chains), user accounts are identified by a 32-byte (256-bit) AccountId. This is simply the public key for the x25519 cryptography used by Substrate.

Encoded using [SS58](https://github.com/paritytech/substrate/wiki/External-Address-Format-(SS58)), the address length is not fixed but in default implementations it is **48** characters.

## Transferring from Stellar to a Substrate address

Using the Substrate address directly as a destination does not work since the transaction will be refused by the Stellar network since no such account exists.

An easy way to create a migration transaction would be to send the TFT back to the issuer with a memo_text that identifies the chain and the address on that chain.

Unfortunately, the memo_text that can be added to a transaction is only **28** bytes long so this is impossible.

We need to find a different solution.
