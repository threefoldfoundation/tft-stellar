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


## Requirements and Running 

Make sure the wallet with the name `faucet_wallet` exists and is saved:

```python
# Import an existing wallet 
j.clients.stellar.new("faucet_wallet", network="TEST",secret="<activation_secret>")

#OR create a new wallet instance and activate it
wallet = j.clients.stellar.new("faucet_wallet", network="TEST")
wallet.activate_through_friendbot() # Activate wallet
wallet.add_known_trustline("TFT") # Add TFT trustline

# Save the wallet
j.clients.stellar.faucet_wallet.save()
```
Fund the wallet with TFTs to transfer from

clone this repository:

```python
j.tools.git.ensure_repo("https://github.com/threefoldfoundation/tft-stellar.git")
```

execute the following command in jsng shell:
`j.servers.threebot.start_default()`

Once this process is completed add the package to the threebot server from jsng shell like this:

```python
j.servers.threebot.default.packages.add(giturl="https://github.com/threefoldfoundation/tft-stellar/tree/master/ThreeBotPackages/tft_faucet")
```

## Usage
Access the browser through `<HOST>/tft_faucet` and add the address of a new activated wallet that needs funding
