# Unlock Service

Service for storing and retrieving unlock transactions for a stellar wallet.
To be used as a Threebot package. See [https://github.com/threefoldtech/jumpscaleX_threebot](https://github.com/threefoldtech/jumpscaleX_threebot).

## Running

- execute following:
`kosmos -p 'j.servers.threebot.start()'`

Once this process is completed, create the stellar and tfchain client and add this package to the Threebot.

```python
JSX> gedis = j.clients.gedis.get("pm", port=8901, package_name="zerobot.packagemanager")
JSX> gedis.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/unlock-service")
JSX> p.threefoldfoundation.unlock_service.start()
```

The server will start at `172.17.0.2/threefoldfoundation/unlock_service/`

Test out the creation of an unlockhash transaction:

`curl -H "Content-Type: application/json" -d '{ "args": { "unlockhash": "", "transaction_xdr": "" }}' -XPOST http://localhost/threefoldfoundation/unlock_service/create_unlockhash_transaction`

## Actor

There is one actor with 2 methods.

- `create_unlockhash_transaction`: creates an unlockhash transaction and stores it in bcdb.
  - param `unlockhash`: unlockhash of transaction
  - param `transaction_xdr`: Stellar transaction in xdr string
- `get_unlockhash_transaction`: get's an unlockhash transaction by hash.
  - param `unlockhash`: unlockhash of transaction to look up
