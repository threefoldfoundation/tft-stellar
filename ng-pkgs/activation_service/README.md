# Activation Service

Service for new accounts activation. To be used as a jumpscale package.

## Requirements

You need following knowledge to start this server.

- `activation_secret`: is the secret key of the activation  account which holds the Stellar XLM to fund the accounts.

## Running

Make sure the wallet exists and is saved:

```python
j.clients.stellar.new("activation_wallet", network="TEST",secret="<activation_secret>")
j.clients.stellar.activation_wallet.save()
```

clone this repository:

```python
j.tools.git.ensure_repo("https://github.com/threefoldfoundation/tft-stellar.git")
```

execute the following command in jsng shell:
`j.servers.threebot.start_default()`

Once this process is completed add the package to the threebot server from jsng shell like this:

```python
from pathlib import Path
package_path=str(Path.joinpath(Path.home(),"sandbox","code","github","threefoldfoundation","tft-stellar","ng-pkgs","activation_service"))
j.servers.threebot.default.packages.add(package_path)
```

The following kwargs can also be given to configure the package:

- *wallet* : Name of new/exisiting stellar wallet client instance
- *secret* : Activation secret of wallet to import
- *network*: "STD" or "TEST" to indicate the type of the stellar network
- *domain* : domain configured to access the service

Example with kwargs:
`j.servers.threebot.default.packages.add(package_path,wallet="WALLET_NAME",domain="domain.test.1")`

## Actor

There is one actor with 2 methods.

- `create_activation_code`: Activates an address
  - param `address`: Stellar address to create an activation code for
  - returns an activation code, the stellar address and possible phonenumbers to send the he activation code to via SMS.

```sh
 curl -k --header "Content-Type: application/json" --request POST --data '{"address":"<address>"}' https://<host>/activation_service/create_activation_code
 ```

- `activate_account`: does nothing, here for backwards compatibility
  - param `activation_code`: activation code created by the `create_activation_code` method

```sh
curl -k --header "Content-Type: application/json" --request POST --data '{"activation_code":"<activation_code>"}' https://<host>/activation_service/activate_account
```
