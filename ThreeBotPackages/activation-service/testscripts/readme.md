# Activate account service testscripts

## Generate an account

`./createAccount.py`

## Submit to the service

```sh
curl -H "Content-Type: application/json" -d '{ "args": { "address": "<newaddress>"  }}' "https://testnet.threefold.io/threefoldfoundation/activation_service/create_activation_code
```
