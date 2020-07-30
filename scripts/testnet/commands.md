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

activate issuer accounts again, publish home domains

service accounts:

```python
j.clients.stellar.new('txfundingwallet',network='TEST',secret='')
j.clients.stellar.new('converter',network='TEST',secret='')
j.clients.stellar.new('activation_wallet',network='TEST',secret='')
j.clients.stellar.new('faucetwallet',network='TEST',secret='')
```

```python
j.clients.stellar.txfundingwallet.activate_through_friendbot()
j.clients.stellar.converter.activate_through_friendbot()
j.clients.stellar.activation_wallet.activate_through_friendbot()
j.clients.stellar.faucetwallet.activate_through_friendbot()
j.clients.stellar.faucetwallet.add_known_trustline('FreeTFT')
j.clients.stellar.txfundingwallet.add_known_trustline('TFT')
j.clients.stellar.txfundingwallet.add_known_trustline('FreeTFT')
j.clients.stellar.txfundingwallet.add_known_trustline('TFTA')
j.clients.stellar.converter.add_known_trustline('TFT')
j.clients.stellar.converter.add_known_trustline('TFTA')
```

Trader accounts:

```python
j.clients.stellar.new('tfttraderwallet',network='TEST',secret='')
j.clients.stellar.new('freetfttraderwallet',network='TEST',secret='')
j.clients.stellar.tfttraderwallet.activate_through_friendbot()
j.clients.stellar.freetfttraderwallet.activate_through_friendbot()
j.clients.stellar.tfttraderwallet.add_known_trustline('TFT')
j.clients.stellar.freetfttraderwallet.add_known_trustline('FreeTFT')
j.clients.stellar.tftissuerwallet.transfer(j.clients.stellar.tfttraderwallet.address, amount="500000",asset='TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3',fund_transaction=False)
j.clients.stellar.freeetftissuerwallet.transfer(j.clients.stellar.freetfttraderwallet.address,amount="500000",asset='FreeTFT:GBLDUINEFYTF7XEE7YNWA3JQS4K2VD37YU7I2YAE7R5AHZDKQXSS2J6R', fund_transaction=False)
```
