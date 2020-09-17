# Activation Service

Service for new accounts activation. To be used as a jumpscale package.

## Requirements

You need following knowledge to start this server.

- `activation_secret`: is the secret key of the activation  account which holds the Stellar XLM to fund the accounts.

## Running

Make sure the wallet exists:
`j.clients.stellar.new("activation_wallet", network="TEST",secret="<activation_secret>")`

execute the following command in jsng shell:
`j.servers.threebot.start_default()`

Once this process is completed, add this package from admin dashboard
or from jsng shell like this:

```python
JS-NG> j.servers.threebot.default.packages.add(<package_path>)
```

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
