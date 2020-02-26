# Conversion Service

Service for converting Threefold tft's to Stellar tft's.
To be used as a Threebot package. See [https://github.com/threefoldtech/jumpscaleX_threebot](https://github.com/threefoldtech/jumpscaleX_threebot).

## Requirements

You need following knowledge to start this server.

- `txfundingwallet_secret`: is the secret key of the converter account which holds the Stellar TFT's.

## Running

- execute following:
`kosmos -p 'j.servers.threebot.start()'`

Once this process is completed, create the stellar and tfchain client and add this package to the Threebot.

```python
JSX> converter = j.clients.stellar.new("txfundingwallet", network="TEST",secret="<txfundingwallet_secret>")


JSX> gedis = j.clients.gedis.get("pm", port=8901, package_name="zerobot.packagemanager")
JSX> gedis.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/transactionfunding-service")
JSX> p.threefoldfoundation.transactionfunding_service.start()
```

The server will start at `host/threefoldfoundation/_service/`

Test out the transfer tokens:

## Actors

There is one actor with 1 method.

- `fund_transaction`: Funds and signs a TFT transaction.
  - param `transaction`: Stellar transaction envelope in xdr
