# Stellar faucet

A faucet for receiving tokens from a specified asset and issuer.
To be used as a JsX Threebot package. See [https://github.com/threefoldtech/jumpscaleX_threebot](https://github.com/threefoldtech/jumpscaleX_threebot).

For developing on this package, see the [Development documentation](./development.md).

## Requirements

For production:

A new wallet for the faucet

```python
faucetwallet = j.clients.stellar.new('faucetwallet')
```

Restore an existing wallet:

```python
j.clients.stellar.new('faucetwallet',secret='<secret>')
```

Add the trustlines:

```python
JSX> faucetwallet.add_trustline('FreeTFT','GCBGS5TFE2BPPUVY55ZPEMWWGR6CLQ7T6P46SOFGHXEBJ34MSP6HVEUT')
```

For testnet:

Add the trustlines:

```python
JSX> faucetwallet.add_trustline('FreeTFT','GBLDUINEFYTF7XEE7YNWA3JQS4K2VD37YU7I2YAE7R5AHZDKQXSS2J6R')
```

## Running

- execute following:
`kosmos -p 'j.servers.threebot.start()'`

Once this process is completed, add this package to the Threebot.

install arguments:

- `wallet`:the wallet to use to transfer from, default: faucetwallet
- `asset`: default: TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3 .
- `amount`: is the amount of token you wish to drip with each transfer in this faucet, default: 1000.
- `domain`: default: "testnet.threefoldtoken.io"

```python
JSX> j.tools.threebot_packages.zerobot__admin.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/stellar_faucet", install_kwargs={"domain": "testnet.threefold.io"})
```

for a freetft faucet:

testnet:

```python
j.tools.threebot_packages.zerobot__admin.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/stellar_faucet", install_kwargs={"domain": "getfreetft.testnet.threefold.io", "asset":"FreeTFT:GBLDUINEFYTF7XEE7YNWA3JQS4K2VD37YU7I2YAE7R5AHZDKQXSS2J6R"})
```

production:

```python
j.tools.threebot_packages.zerobot__admin.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/stellar_faucet", install_kwargs={"domain": "getfreetft.threefold.io", "asset":"FreeTFT:GCBGS5TFE2BPPUVY55ZPEMWWGR6CLQ7T6P46SOFGHXEBJ34MSP6HVEUT"})
```

- server will start at `host/threefoldfoundation/stellar_faucet/`

### Running on a different path than `/`

If the app needs to be deployed on another path than `/` it must only be configured in 1 place.

[vue.config.js](./faucet_frontend/vue.config.js#L6)

afterwards run`npm run build`

## Actors

See [actors](../actors). We have one actor that has one method:

`transfer`: transfers tokens from our distributor account to an address on the Stellar testnet.
