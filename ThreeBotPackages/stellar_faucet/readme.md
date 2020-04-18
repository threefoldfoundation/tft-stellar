# Stellar faucet

A faucet for receiving tokens from a specified asset and issuer.
To be used as a Threebot package. See [https://github.com/threefoldtech/jumpscaleX_threebot](https://github.com/threefoldtech/jumpscaleX_threebot).

For developing on this package, see the [Development documentation](./development.md).

## Requirements

A wallet for the faucet

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
JSX> gedis = j.clients.gedis.get("pm", port=8901, package_name="zerobot.packagemanager")
JSX> j.threebot.packages.zerobot.admin.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/stellar_faucet", install_kwargs={"domain": "testnet.threefold.io"})
JSX> j.threebot.packages.threefoldfoundation.stellar_faucet.start()
```

for a freetft faucet:
```python
gedis.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/stellar_faucet", install_kwargs={"domain": "testnet.threefold.io", "asset":"FreeTFT:GBLDUINEFYTF7XEE7YNWA3JQS4K2VD37YU7I2YAE7R5AHZDKQXSS2J6R"})
```

- server will start at `172.17.0.2/threefoldfoundation/stellar_faucet/`

### Running on a different path than `/`

If the app needs to be deployed on another path than `/` it must only be configured in 1 place.

https://github.com/threefoldfoundation/tft-stellar/blob/5ded498d881550974e9b3f1c916ff93b484a3392/ThreeBotPackages/stellar_faucet/faucet_frontend/vue.config.js#L6

afterwards run`npm run build`

## Actors

See [actors](../actors). We have one actor that has one method:

`transfer`: transfers tokens from our distributor account to an address on the Stellar testnet.
