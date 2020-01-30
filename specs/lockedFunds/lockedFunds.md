# Time locks

## Problem

Tfchain (through Rivine) has an easy way of timelocking funds sent to an account.
As traditional blockchains, the sender creates an output but with an extra condition, the timelock.

In Stellar, such a simple timelock mechanism does not exist.

[Timebounds can be set on a transaction](https://www.stellar.org/developers/guides/concepts/transactions.html#time-bounds) but this only declares when a transaction can be submitted to the network. In combination with a [preauthorized transaction](https://www.stellar.org/developers/guides/concepts/multi-sig.html#pre-authorized-transaction) on an escrow account that holds the funds a similar time lock can be achieved.

It does mean however that the preauthorization transaction is known to receiver to be sure to receive the funds after the time lock has expired. This is not an entirely on-chain process as the timelock authorization transaction needs to be communicated to the receiver. The Receiver does have the ability to find the escrow accounts it has signing capabilities for, find out the the hashes of the preauthorized transactions and can look them up itself if such a service is available.

## Sending locked funds

1. Create an escrow account
2. Add a trustline from the escrow account to the custom asset
3. Create a signed unlock transaction (can oly be submitted after the unlock time) that sets the signing options of the escrow account to
    - require only 1 signature
    - remove the escrow account as signer
4. Set the signing options for the escrow account to
    - requires 2 signatures
    - add the receiver as signer
    - add the hash of the unlock transaction as signer
5. Send the custom assets to the escrow account
6. Make the signed unlock transaction available to the receiver

A working example can be found in the [locked funds research folder](../research/lockedunds). It also demonstrates how to find the locked funds in the escrow accounts.
