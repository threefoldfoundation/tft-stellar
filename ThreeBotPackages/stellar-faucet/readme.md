# Stellar faucet

A faucet for receiving Threefold Stellar tokens (TFT) on the Stellar testnet.
To be used as a Threebot package. See [https://github.com/threefoldtech/jumpscaleX_threebot](https://github.com/threefoldtech/jumpscaleX_threebot).

## Building frontend

- install frontend dependencies: `cd faucet-frontend && npm install`
- build: `npm run build`

## Requirements

You need following knowledge to start this server.

- `secret`: is the secret key of the faucet account which holds the Stellar TFT's.
- `issuer`: is the address (public key) of the Stellar TFT issuer.
- `amount`: is the amount of token you wish to drip with each transfer in this faucet.

## Running

- execute following:
`kosmos -p 'j.servers.threebot.start()'`

Once this process is completed, add this package to the Threebot.

```
JSX> gedis = j.clients.gedis.get("pm", port=8901, package_name="zerobot.packagemanager")
JSX> gedis.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/stellar-faucet", install_kwargs={"secret":"secret", "issuer": "issuer", "amount": "amount"})
JSX> p.threefoldfoundation.stellar_faucet.start()
```
- server will start at `172.17.0.2/threefoldfoundation/stellar_faucet/`

## Actors

See [actors](../actors). We have one actor that has one method:

`transfer`: transfers tokens from our distributor account to an address on the Stellar testnet.