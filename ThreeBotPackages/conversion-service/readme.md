# Conversion Service

JsX Service for converting Threefold tft's to Stellar tft's. To be used as a Threebot package. See [https://github.com/threefoldtech/jumpscaleX_threebot](https://github.com/threefoldtech/jumpscaleX_threebot).

## Requirements

You need following knowledge to start this server.

- `converter_secret`: is the secret key of the converter account which holds the Stellar TFT's.

## Running

- execute following:
`kosmos -p 'j.servers.threebot.start()'`

Once this process is completed, create the stellar and tfchain client and add this package to the Threebot.

Inialize the wallet clients:

testnet:

```python
JSX> j.clients.stellar.new("converter", network="TEST",secret="<converter_secret>")
JSX> j.clients.tfchain.new(name="tfchain", network_type="TEST")
```

production:

```python
JSX> j.clients.stellar.new("converter",secret="<converter_secret>")
JSX> j.clients.tfchain.new(name="tfchain")
```

Make sure that for both TFT and TFTA, the converter account can issue tokens:

```python
tftissuerwallet.modify_signing_requirements((j.clients.stellar.converter.address,),1,0,3,3)
tftaissuerwallet.modify_signing_requirements((j.clients.stellar.converter.address,),1,0,3,3)
```

Install the package.

testnet:

```python
JSX> j.tools.threebot_packages.zerobot__admin.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/conversion-service", install_kwargs={ "domain": "testnet.threefold.io" })
```

production:

```python
JSX> j.tools.threebot_packages.zerobot__admin.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/conversion-service", install_kwargs={ "domain": "tokenservices.threefold.io" })
```

The server will start at `host/threefoldfoundation/conversion_service/`

Test out the transfer tokens:

`curl -H "Content-Type: application/json" -d '{ "args": { "tfchain_address": "", "stellar_address": "" }}' -XPOST http://localhost/threefoldfoundation/conversion_service/migrate_tokens`

## Troubleshooting

If a 404 is returned, restart Lapis server.

## Actor

There is one actor with 2 methods.

- `activate_account`: activates a Stellar account with a minimal balance.
  - param `address`: Stellar address to activate
  - param `tfchain_address`: Source Tfchain address
- `migrate_tokens`: migrate tokens from a TFChain address to a Stellar address. This includes unlocked and locked tokens. Locked tokens will be held in escrow accounts. This function returns the unlock transactions that come with these escrow accounts.
  - param `tfchain_address`: Source Tfchain address
  - param `stellar_address`: Stellar address to transfer funds to

## Notes

A TFChain address balance has a precision of 9, a Stellar one has a precision of 7. We fetch the balance of unlocked/locked tokens from a TFChain address and set the precision to 7 to be compatible with Stellar.

## TODO

- Make conversion process for locked tokens faster, right now it executes locked token transfer sequentially. This is because the stellar account requires sequential increments when executing transactions.
When this process is executed asynchronously the incrementions are scrambled and the stellar network does not aprove on these transactions.
