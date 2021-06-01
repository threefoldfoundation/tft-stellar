# Vesting

People lock (vest), an amount of TFT for a specific time-period. If the price of TFT goes above some predefined limits, 25%, ( or another number) is already released.

The vesting is done over a period of 48 months. Every month 1/48th of the amount is released

Transferring vested funds is not foreseen in the first version but can be added later.

## Implementation

### Concept

Vesting is done on the Stellar network

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

## Recovery of unused vesting accounts

If people create vesting accounts but do not vest, this creates dangling vesting accounts and drains XLM from the vesting account creation services.

In order to clean up dangling vesting accounts, a preauthorization transaction is added as a signer.

This transaction signer has a weight of 10, can only be executed as the next transaction on the vesting account, and executes the following operations:

- Removes the TFT trustline
- Removes the tft-vesting data entry
- Merges the account back to the account that created it to recover the XLM on it

This transaction will fail if there are TFT's on the vesting account since the removal of the trustline will fail after which this transaction signer is removed from the vesting account.

The recovery transaction can only be submitted 2 weeks after the creation giving the user more than enough time to transfer TFT's to it.

Adding this extra signer requires an extra 0.5 XLM per escrow account.

They are published to the unlock-service  which already contain the unlocktransactions for the locked tokens so people can verify that this transaction is nothing fishy.

### Price determination

The price for a month is determined using [stellar.expert](https://stellar.expert) data.
A [script](../scrips/info/stellarexpert/tftprice.py) to determine the weighted average price for a month is available so everyone can check.

monthly prices:

|month| USD price |
|-----|-----------|
|o5/2021|0.09940|
