# UnVesting webapp

A small website that operates completely from the browser.

It lets someone search for a vesting account using a Stellar address and if found, it fetches the unvesting transaction from the vesting_service.

The user can then sign it with its private key and submit it to the Stellar network.

The private key is only used inside the webpage to sign the transaction and is never stored or sent anywhere.

## Requirements

This projects uses `svelte` and `vite` and it depandes on `npx`

- [npx](https://www.npmjs.com/package/npx)

## Build environment

It all depends on the stellar network, by default we set it to be works against `testnet`, but if you want to change it just export it and then run the `build-env.sh` script inside the `public` directory.

```sh
    export STELLAR_NETWORK=main
    cd public && source ../scripts/build-env.sh
```

## How to run

```sh
    yarn && yarn dev 
```
