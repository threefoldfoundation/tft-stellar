# External Funding

## Problem

Transaction fees for TFT on the Stellar platform should be paid in Lumen (XLM) and not in TFT.
It is uncomfortable for users to require and purchase Lumen to be able to do TFT transactions.

## Posssible solution

An option is to fund the transactions from the Threefoldfoundation since transaction fees are very low.

An extra option might be that having the Threefoldfoundation fund the Lumen for the transaction fee is paid by the user in TFT so it feels like the transaction fee is actually in TFT.

## Stellar signatures

In Stellar, there is the notion of a transaction and a transacyion envelope. The transaction contains all information and the transaction envelope contains the transaction + the required signatures.

Signatures are made over hash(network id, transaction envelopetype identifier,serialized transaction).

This means that signatures can only be added if the complete transaction is already constructed.

## Testscripts

The scripts use the python virtualenv described and used in the [regular scripts](../../../scripts).

### Creating the accounts

**Creating the keypairs:**

```sh
rob@MacBook-Pro-783 scripts % ../common/createAccounts.py from to funding
Creating 'from' keypair
Key: Sxxx....
Address: GAXABB7JFCAS5G2BBBD6PZ3U64C2UZXMW4UH6Y7FWZYK7EXBGCRWEV33
account 'GAXABB7JFCAS5G2BBBD6PZ3U64C2UZXMW4UH6Y7FWZYK7EXBGCRWEV33' activated through friendbot
Creating 'to' keypair
Key: Sxxx....
Address: GBDT4FNNBGGELAHVCTH4N2ITCQGZIYGAWYASOG63KRUHHKW5O4TPYHLU
account 'GBDT4FNNBGGELAHVCTH4N2ITCQGZIYGAWYASOG63KRUHHKW5O4TPYHLU' activated through friendbot
Creating 'funding' keypair
Key: Sxxx....
Address: GCIR7XWPO62E6U7PS2GBK6PN3JBGE56F6TDAGCXGTJJG5MYRUTBRAJ6J
account 'GCIR7XWPO62E6U7PS2GBK6PN3JBGE56F6TDAGCXGTJJG5MYRUTBRAJ6J' activated through friendbot
```

**Adding Trustlines:**

Trustlines to the custom asset have to be created for the sending and receiving account, not the funding account.

```sh
../common/addTrustlines.py <FROM_SECRET_KEY> <TO_SECRET_KEY>
{'_links': {'transaction': {'href': 'https://horizon-testnet.stellar.org/transactions/8fba46ffdf34a70b83b0756ef74a315dbdf2fba2027341d36083bb421517f065'}}, 'hash': '8fba46ffdf34a70b83b0756ef74a315dbdf2fba2027341d36083bb421517f065', 'ledger': 1314649, 'envelope_xdr': 'AAAAAC4Ah+kogS6bQQhH5+d09wWqZuy3KH9j5bZwr5LhMKNiAAAAZAAT2/AAAAABAAAAAAAAAAAAAAABAAAAAAAAAAYAAAABVEZUAAAAAAA5/GQbeotMseuGw9LomxJQHv5mNT8nihPVgEwpv/efZH//////////AAAAAAAAAAHhMKNiAAAAQEahkb4U45O0NATHU+ASxqdEN5MwcHmf+sdvJQnrAEmfUqpQ2O5lkrImozH0qFkefNXRX0HCpQCmDijTRdjvtQQ=', 'result_xdr': 'AAAAAAAAAGQAAAAAAAAAAQAAAAAAAAAGAAAAAAAAAAA=', 'result_meta_xdr': 'AAAAAQAAAAIAAAADABQPWQAAAAAAAAAALgCH6SiBLptBCEfn53T3Bapm7Lcof2PltnCvkuEwo2IAAAAXSHbnnAAT2/AAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAABABQPWQAAAAAAAAAALgCH6SiBLptBCEfn53T3Bapm7Lcof2PltnCvkuEwo2IAAAAXSHbnnAAT2/AAAAABAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAABAAAAAwAAAAMAFA9ZAAAAAAAAAAAuAIfpKIEum0EIR+fndPcFqmbstyh/Y+W2cK+S4TCjYgAAABdIduecABPb8AAAAAEAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAEAFA9ZAAAAAAAAAAAuAIfpKIEum0EIR+fndPcFqmbstyh/Y+W2cK+S4TCjYgAAABdIduecABPb8AAAAAEAAAABAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAFA9ZAAAAAQAAAAAuAIfpKIEum0EIR+fndPcFqmbstyh/Y+W2cK+S4TCjYgAAAAFURlQAAAAAADn8ZBt6i0yx64bD0uibElAe/mY1PyeKE9WATCm/959kAAAAAAAAAAB//////////wAAAAEAAAAAAAAAAA=='}
Added trustline to TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3 for account GAXABB7JFCAS5G2BBBD6PZ3U64C2UZXMW4UH6Y7FWZYK7EXBGCRWEV33
{'_links': {'transaction': {'href': 'https://horizon-testnet.stellar.org/transactions/1cdea2dd8797ce1d069211a122876d202b8c5bb1e6abc3f11863b021324da0f8'}}, 'hash': '1cdea2dd8797ce1d069211a122876d202b8c5bb1e6abc3f11863b021324da0f8', 'ledger': 1314650, 'envelope_xdr': 'AAAAAEc+Fa0JjEWA9RTPxukTFA2UYMC2AScb21Roc6rddyb8AAAAZAAT2/EAAAABAAAAAAAAAAAAAAABAAAAAAAAAAYAAAABVEZUAAAAAAA5/GQbeotMseuGw9LomxJQHv5mNT8nihPVgEwpv/efZH//////////AAAAAAAAAAHddyb8AAAAQKI8u5mnZjwY7nwwRMz+unavKb2kJ++c0wrXlLmYu5MsAHSs8zuFnkVSTZV7tqCSfNSSthvtJ/maTasm1YOSPAo=', 'result_xdr': 'AAAAAAAAAGQAAAAAAAAAAQAAAAAAAAAGAAAAAAAAAAA=', 'result_meta_xdr': 'AAAAAQAAAAIAAAADABQPWgAAAAAAAAAARz4VrQmMRYD1FM/G6RMUDZRgwLYBJxvbVGhzqt13JvwAAAAXSHbnnAAT2/EAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAABABQPWgAAAAAAAAAARz4VrQmMRYD1FM/G6RMUDZRgwLYBJxvbVGhzqt13JvwAAAAXSHbnnAAT2/EAAAABAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAABAAAAAwAAAAMAFA9aAAAAAAAAAABHPhWtCYxFgPUUz8bpExQNlGDAtgEnG9tUaHOq3Xcm/AAAABdIduecABPb8QAAAAEAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAEAFA9aAAAAAAAAAABHPhWtCYxFgPUUz8bpExQNlGDAtgEnG9tUaHOq3Xcm/AAAABdIduecABPb8QAAAAEAAAABAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAFA9aAAAAAQAAAABHPhWtCYxFgPUUz8bpExQNlGDAtgEnG9tUaHOq3Xcm/AAAAAFURlQAAAAAADn8ZBt6i0yx64bD0uibElAe/mY1PyeKE9WATCm/959kAAAAAAAAAAB//////////wAAAAEAAAAAAAAAAA=='}
Added trustline to TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3 for account GBDT4FNNBGGELAHVCTH4N2ITCQGZIYGAWYASOG63KRUHHKW5O4TPYHLU
```

