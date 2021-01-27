# Vesting

People lock (vest), an amount of TFT for a specific time-period. If the price of TFT goes above some predefined limits, 25%, ( or another number) is already released.

Since there are no smart contracts in Stellar, every amount that has seperate rules must be placed on a seperate escrow account so the vested amount is split up in blocks.

## Later

It should also be possible to transfer vested funds to another account. The vesting rules stay the same, only the owner changes.

Transferring vested blocks to someone else can be implemented by having another address as the beneficiary and the signers for this address can be modified by the one holding control of this account. This does mean that transferring a vested block partially is not possible.

## unlocking by price

Releasing a vested block if a certain price condition is reached can be achieved by adding a multisig 
signer to the vesting escrow account ( on which the price condition is set as extra data). the multisig signer is the oracle for the TFT price which needs to be validated and signed by multiple oracle validators.

To check: can the preauthsigner transaction hash be added before it is already signed, in this case, no price condition must be set on the escrow account as extra data.


# 