# tft-stellar

Threefoldtoken on the stellar network

> Status 13 March 2024:

Total amount of TFT = 891,551,662 + 51,022,747 TFT = 942,574,409 TFT

The maximum amount of TFT will be 1 Billion TFT (originally was planned for 4 billion)

## TFT

- assetCode: TFT
- issuer: GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47

> [TFT Statistics Info](https://stellarchain.io/assets/TFT-GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47)

> 891,551,662 TFT

## TFTA

We used to have another blockchain called rivine (long time ago) and the tokens coming from there were going over TFTA.
A TFTA can be converted to a TFT anytime anyone wants.

- assetCode: TFTA
- issuer: GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2

> [TFTA Statistics Info](https://stellarchain.io/assets/TFTA-GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2)

> 51,022,747 TFT

## Bridges

- [Binance Smart Chain - BSC](https://stellar.expert/explorer/public/account/GBFFWXWBZDILJJAMSINHPJEUJKB3H4UYXRWNB4COYQAF7UUQSWSBUXW5) 68,340,360 TFT
- [Etherium Bridge](https://stellar.expert/explorer/public/account/GARQ6KUXUCKDPIGI7NPITDN55J23SVR5RJ5RFOOU3ZPLMRJYOQRNMOIJ):  3,159,861 TFT
- [TFChain Bridge](https://stellar.expert/explorer/public/account/GBNOTAYUMXVO5QDYWYO2SOCOYIJ3XFIP65GKOQN7H65ZZSO6BK4SLWSC): 6,952,619 TFT 

All TFT on these bridge accounts are locked on Stellar and cannot be used, they are part of the TFT bucket above.

## Wallet implementations

While we provide some tooling to make it easier for users of only these tokens, it are regular assets on the Stellar network so any Stellar wallet can be used.

- [Jumpscale](https://github.com/threefoldtech/jumpscaleX_libs/tree/development/JumpscaleLibs/clients/stellar)

## tft-stellar services

- [Conversion Service](ThreeBotPackages/tfchainmigration_service/readme.md): Service for converting TFChain TFT's to Stellar TFT's.
- [TFT Faucet](ThreeBotPackages/tft_faucet/readme.md): Faucet for receiving Testnet Stellar TFT's to any testnet Stellar address.
- [Unlock Service](ThreeBotPackages/unlock_service/readme.md): Service for storing and retrieving unlock transaction for a Stellar Wallet.
- [Transaction funding service](ThreeBotPackages/transactionfunding_service/readme.md): Service for funding TFT transactions with Lumens(XLM).
- [Activation service](ThreeBotPackages/activation_service/readme.md): Service for activation of new accounts.

Url: `https://tokenservices.threefold.io` (not usable for humans)

Deployed services:

- Conversion service
- Unlock Service
- Transaction funding service
- Activation service