### Fund the sending account with the custom asset

Either use the TFT faucet or if you have access to testnet assets, use your testnet wallet or the `fundWithAsset.py` script to send some tokens to the `from` account.

```sh
../common/fundWithAsset.py GAXABB7JFCAS5G2BBBD6PZ3U64C2UZXMW4UH6Y7FWZYK7EXBGCRWEV33 --signer=<SOURCE_SECRET_KEY>
{'_links': {'transaction': {'href': 'https://horizon-testnet.stellar.org/transactions/9b20ed8f48abca15844628eb7e9a356f4eaa408c817e78a8dd9ea6f0604c07e2'}}, 'hash': '9b20ed8f48abca15844628eb7e9a356f4eaa408c817e78a8dd9ea6f0604c07e2', 'ledger': 1315596, 'envelope_xdr': 'AAAAADn8ZBt6i0yx64bD0uibElAe/mY1PyeKE9WATCm/959kAAAAZAASKjQAAAACAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAALgCH6SiBLptBCEfn53T3Bapm7Lcof2PltnCvkuEwo2IAAAABVEZUAAAAAAA5/GQbeotMseuGw9LomxJQHv5mNT8nihPVgEwpv/efZAAAAAAF9eEAAAAAAAAAAAG/959kAAAAQN8rzq+N3e5YG7cXlhRenaBxCX2Kv0aNRJS+abyMAT/alZpsDAynJj4Shyooif2zz4ciGprs8pNQ02PdfNhg+Qc=', 'result_xdr': 'AAAAAAAAAGQAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAA=', 'result_meta_xdr': 'AAAAAQAAAAIAAAADABQTDAAAAAAAAAAAOfxkG3qLTLHrhsPS6JsSUB7+ZjU/J4oT1YBMKb/3n2QAAAAXSHbnOAASKjQAAAABAAAAAAAAAAAAAAAAAAAAEXd3dzIudGhyZWVmb2xkLmlvAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAEAFBMMAAAAAAAAAAA5/GQbeotMseuGw9LomxJQHv5mNT8nihPVgEwpv/efZAAAABdIduc4ABIqNAAAAAIAAAAAAAAAAAAAAAAAAAARd3d3Mi50aHJlZWZvbGQuaW8AAAABAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAIAAAADABQPWQAAAAEAAAAALgCH6SiBLptBCEfn53T3Bapm7Lcof2PltnCvkuEwo2IAAAABVEZUAAAAAAA5/GQbeotMseuGw9LomxJQHv5mNT8nihPVgEwpv/efZAAAAAAAAAAAf/////////8AAAABAAAAAAAAAAAAAAABABQTDAAAAAEAAAAALgCH6SiBLptBCEfn53T3Bapm7Lcof2PltnCvkuEwo2IAAAABVEZUAAAAAAA5/GQbeotMseuGw9LomxJQHv5mNT8nihPVgEwpv/efZAAAAAAF9eEAf/////////8AAAABAAAAAAAAAAA='}
Sent 10 TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3 to GAXABB7JFCAS5G2BBBD6PZ3U64C2UZXMW4UH6Y7FWZYK7EXBGCRWEV33

### Execute an externally funded payment

```sh
./externallyFundedPayment.py --from_secret=<FROM_SECRET> --funder_secret=<FUNDER_SECRET> GBDT4FNNBGGELAHVCTH4N2ITCQGZIYGAWYASOG63KRUHHKW5O4TPYHLU
{'_links': {'transaction': {'href': 'https://horizon-testnet.stellar.org/transactions/f861663dc2e98aca37fac5d8e3aaca4f1bbf875e0f0cbc26c47f80b0c0a11254'}}, 'hash': 'f861663dc2e98aca37fac5d8e3aaca4f1bbf875e0f0cbc26c47f80b0c0a11254', 'ledger': 1317583, 'envelope_xdr': 'AAAAAJEf3s93tE9T75aMFXnt2kJid8X0xgMK5ppSbrMRpMMQAAAAZAAT2/IAAAABAAAAAAAAAAAAAAABAAAAAQAAAAAuAIfpKIEum0EIR+fndPcFqmbstyh/Y+W2cK+S4TCjYgAAAAEAAAAARz4VrQmMRYD1FM/G6RMUDZRgwLYBJxvbVGhzqt13JvwAAAABVEZUAAAAAAA5/GQbeotMseuGw9LomxJQHv5mNT8nihPVgEwpv/efZAAAAAAAmJaAAAAAAAAAAALhMKNiAAAAQBkkYy5A4LPxr5LcPHcKfmoeEC+uFw8gr7cPTRIuYKlnoV2241Ge7SxpV5epd2efevKsZutqLqCery6l+9kJsgwRpMMQAAAAQGpTjzAfLxzYVzEKL8MsboGN/1GDeTohFBHnl2YOpT/o80zdSpK95CEBiCah435HBlI66S1DmzqoVqK95H3U+wI=', 'result_xdr': 'AAAAAAAAAGQAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAA=', 'result_meta_xdr': 'AAAAAQAAAAIAAAADABQazwAAAAAAAAAAkR/ez3e0T1PvlowVee3aQmJ3xfTGAwrmmlJusxGkwxAAAAAXSHbnnAAT2/IAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAABABQazwAAAAAAAAAAkR/ez3e0T1PvlowVee3aQmJ3xfTGAwrmmlJusxGkwxAAAAAXSHbnnAAT2/IAAAABAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAABAAAABAAAAAMAFA9aAAAAAQAAAABHPhWtCYxFgPUUz8bpExQNlGDAtgEnG9tUaHOq3Xcm/AAAAAFURlQAAAAAADn8ZBt6i0yx64bD0uibElAe/mY1PyeKE9WATCm/959kAAAAAAAAAAB//////////wAAAAEAAAAAAAAAAAAAAAEAFBrPAAAAAQAAAABHPhWtCYxFgPUUz8bpExQNlGDAtgEnG9tUaHOq3Xcm/AAAAAFURlQAAAAAADn8ZBt6i0yx64bD0uibElAe/mY1PyeKE9WATCm/959kAAAAAACYloB//////////wAAAAEAAAAAAAAAAAAAAAMAFBMMAAAAAQAAAAAuAIfpKIEum0EIR+fndPcFqmbstyh/Y+W2cK+S4TCjYgAAAAFURlQAAAAAADn8ZBt6i0yx64bD0uibElAe/mY1PyeKE9WATCm/959kAAAAAAX14QB//////////wAAAAEAAAAAAAAAAAAAAAEAFBrPAAAAAQAAAAAuAIfpKIEum0EIR+fndPcFqmbstyh/Y+W2cK+S4TCjYgAAAAFURlQAAAAAADn8ZBt6i0yx64bD0uibElAe/mY1PyeKE9WATCm/959kAAAAAAVdSoB//////////wAAAAEAAAAAAAAAAA=='}
Sent 1 TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3 from GAXABB7JFCAS5G2BBBD6PZ3U64C2UZXMW4UH6Y7FWZYK7EXBGCRWEV33 to GBDT4FNNBGGELAHVCTH4N2ITCQGZIYGAWYASOG63KRUHHKW5O4TPYHLU funded by GCIR7XWPO62E6U7PS2GBK6PN3JBGE56F6TDAGCXGTJJG5MYRUTBRAJ6J
```

## Conclusion

It is perfectly possible to  fund a transaction from a different account.

Given the way how signatures work in Stellar( as explained earlier), the transaction needs to be complete before anything can be signed. As a consequence, the client needs to know the funding service's details, even with the sequence number which might cause problems.

Another option is to have the funding service fill in the transaction details,sign it and give it back to the client that needs to verify if everything is still correct, sign and publish it.

One can also add a fee in TFT for the funding service to accept the transaction to fund or it can be added by the funding service and then it's up to the client to accept it.
