# Unlock Service

js-ng service for storing and retrieving unlock transactions for a stellar wallet.
To be used as a Threebot package.

## Running

clone this repository:

```python
j.tools.git.ensure_repo("https://github.com/threefoldfoundation/tft-stellar.git")
```

execute the following command in jsng shell:
`j.servers.threebot.start_default()`

Install the package.
Once this process is completed add the package to the threebot server from jsng shell like this:

```python
from pathlib import Path
package_path=str(Path.joinpath(Path.home(),"sandbox","code","github","threefoldfoundation","tft-stellar","ThreeBotPackages","unlock_service"))
j.servers.threebot.default.packages.add(package_path)
```

The server will start and the actor methods will be available at `<HOST>/unlock_service/actors/unlock_service/<ACTOR_METHOD>`

The following kwargs can also be given to configure the package:

- *domain* : domain configured to access the service

Example with kwargs:
`j.servers.threebot.default.packages.add(package_path,domain="domain.test.1")`


Test out the creation of an unlockhash transaction:

`curl -H "Content-Type: application/json" -d '{ "unlockhash": "", "transaction_xdr": "" }' -XPOST https://localhost/unlock_service/actors/unlock_service/create_unlockhash_transaction -k`

## Actor

There is one actor with 2 methods.

- `create_unlockhash_transaction`: creates an unlockhash transaction and stores it .
  - param `unlockhash`: unlockhash of transaction
  - param `transaction_xdr`: Stellar transaction in xdr string
- `get_unlockhash_transaction`: get's an unlockhash transaction by hash.
  - param `unlockhash`: unlockhash of transaction to look up
