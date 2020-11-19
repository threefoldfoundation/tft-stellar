# Activate account service testscripts

## Generate an account

`./createAccount.py`

## Submit to the service

```sh
curl --insecure -H "Content-Type: application/json" -d '{ "args": { "address": "<newaddress>"  }}' "https://localhost:443/threefoldfoundation/activation_service/create_activation_code"
```
