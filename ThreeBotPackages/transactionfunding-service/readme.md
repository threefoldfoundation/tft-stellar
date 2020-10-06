# Transaction funding Service

A funding service accepts transaction envelopes and funds the required lumen as described in the [documentation](../../docs/transaction_funding.md).

To be used as a JsX Threebot package. See [https://github.com/threefoldtech/jumpscaleX_threebot](https://github.com/threefoldtech/jumpscaleX_threebot).

## Requirements

You need following knowledge to start this server.

A funding wallet with trustlines to the tokens it funds payment transactions for.
It needs trustlines to all tokens it funds transactions for to claim the fee.

With a new funding wallet(Testnet):

```python
JSX> txfundingwallet = j.clients.stellar.new("txfundingwallet", network="TEST")
JSX> txfundingwallet.activate_through_friendbot()
JSX> txfundingwallet.add_trustline('TFT','GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3')
JSX> txfundingwallet.add_trustline('FreeTFT','GBLDUINEFYTF7XEE7YNWA3JQS4K2VD37YU7I2YAE7R5AHZDKQXSS2J6R')
```

for production:

```python
JSX> txfundingwallet = j.clients.stellar.new("txfundingwallet", network="TEST")
```

Activate it from another wallet

Add the trustlines:

```python
JSX> txfundingwallet.add_trustline('TFT','GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47')
JSX> txfundingwallet.add_trustline('FreeTFT','GCBGS5TFE2BPPUVY55ZPEMWWGR6CLQ7T6P46SOFGHXEBJ34MSP6HVEUT')
```

With an existing funding wallet:

`txfundingwallet_secret`: is the secret key of the funding account which holds the Lumens and already has the trustlines.

```python
JSX> j.clients.stellar.new("txfundingwallet", network="TEST",secret="<txfundingwallet_secret>")
```

## Running

- execute following:
`kosmos -p 'j.servers.threebot.start()'`

Once this process is completed, create the stellar and tfchain client and add this package to the Threebot.

install arguments:

- `wallet`: the wallet used to fund the transactions, default: `txfundingwallet`
- `slaves`: the number of wallets to use to distribute the load, default: 30
- `domain`: default: `testnet.threefoldtoken.io`

```python
JSX> j.tools.threebot_packages.zerobot__admin.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/transactionfunding-service",install_kwargs={ "domain": "testnet.threefold.io" })
JSX>  j.tools.threebot_packages.threefoldfoundation__transactionfunding_service.start()
```

The server will start at `host/threefoldfoundation/transactionfunding_service/`

Test out the transfer tokens:

## Actors

There is one actor with 1 method.

- `fund_transaction`: Funds and signs a TFT transaction.
  - param `transaction`: Stellar transaction envelope in xdr

## Load distribution

In Stellar sequence numbers for an account must increase.
If only 1 account would be used, all request must essentially be executed in sequence and transmitted to the Stellar network before the next request to fund a transaction can be done.

Ths package creates extra slave wallets with the name of the basewallet appended with `_index`. It loops over the slaves to search for one where the last sequence is already accepted by the network and if not found, takes the slave that was least recently used, given that it was longer than a minute ago.

### Slave cleanup

```python
walletnames=j.clients.stellar._children_names_get()
slaves=[w for w in walletnames if 'txfundingwallet_' in w]
for slavename in slaves:
    j.clients.stellar.delete(slavename)
```
