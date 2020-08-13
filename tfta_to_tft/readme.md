# Service to convert TFTA to TFT

This script issues TFT for destroyed TFTA .

## Functionality

All TFT transactions and their memo_hashes are are collected from the Stellar network.

All TFTA payments to the TFTA issuer account ( destructions of TFTA) are collected.
If the transaction id from a destruction is in the the list of transaction memo hashes, the issuance for that destruction has already happened. If not, the payment is kept aside

We then loop forever with the following logic:

We wait for 60 seconds to be sure all issuances are processed and available through horizon.

All TFT transactions and their memo_hashes are are collected from the Stellar network again.

The kept aside destruction payments are checked.
If  the transaction id from a destruction is in the the list of  transaction memo hashes, the issuance for that destruction has already happened.
If not, the same amount of destroyed TFTA is issued as TFT to the sending account.

All TFTA payments (starting from the last time we checked)  to the TFTA issuer account are collected.
If the transaction id from a destruction is in the the list of tft transaction memo hashes, the issuance for that destruction has already happened. If not, the payment is kept aside

## Requirements

- [js-sdk](https://github.com/threefoldtech/js-sdk) off course
- A wallet that has payment signing rights on the TFT and TFTA issuer accounts (by default `j.clients.stellar.tftatotftissuer`)

## Run it

Enter the js-sdk shell ( `poetry shell` for a development environment).

`./tft_issuer.py`

An optional `--walletname=<anotherwalletname>` parameter can be supplied if another wallet than `j.clients.stellar.tftatotftissuer` needs to be used.

The network to work on is derived from the wallet.

## Support

When a user reports a problem, first ask for the stellar address the TFTA was sent from. Check [stellar.expert](https://stellar.expert/explorer/public) if the TFTA was sent to the correct address and if there indeed was no TFT sent back for the same amount with a memo_hash of the TFTA sending transaction.
