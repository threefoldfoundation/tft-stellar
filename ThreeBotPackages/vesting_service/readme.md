# Vesting Service

## Threefoldfoundation deployed urls

### Testnet

url: `https://testnet.threefold.io/threefoldfoundation/vesting_service/create_vesting_account`

example using curl:

```sh
curl  -H "Content-Type: application/json" -d '{ "owner_address": "GBB375L64ZDTW2APJMCOCPJROKTR43PA63J4PKK6Q6OD5LTP4ATCI7OJ"}' "https://testnet.threefold.io/threefoldfoundation/vesting_service/create_vesting_account"

{"address": "GDKMZFELJER5RNQB6T2Z2JO4ZLH6PN5RHH4ZO6AW4LVPBZCFY2PIRENL"}
```

### Production

url: `https://tokenservices.threefold.io/threefoldfoundation/vesting_service/create_vesting_account`

Not available yet