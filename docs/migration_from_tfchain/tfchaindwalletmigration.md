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

Use the `stellaraddressesfromseed` tool from the [releases page](https://github.com/threefoldfoundation/tft-stellar/releases) or from rthe [rivine source](https://github.com/threefoldtech/rivine/blob/master/research/stellar/examples/accounts/stellaraddressesfromseed.go) to generate the addresses, the corresponding stellar addresses and their seeds.

```sh
./stellaraddressesfromseed -secrets=true -amount=<amountfromstep1> my very secret rivine seed from step 2
```
