# Time locks

## Problem

Tfchain (through Rivine) has an easy way of timelocking funds sent to an account.
As traditional blockchains, the sender creates an output but with an extra condition, the timelock.

In Stellar, such a simple timelock mechanism does not exist.

[Timebounds can be set on a transaction](https://www.stellar.org/developers/guides/concepts/transactions.html#time-bounds) but this only declares when a transaction can be submitted to the network. In combination with a [preauthorized transaction](https://www.stellar.org/developers/guides/concepts/multi-sig.html#pre-authorized-transaction) on an escrow account that holds the funds a similar time lock can be achieved.

It does mean however that the preauthorization transaction is known to receiver to be sure to receive the funds after the time lock has expired. This is not an entirely on-chain process as the timelock authorization transaction needs to be communicated to the receiver. The Receiver does have the ability to find the escrow accounts it has signing capabilities for and  find out the hashes of the preauthorized transactions.

In order for the sender and receiver to communicate the unlock transactions, an unlock transaction store service is available.
This service allows a sender to publish the unlock transaction and allows the receiver to find it by the hash of the transaction.

## Sending locked funds

1. Create an escrow account
2. Add a trustline from the escrow account to the custom asset
3. Create a signed unlock transaction (can only be submitted after the unlock time) that sets the signing options of the escrow account to
    - require only 1 signature
    - remove the escrow account as signer
4. Publish the signed unlock transaction to the  public unlock transaction store
5. Set the signing options for the escrow account to
    - requires 2 signatures
    - add the receiver as signer
    - add the hash of the unlock transaction as signer
6. Send the custom assets to the escrow account

A working example can be found in the [locked funds research folder](../research/lockedfunds). It also demonstrates how to find the locked funds in the escrow accounts.

## Implementations

## Clients

[Jumpscale](https://github.com/threefoldtech/jumpscaleX_libs/tree/development/JumpscaleLibs/clients/stellar) has a working implementation of locked tokens.

### Unlock transaction store

An implementation of an unlock transaction store is available as a Jumpscale actor [in this repository](../../ThreeBotPackages/unlock-service).

For testnet, this service is deployed at `hhtps://testnet.threefold.io`.
