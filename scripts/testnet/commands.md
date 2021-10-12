# Commands executed for setting up TFT  on Stellar

## Issuing Account

These commands are available through [js-ng shell](https://github.com/threefoldtech/js-sdk).

Create the wallets:

```sh
j.clients.stellar.new('testtftissuer', network='TEST')
j.clients.stellar.new('testfreetftissuer', network='TEST')
j.clients.stellar.new('testtftaissuer', network='TEST')
```

or recreate with the secrets.

Activate and fund the account:

```sh
j.clients.stellar.testtftissuer.activate_through_friendbot()
j.clients.stellar.testfreetftissuer.activate_through_friendbot()
j.clients.stellar.testtftaissuer.activate_through_friendbot()
```

## Publish Token home domain

See the [readme](../readme.md) on how to run these scripts.

```sh
../publishdomain.py --network=test TFT www2.threefold.io --issuer_secret=<Issuer secret>
../publishdomain.py --network=test TFTA www2.threefold.io --issuer_secret=<Issuer secret>
../publishdomain.py --network=test FreeTFT www2.threefold.io --issuer_secret=<Issuer secret>
```

## after network reset

activate issuer accounts again, publish home domains

service accounts:

```python
j.clients.stellar.new('testtxfundingwallet',network='TEST',secret='')
j.clients.stellar.new('testmigration_wallet',network='TEST',secret='')
j.clients.stellar.new('testactivation_wallet',network='TEST',secret='')
j.clients.stellar.new('testvesting_wallet',network='TEST',secret='')
j.clients.stellar.new('testBTCissuer',network='TEST',secret='')
```

```python
j.clients.stellar.testtxfundingwallet.activate_through_friendbot()
j.clients.stellar.testmigration_wallet.activate_through_friendbot()
j.clients.stellar.testactivation_wallet.activate_through_friendbot()
j.clients.stellar.testvesting_wallet.activate_through_friendbot()
j.clients.stellar.testBTCissuer.activate_through_friendbot()
```

Restart the transaction funding service to recreate the slave wallets.
