# Service to convert TFTA to TFT

This script issues TFT for destroyed TFTA .

## Functionality

All TFT and TFTA transactions and their memo_hashes are are collected from the Stellar network.

All TFTA payments to the TFTA issuer account ( destructions of TFTA) are collected.
If the transaction id from a destruction is in the the list of transaction memo hashes, the issuance for that destruction has already happened. If not, the payment is kept aside

We then loop forever with the following logic:

We wait for 60 seconds to be sure all issuances are processed and available through horizon.

All and TFTA transactions and their memo_hashes are are collected from the Stellar network again.

The kept aside destruction payments are checked.
If  the transaction id from a destruction is in the the list of  transaction memo hashes, the issuance for that destruction has already happened.
If not, the same amount of destroyed TFTA is issued as TFT to the sending account if the message in the memo_text is correct, If the memo_text is not correct, the same amount of TFTA is sent.

All TFTA payments (starting from the last time we checked)  to the TFTA issuer account are collected.
If the transaction id from a destruction is in the the list of tft transaction memo hashes, the issuance for that destruction has already happened. If not, the payment is kept aside

## Requirements

- [js-sdk](https://github.com/threefoldtech/js-sdk) off course
- A wallet that has payment signing rights on the TFT and TFTA issuer accounts (by default `j.clients.stellar.tftatotftissuer`)

## Run it

Enter the js-sdk shell ( `poetry shell` for a development environment).

`./tft_issuer.py <the required message>`

An optional `--walletname=<anotherwalletname>` parameter can be supplied if another wallet than `j.clients.stellar.tftatotftissuer` needs to be used.

The network to work on is derived from the wallet.
