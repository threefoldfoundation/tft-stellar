# Unlock Service

Service for storing and retrieving unlock transactions for a stellar wallet.
To be used as a Threebot package. See [https://github.com/threefoldtech/jumpscaleX_threebot](https://github.com/threefoldtech/jumpscaleX_threebot).

## Running

- execute following:
`kosmos -p 'j.servers.threebot.start()'`

Once this process is completed, create the stellar and tfchain client and add this package to the Threebot.

testnet:

```python
JSX> j.tools.threebot_packages.zerobot__admin.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/unlock-service", install_kwargs={ "domain": "testnet.threefold.io" })
```

production:

```python
JSX> j.tools.threebot_packages.zerobot__admin.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/unlock-service", install_kwargs={ "domain": "tokenservices.threefold.io" })
```

The server will start at `host/threefoldfoundation/unlock_service/`

Test out the creation of an unlockhash transaction:

`curl -H "Content-Type: application/json" -d '{ "args": { "unlockhash": "", "transaction_xdr": "" }}' -XPOST http://localhost/threefoldfoundation/unlock_service/create_unlockhash_transaction`

## Actor

There is one actor with 2 methods.

- `create_unlockhash_transaction`: creates an unlockhash transaction and stores it in bcdb.
  - param `unlockhash`: unlockhash of transaction
  - param `transaction_xdr`: Stellar transaction in xdr string
- `get_unlockhash_transaction`: get's an unlockhash transaction by hash.
  - param `unlockhash`: unlockhash of transaction to look up
