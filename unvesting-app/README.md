# UnVesting webapp

A small website that operates completely from the browser.

It lets someone search for a vesting account using a Stellar address and if found, it fetches the unvesting transaction from the vesting_service.

The user can then sign it with its private key and submit it to the Stellar network.

The private key is only used inside the webpage to sign the transaction and is never stored or sent anywhere.

## How to run

```sh
    yarn & yarn dev 
```
