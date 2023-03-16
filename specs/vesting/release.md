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
