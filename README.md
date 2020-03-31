# tft-stellar

Threefoldtoken on the stellar network

## Production network

## TFT

### Production network

- assetCode: TFT
- issuer: GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47

## Testnet

### Testnet

- assetCode: TFT
- issuer: GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3

Keep in mind that the stellar testnet is [reset every quarter](https://www.stellar.org/developers/guides/concepts/test-net.html#periodic-reset-of-testnet-data).

## FreeTFT

### Production network

- assetCode: FreeTFT
- issuer: GCBGS5TFE2BPPUVY55ZPEMWWGR6CLQ7T6P46SOFGHXEBJ34MSP6HVEUT

### Testnet

- assetCode: FreeTFT
- issuer: GBLDUINEFYTF7XEE7YNWA3JQS4K2VD37YU7I2YAE7R5AHZDKQXSS2J6R

Keep in mind that the stellar testnet is [reset every quarter](https://www.stellar.org/developers/guides/concepts/test-net.html#periodic-reset-of-testnet-data).

## Wallet implementations

- [Jumpscale](https://github.com/threefoldtech/jumpscaleX_libs/tree/development/JumpscaleLibs/clients/stellar)

## tft-stellar tooling

This contains following tools:

- [Conversion Service](ThreeBotPackages/conversion-service/readme.md): Service for converting TFChain TFT's to Stellar TFT's.
- [Stellar Faucet](ThreeBotPackages/stellar-faucet/readme.md): Faucet for receiving Testnet Stellar TFT's to any testnet Stellar address.
- [Unlock Service](ThreeBotPackages/unlock-service/readme.md): Service for storing and retrieving unlock transaction for a Stellar Wallet.
- [Transaction funding service](ThreeBotPackages/transactionfunding-service/readme.md): Service for funding TFT transactions with Lumens(XLM).
- [Activation service](ThreeBotPackages/activation-service/readme.md): Service for activation of new accounts.

## Deployed services

### Testnet services

Url: `https://testnet.threefold.io`

Deployed services:

- Conversion service
- Unlock Service
- Transaction funding service
