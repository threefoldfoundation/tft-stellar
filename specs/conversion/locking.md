# Locking of tchain accounts during the conversion

In the v1.3 release of tfchain, locking of accounts has been added to support the transition to a different blockchain platform.

## Why

Eventually, all TFT have to be migrated after which no TFT remains on tchain, the problem is solved then.

During the transition, the wallet of the user needs to initiate the conversion as explained in the [conversion document](./conversion.md).

Without account locking, some users might have already migrated and some might have not. Part of the TFT would circulate on tfchain and some would circulate on the new platform.

A wallet of a migrated user would constantly have to check if some funds are sent to an old tfchain address, making it impossible to fade out the tfchain functionality in the wallet.

If tfchain needs to remain active, the consensus needs to remain running with enough nodes as well and the codebase has to be maintained, making us run on two platforms.

An account lock is a transaction with a unique transaction hash. This transaction hash should be added to the coin issuance transaction on the new platform. This proves there is no random coin creation and makes the coin creation traceable for everyone to see that it is a migration from the tfchain platform.

## Alternatives

### Stop accepting transactions in the consensus

### Atomic Swaps

## Process
