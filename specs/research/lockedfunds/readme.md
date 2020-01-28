# Locked funds research

[Problem description](../../lockedfunds.md#Problem)

## Testscripts

The scripts use the python virtualenv described and used in the [regular scripts](../../../scripts).

### Creating the accounts

**Creating the keypairs:**

```sh
rob@MacBook-Pro-783 scripts % ../common/createAccounts.py from to
Creating 'from' keypair
Key: SA.....
Address: GBDSGJV7T4H5GFC5WJTPG4F7W7TBUWBOK7GPLQEDBVODH37VK2U4B7WB
account 'GBDSGJV7T4H5GFC5WJTPG4F7W7TBUWBOK7GPLQEDBVODH37VK2U4B7WB' activated through friendbot
Creating 'to' keypair
Key: SB....
Address: GACDYYBJIGPT5RNORYGTFA46MVLMU5GY7JQ3NHW6AIEOMIH63VWFHTIN
account 'GACDYYBJIGPT5RNORYGTFA46MVLMU5GY7JQ3NHW6AIEOMIH63VWFHTIN' activated through friendbot
```

**Adding Trustlines:**

Trustlines to the custom asset have to be created for the sending and receiving account.

```sh
../common/addTrustlines.py <FROM_SECRET_KEY> <TO_SECRET_KEY>
{'_links': {'transaction': {'href': 'https://horizon-testnet.stellar.org/transactions/1e13d835944007fc1fd46c0b8423b22165b65f8f78df222e84e2ec1d00212a1b'}}, 'hash': '1e13d835944007fc1fd46c0b8423b22165b65f8f78df222e84e2ec1d00212a1b', 'ledger': 1346220, 'envelope_xdr': 'AAAAAEcjJr+fD9MUXbJm83C/t+YaWC5XzPXAgw1cM+/1VqnAAAAAZAAUiooAAAABAAAAAAAAAAAAAAABAAAAAAAAAAYAAAABVEZUAAAAAAA5/GQbeotMseuGw9LomxJQHv5mNT8nihPVgEwpv/efZH//////////AAAAAAAAAAH1VqnAAAAAQLX9uDgaAy+wnSYuD6QDHnLTfTKqNF/1EZkGo52tnmzqiowScud9aNVvmQku+a5ecxchDFCqo4uWvWuZHonsVgk=', 'result_xdr': 'AAAAAAAAAGQAAAAAAAAAAQAAAAAAAAAGAAAAAAAAAAA=', 'result_meta_xdr': 'AAAAAQAAAAIAAAADABSKrAAAAAAAAAAARyMmv58P0xRdsmbzcL+35hpYLlfM9cCDDVwz7/VWqcAAAAAXSHbnnAAUiooAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAABABSKrAAAAAAAAAAARyMmv58P0xRdsmbzcL+35hpYLlfM9cCDDVwz7/VWqcAAAAAXSHbnnAAUiooAAAABAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAABAAAAAwAAAAMAFIqsAAAAAAAAAABHIya/nw/TFF2yZvNwv7fmGlguV8z1wIMNXDPv9VapwAAAABdIduecABSKigAAAAEAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAEAFIqsAAAAAAAAAABHIya/nw/TFF2yZvNwv7fmGlguV8z1wIMNXDPv9VapwAAAABdIduecABSKigAAAAEAAAABAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAFIqsAAAAAQAAAABHIya/nw/TFF2yZvNwv7fmGlguV8z1wIMNXDPv9VapwAAAAAFURlQAAAAAADn8ZBt6i0yx64bD0uibElAe/mY1PyeKE9WATCm/959kAAAAAAAAAAB//////////wAAAAEAAAAAAAAAAA=='}
Added trustline to TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3 for account GBDSGJV7T4H5GFC5WJTPG4F7W7TBUWBOK7GPLQEDBVODH37VK2U4B7WB
{'_links': {'transaction': {'href': 'https://horizon-testnet.stellar.org/transactions/6c27fcb1752db4d5e57d85373c9d6b00f3ef7df2475dd98e8080d65be89b26ff'}}, 'hash': '6c27fcb1752db4d5e57d85373c9d6b00f3ef7df2475dd98e8080d65be89b26ff', 'ledger': 1346221, 'envelope_xdr': 'AAAAAAQ8YClBnz7Fro4NMoOeZVbKdNj6Ybae3gII5iD+3WxTAAAAZAAUiosAAAABAAAAAAAAAAAAAAABAAAAAAAAAAYAAAABVEZUAAAAAAA5/GQbeotMseuGw9LomxJQHv5mNT8nihPVgEwpv/efZH//////////AAAAAAAAAAH+3WxTAAAAQCbD2hum0wBPVJOowNCBVpfM5u5dAiL0Ve1qukdK01FTbl8i8JY7IVZLiIW9ZO9b4Q41uw4KlvxyDjN9F9nH2gw=', 'result_xdr': 'AAAAAAAAAGQAAAAAAAAAAQAAAAAAAAAGAAAAAAAAAAA=', 'result_meta_xdr': 'AAAAAQAAAAIAAAADABSKrQAAAAAAAAAABDxgKUGfPsWujg0yg55lVsp02Pphtp7eAgjmIP7dbFMAAAAXSHbnnAAUiosAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAABABSKrQAAAAAAAAAABDxgKUGfPsWujg0yg55lVsp02Pphtp7eAgjmIP7dbFMAAAAXSHbnnAAUiosAAAABAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAABAAAAAwAAAAMAFIqtAAAAAAAAAAAEPGApQZ8+xa6ODTKDnmVWynTY+mG2nt4CCOYg/t1sUwAAABdIduecABSKiwAAAAEAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAEAFIqtAAAAAAAAAAAEPGApQZ8+xa6ODTKDnmVWynTY+mG2nt4CCOYg/t1sUwAAABdIduecABSKiwAAAAEAAAABAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAFIqtAAAAAQAAAAAEPGApQZ8+xa6ODTKDnmVWynTY+mG2nt4CCOYg/t1sUwAAAAFURlQAAAAAADn8ZBt6i0yx64bD0uibElAe/mY1PyeKE9WATCm/959kAAAAAAAAAAB//////////wAAAAEAAAAAAAAAAA=='}
Added trustline to TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3 for account GACDYYBJIGPT5RNORYGTFA46MVLMU5GY7JQ3NHW6AIEOMIH63VWFHTIN
```

### Fund the sending account with the custom asset

Either use the TFT faucet or if you have access to testnet assets, use your testnet wallet or the `../common/fundWithAsset.py` script to send some tokens to the `from` account.

```sh
../common/fundWithAsset.py GBDSGJV7T4H5GFC5WJTPG4F7W7TBUWBOK7GPLQEDBVODH37VK2U4B7WB --signer=<SOURCE_SECRET_KEY>
{'_links': {'transaction': {'href': 'https://horizon-testnet.stellar.org/transactions/a83359277a22f731ddcab975f87fb0c466ad5ed4a18abf1725055ae7423ddd6f'}}, 'hash': 'a83359277a22f731ddcab975f87fb0c466ad5ed4a18abf1725055ae7423ddd6f', 'ledger': 1346264, 'envelope_xdr': 'AAAAADn8ZBt6i0yx64bD0uibElAe/mY1PyeKE9WATCm/959kAAAAZAASKjQAAAADAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAARyMmv58P0xRdsmbzcL+35hpYLlfM9cCDDVwz7/VWqcAAAAABVEZUAAAAAAA5/GQbeotMseuGw9LomxJQHv5mNT8nihPVgEwpv/efZAAAAAAF9eEAAAAAAAAAAAG/959kAAAAQPuE6+9QdvGB0tDcX61rMo+lBvpF7u+lUh6Rmu5SZJLWHC8n4fozA2WoL4N9Hz6/hdvOE+oV2iwzjsSITjQ8xAM=', 'result_xdr': 'AAAAAAAAAGQAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAA=', 'result_meta_xdr': 'AAAAAQAAAAIAAAADABSK2AAAAAAAAAAAOfxkG3qLTLHrhsPS6JsSUB7+ZjU/J4oT1YBMKb/3n2QAAAAXSHbm1AASKjQAAAACAAAAAAAAAAAAAAAAAAAAEXd3dzIudGhyZWVmb2xkLmlvAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAEAFIrYAAAAAAAAAAA5/GQbeotMseuGw9LomxJQHv5mNT8nihPVgEwpv/efZAAAABdIdubUABIqNAAAAAMAAAAAAAAAAAAAAAAAAAARd3d3Mi50aHJlZWZvbGQuaW8AAAABAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAIAAAADABSKrAAAAAEAAAAARyMmv58P0xRdsmbzcL+35hpYLlfM9cCDDVwz7/VWqcAAAAABVEZUAAAAAAA5/GQbeotMseuGw9LomxJQHv5mNT8nihPVgEwpv/efZAAAAAAAAAAAf/////////8AAAABAAAAAAAAAAAAAAABABSK2AAAAAEAAAAARyMmv58P0xRdsmbzcL+35hpYLlfM9cCDDVwz7/VWqcAAAAABVEZUAAAAAAA5/GQbeotMseuGw9LomxJQHv5mNT8nihPVgEwpv/efZAAAAAAF9eEAf/////////8AAAABAAAAAAAAAAA='}
Sent 10 TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3 to GBDSGJV7T4H5GFC5WJTPG4F7W7TBUWBOK7GPLQEDBVODH37VK2U4B7WB
```

### Send locked funds

Process:

1. Create an escrow account
2. Add a trustline from the escrow account to the custom asset
3. Create a signed unlock transaction (can oly be submitted after the unlock time) that sets the signing options of the escrow account to
    - require only 1 signature
    - remove the escrow account as signer
4. Set the signing options for the escrow account to 
    - requires 2 signatures
    - add the receiver as signer
    - add the hash of the unlock transaction as signer
5. Send the custom assets to the escrow account

```sh
./sendLockedFunds.py <FROM_SECRET_KEY> GACDYYBJIGPT5RNORYGTFA46MVLMU5GY7JQ3NHW6AIEOMIH63VWFHTIN
```

### Receiving locked funds

The serialized unlock transaction should be kept to submit to the network after the unlock time has expired.
After this, the destination account can merge the escrow account with it's own.

It is possible to find all escrow accounts where the destination is a signer since the [horizon server supports it](https://www.stellar.org/developers/horizon/reference/endpoints/accounts.html). as demonstrated in the 'findEscrowAccounts.py script.

```sh
./findEscrowAccounts.py GACDYYBJIGPT5RNORYGTFA46MVLMU5GY7JQ3NHW6AIEOMIH63VWFHTIN
Account GB23ATJXDRUFQTTUCVQ5YUIG3TJ4YZP3NPUXAS6CVPYESWP7XXWNKYXL with 1.0000000 TFT has unlocktransaction hashes ['TB2PBXB443YJOA5JSU35UJQIJF2FD4F7XHK77Z4QWWDXSGEX7FD2AUEI']
Account GBGQGHALUVLQTX6E2J2OZ7H6MPN663YZ7363WB34UJ7EW5YHJZVWISTS with 1.0000000 TFT has unlocktransaction hashes ['TBTVIHAGD6DRVAXAHCBQ7T2OF5KJPB3MYZG5JI4GWMUOLUW6IRTXD2EL']
```