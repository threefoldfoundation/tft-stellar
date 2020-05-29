# Locking of tchain accounts during the conversion

## Migration from Rivine to Stellar

We will use a process we called "locked Conversion Transaction".

This is basically a controlled process in which we lock the account on Rivine before the transaction, metadata is inserted in the Stellar minting action which points back to the originating funds, once the transaction succeeded the account gets permanently locked and metadata written to point to the new account on Stellar. The account address on Stellar is a derivate from the account on Rivine which makes it easy for everyone to follow the flow.

We first wanted to use atomic swaps for this but this had some issues to do with transparancy and complexity for the user.

## Why did we choose this path

Rule nr 1 all TFT have to be migrated after which no TFT remains on the rivine chain (TF Chain).

During the transition, the wallet of the user needs to initiate the conversion as explained in the [conversion document](./conversion.md).

Without account locking, some users might have already migrated and some might have not. Part of the TFT would circulate on tfchain and some would circulate on the new platform.

A wallet of a migrated user would constantly have to check if some funds are sent to an old tfchain address, making it impossible to fade out the tfchain functionality in the wallet.

If tfchain needs to remain active, the consensus needs to remain running with enough nodes as well and the codebase has to be maintained, making us run on two platforms.

An account lock is a transaction with a unique transaction hash. This transaction hash should be added to the coin issuance transaction on the new platform. This proves there is no random coin creation and makes the coin creation traceable for everyone to see that it is a migration from the tfchain platform.

## Alternatives

### Stop accepting transactions in the consensus

In other words, pull the plug.

Essentially the same but not so graceful and no hashes to include in the coin issuance transaction.

### Atomic Swaps

As explained in the "why", this means having TFT running on both platforms and the traceability of coin creation because of the migration is far less.

## Info

In the v1.3 release of tfchain, locking of accounts has been added to support the transition to a different blockchain platform.

See the info in the explorer: `https://explorer.testnet.threefoldtoken.com/explorer/authcoin/status?addr=address`
