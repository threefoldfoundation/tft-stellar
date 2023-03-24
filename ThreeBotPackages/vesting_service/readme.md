# Vesting Service

## Available methods

### List vesting accounts

`vesting_accounts`

On localhost: `https://localhost:443/vesting_service/actors/vesting_service/vesting_accounts`

It can be called using an http POST with `application/json` as content type and with the following data:

```json
{ "owner_address": "<ADDRESS>"}
```

example using curl:

```sh
curl --insecure -H "Content-Type: application/json" -d '{ "owner_address": "GBB375L64ZDTW2APJMCOCPJROKTR43PA63J4PKK6Q6OD5LTP4ATCI7OJ"}' "https://localhost:443/vesting_service/actors/vesting_service/vesting_accounts"
```

### Get an unvesting transaction

`unvestingtransaction`

On localhost: `https://localhost:443/vesting_service/actors/vesting_service/unvestingtransaction`

It can be called using an http POST with `application/json` as content type and with the following data:

```json
{ "vestingaccount": "<VESTING_ACCOUNT_ADDRESS>"}
```

Return value: The service reurns the bare xdr encoded unvesting transaction envelope, no json structure.

example using curl:

```sh
 curl --insecure -v -H "Content-Type: application/json" -d '{ "vestingaccount":"GBEQG5YYLZFGPX6CIZUJSJHJ26MTLGKRJMT2I44XP3SLVSGKS3Q5BFO6"}' "https://localhost:443/vesting_service/actors/vesting_service/unvestingtransaction"
```

If there is no unvesting transaction for the supplied account:

An `HTTP/1.1 404 Not Found` is returned with `{"error": "No unvesting transaction found for this address"}` as body.

## Threefoldfoundation deployed urls

### Testnet

url: `https://testnet.threefold.io/threefoldfoundation/vesting_service/`

example using curl:

```sh
curl  -H "Content-Type: application/json" -d '{ "owner_address": "GBB375L64ZDTW2APJMCOCPJROKTR43PA63J4PKK6Q6OD5LTP4ATCI7OJ"}' "https://testnet.threefold.io/threefoldfoundation/vesting_service/vesting_accounts"

{"address": "GDKMZFELJER5RNQB6T2Z2JO4ZLH6PN5RHH4ZO6AW4LVPBZCFY2PIRENL"}
```

### Production

url: `https://tokenservices.threefold.io/threefoldfoundation/vesting_service/`
