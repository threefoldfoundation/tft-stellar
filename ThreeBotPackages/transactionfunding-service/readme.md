# Conversion Service

Service for converting Threefold tft's to Stellar tft's.
To be used as a Threebot package. See [https://github.com/threefoldtech/jumpscaleX_threebot](https://github.com/threefoldtech/jumpscaleX_threebot).

## Requirements

You need following knowledge to start this server.

A funding wallet with trustlines to the tokens it funds payment transactions for.

With a new funding wallet:

```python
JSX> txfundingwallet = j.clients.stellar.new("txfundingwallet", network="TEST")
JSX> txfundingwallet.add_trustline('TFT','GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3')
JSX> txfundingwallet.add_trustline('FreeTFT','GBLDUINEFYTF7XEE7YNWA3JQS4K2VD37YU7I2YAE7R5AHZDKQXSS2J6R')
```

With an existing funding wallet:

`txfundingwallet_secret`: is the secret key of the funding account which holds the Lumens.

```python
JSX> j.clients.stellar.new("txfundingwallet", network="TEST",secret="<txfundingwallet_secret>")
```

## Running

- execute following:
`kosmos -p 'j.servers.threebot.start()'`

Once this process is completed, create the stellar and tfchain client and add this package to the Threebot.

```python
JSX> gedis = j.clients.gedis.get("pm", port=8901, package_name="zerobot.packagemanager")
JSX> gedis.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/transactionfunding-service",install_kwargs={ "domain": "testnet.threefold.io" })
JSX> p.threefoldfoundation.transactionfunding_service.start()
```

The server will start at `host/threefoldfoundation/transactionfunding_service/`

Test out the transfer tokens:

## Actors

There is one actor with 1 method.

- `fund_transaction`: Funds and signs a TFT transaction.
  - param `transaction`: Stellar transaction envelope in xdr
