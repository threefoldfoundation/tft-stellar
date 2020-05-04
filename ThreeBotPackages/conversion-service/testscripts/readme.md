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
tfchainc wallet send coins address amount
```

## Account activation

```sh
curl -H "Content-Type: application/json" -d '{ "args": { "address": "","tfchain_address":""   }}' "http://localhost:7000/threefoldfoundation/conversion_service/activate_account"
```

## Token migration

Comment out lines 80-81, 92-93, 96-102 in `./actors/conversion_service.py`

The reason we comment this out is to skip folowing steps for easy testing:

- lock tfchain address

Start the Threebot server with these lines commented out

- Import the converter wallet in JSX
- Create a stellar account with secret from the first step in JSX to addthe  trustlines to TFT and TFTA:

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
curl -H "Content-Type: application/json" -d '{ "args": { "tfchain_address": "", "stellar_address": "" }}' "http://localhost/threefoldfoundation/conversion_service/migrate_tokens"
```

This result is an array of unlock transactionenvelopes in xdr format.
