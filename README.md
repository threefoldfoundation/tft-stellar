# tft-stellar

Threefoldtoken on the stellar network

## Production network

## TFT

### Production network

- assetCode: TFT
- issuer: GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47

### Testnet

- assetCode: TFT
- issuer: GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3

Keep in mind that the stellar testnet is [reset every quarter](https://www.stellar.org/developers/guides/concepts/test-net.html#periodic-reset-of-testnet-data).

## TFTA

### Production network

- assetCode: TFTA
- issuer: GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2

### Testnet

- assetCode: TFTA
- issuer: GB55A4RR4G2MIORJTQA4L6FENZU7K4W7ATGY6YOT2CW47M5SZYGYKSCT

Keep in mind that the stellar testnet is [reset every quarter](https://www.stellar.org/developers/guides/concepts/test-net.html#periodic-reset-of-testnet-data).

## FreeTFT

### Production network

- assetCode: FreeTFT
- issuer: GCBGS5TFE2BPPUVY55ZPEMWWGR6CLQ7T6P46SOFGHXEBJ34MSP6HVEUT

### Testnet

- assetCode: FreeTFT
- issuer: GBLDUINEFYTF7XEE7YNWA3JQS4K2VD37YU7I2YAE7R5AHZDKQXSS2J6R

Keep in mind that the stellar testnet is [reset every quarter](https://www.stellar.org/developers/guides/concepts/test-net.html#periodic-reset-of-testnet-data).

## Acquiring testnet tokens

### TFT

Dex: https://stellar.expert/explorer/testnet/asset/TFT-GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3-1?filter=orderbook

### FreeTFT

- Dex: https://stellar.expert/explorer/testnet/asset/FreeTFT-GBLDUINEFYTF7XEE7YNWA3JQS4K2VD37YU7I2YAE7R5AHZDKQXSS2J6R-2?filter=orderbook
- Faucet: https://getfreetft.testnet.threefold.io

## Wallet implementations

Whil we provide some tooling to make it easier for users of only these tokens, it are regular assets on the Stellar network so any Stellar wallet can be used.

- [Jumpscale](https://github.com/threefoldtech/jumpscaleX_libs/tree/development/JumpscaleLibs/clients/stellar)

## Integration for exchanges

These tokens are regular Stellar custom assets so the normal Stellar documentation for custom assets appplies.

## tft-stellar tooling

This contains following tools:

- [Conversion Service](ThreeBotPackages/conversion-service/readme.md): Service for converting TFChain TFT's to Stellar TFT's.
- [Stellar Faucet](ThreeBotPackages/stellar_faucet/readme.md): Faucet for receiving Testnet Stellar TFT's to any testnet Stellar address.
- [Unlock Service](ThreeBotPackages/unlock-service/readme.md): Service for storing and retrieving unlock transaction for a Stellar Wallet.
- [Transaction funding service](ThreeBotPackages/transactionfunding-service/readme.md): Service for funding TFT transactions with Lumens(XLM).
- [Activation service](ThreeBotPackages/activation-service/readme.md): Service for activation of new accounts.

## Deployed services

### Production services

Url: `https://tokenservices.threefold.io`

Deployed services:

None yet

### Testnet services

Url: `https://testnet.threefold.io`

Deployed services:

- Conversion service
- Unlock Service
- Transaction funding service
- Activation service
- [Freetft faucet](https://getfreetft.testnet.threefold.io)


## Statistics

[A js-sdk script for getting statistics about  one of the tokens is available](lib/stats/readme.md).