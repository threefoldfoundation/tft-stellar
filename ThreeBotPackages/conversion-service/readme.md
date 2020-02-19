# Conversion Service

Service for converting Threefold tft's to Stellar tft's.
To be used as a Threebot package. See [https://github.com/threefoldtech/jumpscaleX_threebot](https://github.com/threefoldtech/jumpscaleX_threebot).

## Requirements

You need following knowledge to start this server.

- `converter_secret`: is the secret key of the converter account which holds the Stellar TFT's.

## Running

- execute following:
`kosmos -p 'j.servers.threebot.start()'`

Once this process is completed, create the stellar and tfchain client and add this package to the Threebot.

```python
JSX> converter = j.clients.stellar.new("converter", network="TEST",secret="<converter_secret>")

JSX> tfchain = j.clients.tfchain.new(name="tfchain", network_type="TEST")

JSX> gedis = j.clients.gedis.get("pm", port=8901, package_name="zerobot.packagemanager")
JSX> gedis.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/ThreeBotPackages/conversion-service")
JSX> p.threefoldfoundation.conversion_service.start()
```

The server will start at `172.17.0.2/threefoldfoundation/conversion_service/`

Test out the transfer tokens:

`curl -H "Content-Type: application/json" -d '{ "args": { "tfchain_address": "", "stellar_address": "", "asset_code": "", "issuer": "" }}' -XPOST http://localhost/threefoldfoundation/conversion_service/actors/conversion_service/transfer_tokens`

## Actor

There is one actor with 2 methods.

- `activate_account`: activates a Stellar account with a minimal balance.
- `transfer_tokens`: transfer tokens from a TFChain address to a Stellar address. This includes unlocked and locked tokens. Locked tokens will be held in escrow accounts. This function returns the unlock transactions that come with these escrow accounts.

## Notes

A TFChain address balance has a precision of 9, a Stellar one has a precision of 7. We fetch the balance of unlocked/locked tokens from a TFChain address and set the precision to 7 to be compatible with Stellar.

## TODO

- Make conversion process for locked tokens faster, right now it executes locked token transfer sequentially. This is because the stellar account requires sequential increments when executing transactions.
When this process is executed asynchronously the incrementions are scrambled and the stellar network does not aprove on these transactions.