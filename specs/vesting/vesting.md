# Vesting

People lock (vest), an amount of TFT for a specific time-period. If the price of TFT goes above some predefined limits, 25%, ( or another number) is already released.

The vesting is done over a period of 48 months. Every month 1/48th of the amount is released

Transferring vested funds is not foreseen in the first version but can be added later.

## Implementation

### concept

Use 1 escrow account per vesting user with normal multisig

Set up an escrow account with the beneficiary ( or any other account set as owner) having a signing weight of 5 and 9 foundation signers with a weight of 1. The weight required to transfer funds or change the signers is set to 10.

The owner always has to sign since the cosigners alone never have enough signing weight.

An extra data entry is set to the escrow account with the vesting scheme ( the formula).

The owner asks to cosign for every transaction. The cosigners can validate if the transaction is valid and cosign if it is.

Since the vesting formula is set on the account, It is visible by everyone and no external data has to be kept
A wallet can show the vested funds as 1 seperate account with a free and locked balance, one can transfer to anyone from the vested account.

The cosigning code will be published to github so everyone can check the code and since all the data resides on-chain, everyone can validate that no rules have been violated.

### Data Entry

As mentioned before, a data entry is added to the escrow account with the vesting scheme ( the formula).

As key of the data entry **tft-vesting** is used. This allows wallets or clients to easily distinguish normal multisig wallets from  vesting wallets.

## Required XLM

Since an escrow account has 12 subentries, it requires 7 XLM. In order to finance future transactions 7.1 XLM as a starting balance is taken.

These XLM's can be recovered by demanding that the last transaction  contains a setoptions operation  setting the signing weight of the owner to 0 and modifying the tresholds to 5  so the cosigners can merge the escrow account to recover the remaining XLM and the do not remain lost forever.

### Examples and testcode

The [testscripts](./testscripts/) folder contains testscripts in Python to create escrow accounts on the Stellar test network.

