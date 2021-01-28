# TFT on Stellar to Substrate bridge

## Substrate Addresses

In Polkadot (and most Substrate chains), user accounts are identified by a 32-byte (256-bit) AccountId. This is simply the public key for the x25519 cryptography used by Substrate.

Encoded using [SS58](https://github.com/paritytech/substrate/wiki/External-Address-Format-(SS58)), the address length is not fixed but in default implementations it is **48** characters.

## Transferring from Stellar to a Substrate address

Using the Substrate address directly as a destination does not work since the transaction will be refused by the Stellar network since no such account exists.

An easy way to create a migration transaction would be to send the TFT back to the issuer with a memo_text that identifies the chain and the address on that chain.

Unfortunately, the memo_text that can be added to a transaction is only **28** bytes long so this is impossible.

We need to find a different solution to provide the Sustrate address to the bridge in a way that it is verifiable by people/programs looking only at the chain.

A Possible solution is to set data entries on the bridge account. If someone wants to transfer TFT to the Substrate chain, a call is made to the bridge service that adds an entry to it's account containing a 28 byte identifier, the substrate address and the time until when the entry is valid.

The validity is important since the bridge account's reserved balance is increased by adding data-entries.

A fee for creating a transfer slot is possible but makes it a bit more complex.
Options here are to prepare the transaction and identifier by the client, send it to the bridge service that validates, signs and submits it or vice-versa. Both have sequence collision problems so the throughput is decreased even though the first option does not provide the free dos-ing problem

Everyone wanting to send TFT's to the Substrate chain can look up the identifier (or create one if it does not exist yet) and burn the tokens by sending them to the TFT issuer account with the identifier as a memo_text.
The bridge picks up this burning transaction and issues the TFT on the Substrate chain. If the identifier is invalid, the TFT's are reissued to the sending account.
