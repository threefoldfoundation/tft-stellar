# TFT Faucet
A package with a bottle server that allows the transfer of TFTs to fund a wallet that provides a certain stellar wallet address

## Components
- Bottle app

    - POST endpoint `HOST/tft_faucet/api/transfer`
    - request body should include `destination` info in its data
- Stellar wallet instance
    - name: `faucet_wallet`
    - setup with trustlines for TFT (testnet)

- Vue based UI
    - available on `HOST/tft_faucet`
    - user enters the destination address of a wallet and will have the TFTs transfered there

## Usage
To install the package on a host machine, add the package using the repo url through the admin dashboard of js-ng
