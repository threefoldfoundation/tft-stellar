# tft-stellar

Threefoldtoken on the stellar network

## Production network

## TFT

- assetCode: TFT
- issuer: GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47

## TFTA

- assetCode: TFTA
- issuer: GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2

## Token statistics

Token statistics can be seen on [token statistics](https://statsdata.threefoldtoken.com/stellar_stats/api/stats)

[A js-sdk script for getting statistics about  one of the tokens is also available](lib/stats/readme.md).

## Wallet implementations

While we provide some tooling to make it easier for users of only these tokens, it are regular assets on the Stellar network so any Stellar wallet can be used.

- [Jumpscale](https://github.com/threefoldtech/jumpscaleX_libs/tree/development/JumpscaleLibs/clients/stellar)

## Integration for exchanges

These tokens are regular Stellar custom assets so the normal Stellar documentation for custom assets appplies.

## tft-stellar services

- [Conversion Service](ThreeBotPackages/tfchainmigration_service/readme.md): Service for converting TFChain TFT's to Stellar TFT's.
- [TFT Faucet](ThreeBotPackages/tft_faucet/readme.md): Faucet for receiving Testnet Stellar TFT's to any testnet Stellar address.
- [Unlock Service](ThreeBotPackages/unlock_service/readme.md): Service for storing and retrieving unlock transaction for a Stellar Wallet.
- [Transaction funding service](ThreeBotPackages/transactionfunding_service/readme.md): Service for funding TFT transactions with Lumens(XLM).
- [Activation service](ThreeBotPackages/activation_service/readme.md): Service for activation of new accounts.

Url: `https://tokenservices.threefold.io`

Deployed services:

- Conversion service
- Unlock Service
- Transaction funding service
- Activation service
