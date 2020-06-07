# Migrating a tfchaind wallet

## Check the amount of addresses in your wallet

After unlocking the wallet:

```sh
tfchainc wallet addresses | wc -l
```

## Get the seed from the wallet

```sh
tfchainc wallet seeds
```

## Generate addresses and secrtets from the seed

Use the `stellaraddressesfromseed` tool from the [releases page](https://github.com/threefoldfoundation/tft-stellar/releases) or from the [rivine source](https://github.com/threefoldtech/rivine/blob/master/research/stellar/examples/accounts/stellaraddressesfromseed.go) to generate the addresses, the corresponding stellar addresses and their seeds.

```sh
./stellaraddressesfromseed -secrets=true -amount=<amountfromstep1> my very secret rivine seed from step 2
```

## Check the adresses that need to be converted

```sh
tfchainc wallet addresses > tft_adresses.txt
```

Run the [tfchainaddressses.py](../../scripts/conversion/tfchainaddresses.py) script.
This will list the adresses that need to be converted together with the amounts they hold.

Filter the output from the `stellaraddressesfromseed` tool  based on this information and curl the [ThreeBotPackages/conversion-service](../../ThreeBotPackages/conversion-service) endpoints for the needed addresses.

