# Commands executed for setting up TFT  on Stellar

## Issuing Account

These commands are available through [Jumpscale](https://github.com/threefoldtech/jumpscaleX_core).

Create the wallets:

```sh
j.clients.stellar.new('tftissuerwallet', network='TEST')
j.clients.stellar.new('freetftissuerwallet', network='TEST')
j.clients.stellar.new('tftaissuerwallet', network='TEST')
```

or recreate with the secrets.

Activate and fund the account:

```sh
j.clients.stellar.tftissuerwallet.activate_through_friendbot()
j.clients.stellar.tftissuerwallet.activate_through_friendbot()
j.clients.stellar.tftaissuerwallet.activate_through_friendbot()
```

## Publish Token home domain

See the [readme](../readme.md) on how to run these scripts.

```sh
../publishdomain.py --network=test TFT www2.threefold.io --issuer_secret=<Issuer secret>
../publishdomain.py --network=test TFTA www2.threefold.io --issuer_secret=<Issuer secret>
../publishdomain.py --network=test FreeTFT www2.threefold.io --issuer_secret=<Issuer secret>
```


## after network reset

activate accounts again, publish home domains