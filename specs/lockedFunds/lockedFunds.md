# Time locks

Tfchain (through Rivine) has an easy way of timelocking funds sent to an account.
As traditional blockchains, the sender creates an output but with an extra condition, the timelock.

In Stellar, such a simple timelock mechanism does not exist.

[Timebounds can be set on a transaction](https://www.stellar.org/developers/guides/concepts/transactions.html#time-bounds) but this only declares when a transaction can be submitted to the network. In combination with a [preauthorized transaction](https://www.stellar.org/developers/guides/concepts/multi-sig.html#pre-authorized-transaction) on an escrow account that holds the funds a similar time lock can be achieved.

It does mean however that the preauthorization transaction is known to receiver to be sure to receive the funds after the time lock has expired. This is not an entirely on-chain process as the timelock authorization transaction needs to be communicated to the receiver. The Receiver does have the ability to find the escrow accounts it has signing capabilities for, find out the the hashes of the preauthorized transactions and can look them up itself if such a service is available.
