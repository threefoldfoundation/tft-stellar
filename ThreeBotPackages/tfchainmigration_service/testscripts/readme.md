# Test the conversion service

## Create accounts

```sh
go run createAccounts.go
```

## Fund the tfchain address

- Using the tfchain address from the previous step:
  - ensure this address has some balance in TFT
  - create some locked token transfers using the desktop wallet

with the commandline client:

send some unlocked tokens:

```sh
tfchainc wallet send coins <address> 10
```

send some locked tokens:

with a lock until November 1 2020:

```sh
tfchainc wallet send coins '{"type": 3,"data": {"locktime": 1604188800,"condition": {"type":1,"data":{ "unlockhash":"<address>"}}}}' 11
```

with a lock until November 1 2021:

```sh
tfchainc wallet send coins '{"type": 3,"data": {"locktime": 1635724800,"condition": {"type":1,"data":{ "unlockhash":"<address>"}}}}' 12
```

Deauthorize the account:

```sh
tfchainc wallet send transaction "$(tfchainc wallet sign "$(tfchainc wallet authcoin authaddresses --deauth <address>)")"
```

## Account activation

```sh
curl -H "Content-Type: application/json" -d '{ "args": { "address": "","tfchain_address":""   }}' "http://localhost:7000/threefoldfoundation/conversion_service/activate_account"
```

## Token migration

- Import the converter wallet in JSX
- Create a stellar account with secret from the first step in JSX to add the trustlines to TFT and TFTA:

```python
a= j.clients.stellar.new('migrating',network='TEST',secret='')
a.add_known_trustline('TFT')
a.add_known_trustline('TFTA')
```

**from jsx:**

```python
p.threefoldfoundation.conversion_service.actors.conversion_service.migrate_tokens(stellar_address=stellarclient.address, tfchain_address="<tfchainaddress>")
```

**through curl:**

```sh
curl -H "Content-Type: application/json" -d '{ "args": { "tfchain_address": "", "stellar_address": "" }}' "http://localhost:7000/threefoldfoundation/conversion_service/migrate_tokens"
```

This result is an array of unlock transactionenvelopes in xdr format.
