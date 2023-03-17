# Releasing vested TFT

We are abandoning the vesting scheme and returning all vested TFT's back to the owners.

Let's just prepare the unvest transactions, have them signed by the cosigners and make them available. The owner then has to sign it too and submit it to the Stellar network.

## Options for the release transactions

1. Just give control to the owner

    Simple, easy to verify by the owner and the guardians.

    The owner than has to clean up the escrow account by transferring the TFT's, remove the TFT trustline, remove the data entry and merge the account into it's own.

2. Just send the TFT's to the owner

    Simple, easy to verify by the owner and the guardians.

    Leaves escrow accounts which can not be cleaned up and will stay as multisig accounts for the owners.

3. Do it all

    Send the TFT's to the owner, remove the TFT trustline, remove the data entry and merge the account to the owner account.

    Cleanest thing to do, harder to verify.

    Gives the owners 7.6 XLM instead of recovering them (=2538 XLM).

    Have to check if the escrow accounts have enough XLM to perform all these operations

Option 3 is taken as it is the cleanest and most user friendly.

The script generates a file `unvesting_transactions.txt` containing 1 transaction envelope per line.

## Guardians signing program

### Requirements

As the guardians have different operating systems and not everyone has deep tecgnival knowledge, it should be a program that can run inor built for different operating systems and architectures and be very easy to run without much installation requirements

### Programming language

Go

### input/output

The program reads the transactions to sign from the file `unvesting_transactions.txt` and writes the signed transactions to the file `signed_unvesting_transactions_<signer_address>.txt`, 1 transaction envelope per line.

The program takes exactly 1 argument: the signing secret.

## Combinng the guardian signatures

To facilitate and speed up the signing process, all guardians can sign in parallel.
The resulting signatures need to be collected from the ouput files and put in a transaction envelope with the transaction. Exactly 5 signatures should be placed in 1 transaction envelope as the weight of each signer is 1, the weight of the owner is 5 and Stellar does not allow too many signatures.

## Publish the partially signed unvesting transactions

The [vesting service](../../ThreeBotPackages/vesting_service/) needs to get an extra endpoint `unvestingtransaction` that takes the owner as an argument and returns the unvesting traansaction envelope containg the guardian signatures.
