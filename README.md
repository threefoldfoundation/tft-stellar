# tft-stellar

Threefoldtoken on the stellar network

## Testnet

On the stellar testnet it is known as `TFT` and the issuer is `GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3`.

Keep in mind that the stellar testnet is [reset every quarter](https://www.stellar.org/developers/guides/concepts/test-net.html#periodic-reset-of-testnet-data).

## Wallet implementations

- [Jumpscale](https://github.com/threefoldtech/jumpscaleX_libs/tree/development/JumpscaleLibs/clients/stellar)

## tft-stellar tooling on your Threebot

This Threebot package contains following tools:

- `Conversion Service`: Service for converting TFChain TFT's to Stellar TFT's.
- `Stellar Faucet`: Faucet for receiving Testnet Stellar TFT's to any testnet Stellar address.
- `Unlock Service`: Service for storing and retrieving unlock transaction for a Stellar Wallet.


### Building Faucet Frontend

- install frontend dependencies: `cd faucet-frontend && npm install`
- build: `npm run build`

### Requirements

You need following knowledge to start the frontend.

- `secret`: is the secret key of the faucet account which holds the Stellar TFT's.
- `issuer`: is the address (public key) of the Stellar TFT issuer.
- `amount`: is the amount of token you wish to drip with each transfer in this faucet.

## Running this package on your Threebot

- execute following:
`kosmos -p 'j.servers.threebot.start()'`

Once this process is completed, add this package to the Threebot.

```
JSX> gedis = j.clients.gedis.get("pm", port=8901, package_name="zerobot.packagemanager")
JSX> gedis.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar", install_kwargs={"secret":"secret", "issuer": "issuer", "amount": "amount"})

# To use the conversion tool, set following:
JSX> converter = j.clients.stellar.new("converter", network="TEST",secret="<converter_secret>")
JSX> tfchain = j.clients.tfchain.new(name="tfchain", network_type="TEST")

JSX> p.threefoldfoundation.tft_stellar.start()
```
- server will start at `172.17.0.2/threefoldfoundation/tft_stellar/`

## Actors

See [actors](../actors).

### Conversion Service

This actor has two methods:

- `activate_account`: activates a Stellar account with a minimal balance.
- `transfer_tokens`: transfer tokens from a TFChain address to a Stellar address. This includes unlocked and locked tokens. Locked tokens will be held in escrow accounts. This function returns the unlock transactions that come with these escrow accounts.

### Stellar Faucet

This actor has one method:

`transfer`: transfers tokens from our distributor account to an address on the Stellar testnet.

### Unlock Service

This actor has two methods:

- `create_unlockhash_transaction`: creates an stores an unlock transaction by hash. Requires a unlockhash_transaction object.
- `get_unlockhash_transaction`: retrieves an unlockhash_transaction object by hash.
