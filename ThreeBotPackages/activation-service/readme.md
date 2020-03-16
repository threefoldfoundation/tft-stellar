# Activation Service

Service for new accounts activation as described [in the specs](../specs/address_activation.md).
To be used as a Threebot package. See [jumpscaleX_threebot](https://github.com/threefoldtech/jumpscaleX_threebot).


## Requirements

You need following knowledge to start this server.

- `activation_secret`: is the secret key of the activation  account which holds the Stellar XLM to fund the accounts.

## Running

- execute following:
`kosmos -p 'j.servers.threebot.start()'`

Once this process is completed, create the stellar and add this package to the Threebot.

```python
JSX> gedis = j.clients.gedis.get("pm", port=8901, package_name="zerobot.packagemanager")
JSX> gedis.actors.package_manager.package_add(git_url="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/activation-service", install_kwargs={ "domain": "testnet.threefold.io" })
JSX> p.threefoldfoundation.unlock_service.start()
```

The server will start at `172.17.0.2/threefoldfoundation/unlock_service/`

## Actor

There is one actor with 2 methods.

- `create_activation_code`: Creates an activation code for an address
  - param `address`: Stellar address to create an activation code foractivate
  - returns an activation code, the stellar address and possible phonenumbers to send the he activation code to via SMS.
  