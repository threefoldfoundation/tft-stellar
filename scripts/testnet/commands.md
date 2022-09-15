# Commands executed for setting up TFT  on Stellar

## Issuing Account

These commands are available through [js-ng shell](https://github.com/threefoldtech/js-sdk).

Create the wallets:

```sh
j.clients.stellar.new('testtftissuerwallet', network='TEST')
j.clients.stellar.new('testfreetftissuerwallet', network='TEST')
j.clients.stellar.new('testtftaissuerwallet', network='TEST')
```

or recreate with the secrets.

Activate and fund the account:

```sh
j.clients.stellar.testtftissuerwallet.activate_through_friendbot()
j.clients.stellar.testfreetftissuerwallet.activate_through_friendbot()
j.clients.stellar.testtftaissuerwallet.activate_through_friendbot()
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
j.clients.stellar.new('testfaucetwallet',network='TEST',secret='')
```

```python
j.clients.stellar.testtxfundingwallet.activate_through_friendbot()
j.clients.stellar.testconverter.activate_through_friendbot()
j.clients.stellar.testactivation_wallet.activate_through_friendbot()
j.clients.stellar.testfaucetwallet.activate_through_friendbot()
j.clients.stellar.testfaucetwallet.add_known_trustline('TFT')
j.clients.stellar.testtxfundingwallet.add_known_trustline('TFT')
j.clients.stellar.testtxfundingwallet.add_known_trustline('TFTA')
j.clients.stellar.testmigration_walle.add_known_trustline('TFT')
j.clients.stellar.testmigration_walle.add_known_trustline('TFTA')
```
