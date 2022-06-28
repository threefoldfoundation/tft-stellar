# Conversion Service

Js-ng Service for converting Threefold tft's to Stellar tft's. To be used as a Threebot package.

## Requirements

You need following knowledge to start this server.

- `converter_secret`: is the secret key of the converter account which is a cosigner of the TFT issuer account with enough weight to satisfy the medium treshold.

## Running

Make sure the wallet exists and is saved:

```python
j.clients.stellar.new("converter_wallet", network="TEST",secret="<converter_secret>")
j.clients.stellar.converter_wallet.save()
```

execute the following command in jsng shell:
`j.servers.threebot.start_default()`

Make sure that the converter account can issue TFT tokens:

```python
tftissuerwallet.modify_signing_requirements((j.clients.stellar.converter_wallet.address,),5,0,5,7)
```

Install the package.
Once this process is completed add the package to the threebot server from jsng shell like this:

```python
j.servers.threebot.default.packages.add(giturl="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/tfchainmigration_service")
```

The server will start at `host/threefoldfoundation/tfchainmigration_service/`

The following kwargs can also be given to configure the package:

- *wallet* : Name of new/exisiting stellar wallet client instance
- *secret* : Activation secret of wallet to import
- *network*: "STD" or "TEST" to indicate the type of the stellar network
- *domain* : domain configured to access the service

Example with kwargs:
`j.servers.threebot.default.packages.add(package_path,wallet="WALLET_NAME",domain="domain.test.1")`

Test out the transfer tokens:

`curl -H "Content-Type: application/json" -d '{ "tfchain_address": "", "stellar_address": "" }' -XPOST http://localhost/tfchainmigration_service/actors/tfchainmigration_service/migrate_tokens`

## Production deployment

In production it is deployed at `https://tokenservices.threefold.io/threefoldfoundation/conversion_service/<actor_method>`

## Actor

There is one actor with 2 methods.

- `activate_account`: activates a Stellar account with a minimal balance.
  - param `address`: Stellar address to activate
  - param `tfchain_address`: Source Tfchain address
- `migrate_tokens`: migrate tokens from a TFChain address to a Stellar address. This includes unlocked and locked tokens. Locked tokens will be held in escrow accounts. This function returns the unlock transactions that come with these escrow accounts.
  - param `tfchain_address`: Source Tfchain address
  - param `stellar_address`: Stellar address to migrate the TFT's to

## Notes

A TFChain address balance has a precision of 9, a Stellar one has a precision of 7. We fetch the balance of unlocked/locked tokens from a TFChain address and set the precision to 7 to be compatible with Stellar.

## TODO

- Cache the transaction listing of the TFT issuer account, the more TFT issuances are done, the longer this is starting to take.
- Make conversion process for locked tokens faster, right now it executes locked token transfer sequentially. This is because the stellar account requires sequential increments when executing transactions.
When this process is executed asynchronously the incrementions are scrambled and the stellar network does not aprove on these transactions.
