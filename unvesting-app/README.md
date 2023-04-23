# UnVesting webapp

A small website that operates completely from the browser.

It lets someone search for a vesting account using a Stellar address and if found, it fetches the unvesting transaction from the vesting_service.

The user can then sign it with its private key and submit it to the Stellar network.

The private key is only used inside the webpage to sign the transaction and is never stored or sent anywhere.

## Requirements

This projects uses `svelte` and `vite` and it depandes on `npx`

- [npx](https://www.npmjs.com/package/npx)

## Network configuration

It all depends on the stellar network, You have to set configure the network in [config.js](./public/config.js) file.

`window.STELLAR_NETWORK` options.

- test
- main

## How to run

```sh
    yarn && yarn dev 
```

## Production URL

<https://tokenservices.threefold.io/unvest/>
