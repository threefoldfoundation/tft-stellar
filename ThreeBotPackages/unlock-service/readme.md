# Unlock Service

Service for storing and retrieving unlock transactions for a stellar wallet.
To be used as a Threebot package. See [https://github.com/threefoldtech/jumpscaleX_threebot](https://github.com/threefoldtech/jumpscaleX_threebot).

## Running

- execute following:
`kosmos -p 'j.servers.threebot.start()'`

Once this process is completed, create the stellar and tfchain client and add this package to the Threebot.

```python
JSX> converter = j.clients.stellar.new("converter", network="TEST",secret="<converter_secret>")

JSX> tfchain = j.clients.tfchain.new(name="tfchain", network_type="TEST")

JSX> gedis = j.clients.gedis.get("pm", port=8901, package_name="zerobot.packagemanager")
JSX> gedis.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/unlock-service")
JSX> p.threefoldfoundation.unlock_service.start()
```

The server will start at `172.17.0.2/threefoldfoundation/unlock_service/`

Test out listing the unlockhash transactions:

`curl http://localhost/threefoldfoundation/unlock_service/list`

## Troubleshooting

If a 404 is returned, restart Lapis server.

## Actor

There is one actor with 2 methods.

- `create_unlockhash_transaction`: creates an unlockhash transaction and stores it in bcdb.
- `get_unlockhash_transaction`: get's an unlockhash transaction by hash.
- `list`: lists all unlockhash transactions

## Notes

A TFChain address balance has a precision of 9, a Stellar one has a precision of 7. We fetch the balance of unlocked/locked tokens from a TFChain address and set the precision to 7 to be compatible with Stellar.

## TODO

- Make conversion process for locked tokens faster, right now it executes locked token transfer sequentially. This is because the stellar account requires sequential increments when executing transactions.
When this process is executed asynchronously the incrementions are scrambled and the stellar network does not aprove on these transactions.