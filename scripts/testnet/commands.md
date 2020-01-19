# Commands executed for setting up TFT  on Stellar

## Issuing Account

These python scripts are available in the [Stellar examples of Rivine](https://github.com/threefoldtech/rivine/tree/master/research/stellar/examples/python)

Create a keypair:

```sh
python account/create-keypair.py
```

Activate and fund the account:

```sh
python account/fund-account.py --address GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3
```

## Publish Token home domain

```sh
../publishdomain.py --network=test TFT www2.threefold.io --issuer_secret=<Issuer secret>
```
