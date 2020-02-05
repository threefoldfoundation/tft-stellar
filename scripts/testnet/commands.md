# Commands executed for setting up TFT  on Stellar

## Issuing Account

These commands are available through [Jumpscale](https://github.com/threefoldtech/jumpscaleX_core).

Create a wallet:

```sh
j.clients.stellar.new('issuerwallet', network='TEST')
```

Activate and fund the account:

```sh
j.clients.stellar.issuerwallet.activate_through_friendbot()
```

## Publish Token home domain

See the [readme](../readme.md) on how to run these scripts.

```sh
../publishdomain.py --network=test TFT www3.threefold.io --issuer_secret=<Issuer secret>
```
