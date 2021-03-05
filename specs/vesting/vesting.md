# Vesting

People lock (vest), an amount of TFT for a specific time-period. If the price of TFT goes above some predefined limits, 25%, ( or another number) is already released.

The vesting is done over a period of 48 months. Every month 1/48th of the amount is released

Transferring vested funds is not foreseen in the first version but can be added later.

## Implementation concept

Use 1 escrow account per vesting user with normal multisig

Set up an escrow account with the beneficiary ( or any other account set as owner) having a signing weight of 5 and 9 foundation signers with a weight of 1. The weight required to transfer funds or change the signers is set to 10.

The owner always has to sign since the cosigners alone never have enough signing weight.

An extra data entry is set to the escrow account with the vesting scheme ( the formula).

The owner asks to cosign for every transaction. The cosigners can validate if the transaction is valid and cosign if it is.

Since the vesting formula is set on the account, It is visible by everyone and no external data has to be kept
A wallet can show the vested funds as 1 seperate account with a free and locked balance, one can transfer to anyone from the vested account.

The cosigning code will be published to github so everyone can check the code and since all the data resides on-chain, everyone can validate that no rules have been violated.
