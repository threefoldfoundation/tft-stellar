# Stellar faucet

A faucet for receiving tokens from a specified asset and issuer.
To be used as a Threebot package. See [https://github.com/threefoldtech/jumpscaleX_threebot](https://github.com/threefoldtech/jumpscaleX_threebot).

## Building frontend

- install frontend dependencies: `cd faucet-frontend && npm install`
- build: `npm run build`

## Requirements

Required install kwargs!!

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
JSX> gedis.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/stellar-faucet", install_kwargs={"domain": "testnet.threefold.io"})
JSX> p.threefoldfoundation.stellar_faucet.start()
```

- server will start at `172.17.0.2/threefoldfoundation/stellar_faucet/`

## Actors

See [actors](../actors). We have one actor that has one method:

`transfer`: transfers tokens from our distributor account to an address on the Stellar testnet.