# Vesting options

People lock (vest), an amount of TFT for a specific time-period. If the price of TFT goes above some predefined limits, 25%, ( or another number) is already released.

The vesting is done over a period of 48 months. Every month 1/48th of the amount is released

Since there are no smart contracts in Stellar,  we need to be a bit creative on how we implement this.

## Nice to have

Make it possible to transfer vested funds to another account. The vesting rules stay the same, only the owner changes.

## unlocking by price

Releasing a vested block if a certain price condition is reached can be achieved by adding a multisig 
signer to the vesting escrow account ( on which the price condition is set as extra data). the multisig signer is the oracle for the TFT price which needs to be validated and signed by multiple oracle validators.

To check: can the preauthsigner transaction hash be added before it is already signed, in this case, no price condition must be set on the escrow account as extra data.

## Possible solutions

### Break up the amount in several escrow accounts

Every amount that has seperate rules is be placed on a seperate escrow account so the vested amount is split up in blocks. This means 48 escrow accounts each with a prepublished timebased unlocktransaction and an unsigned unlocktransaction for the oracle price The Oracle signers need to added to the escrow account.

Transferring funds:

Transferring vested blocks to someone else can be implemented by having another address as the beneficiary and the signers for this address can be modified by the one holding control of this account. This does mean that transferring a vested block partially is not possible and that beneficiary account needs to be created for every block that should be transferrable.

Cons:

- A lot of escrow accounts have to be created with  a minimum balance of 1+1.5(benificiary+ 2 unlocktransactions)+4.5(for the 9 oracle signers) =6, so 288 XLM per vesting user(= 125.28 USD at the time of writing).
- A bit complex

### Use 1 escrow account with chained unlocktransactions

The major benefit is that this costs less XLM

We can chain the timebased unlocktransactions that transfer that months payout  and modifies the signing rules to the next unlocktransactions The Oracle would still need to cosign for releasing earlier. The transaction would also need to set the signing condition orrectly to the next unlocktransactions.

Transferring funds:

Transferring vested funds to someone else can be implemented by having another address as the beneficiary and the signers for this address can be modified by the one holding control of this account. This does mean that transferring vested funds partially is not possible.

Cons:

- Very complex and very inflexible

### Use 1 escrow account per vesting user with normal multisig

Set up an escrow account with the beneficiasry ( or any account chosen) having a signing weight of 5 and 9 oracle signers with a weight of 1. The weight required to transfer funds or change the signers is set to 10.

An extra data entry is set to the escrow account with the vesting scheme ( the formula).

The Beneficiary asks the oracle to cosign for every transaction. The cosigners can validate if the transaction is valid and cosign if it is. The beneficiary always has to sign since the oracle alone never hasd enouygh signing weight

Cons:

- The funds can not be freed if the oracle stops cosigning ( maybe we can put 1 timebased releas-eall prepublished transaction signer in there to free the funds at the end of the vesting period)

Pros:

- Simple
- Very flexible
  - A wallet can show the vested funds as 1 seperate account with a free and locked balance, one can transfer to anyone from the vested account
  - transferring vested funds can be implemented later as well if the vesting scheme matches for example
- Since the vesting formula is set on the account, It is visible by everyone and no external data has to be kept

At first it seems bit weird since it is not set in stone but in essence it is the same as the previous complex solutions since with the oracle doing cosigning, the funds can be released anyway.

The oracle code for the cosigning will be published to github so everyone can check the code and since all the data resides on-chain, everyone can validate that no rules have been violated.

## Conclusion

Use 1 escrow account per vesting user with normal multisig.
