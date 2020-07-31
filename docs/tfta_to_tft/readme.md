# TFTA to TFT conversion

## Concept

For the conversion to happen, the total amount of TFTA+TFT is not liable to change. This means that newly issued TFTs would require the same amount of TFTAs to be destroyed.

To convert TFTAs into TFT, the user needs to send the particular amount of TFTA to the "TFTA issuer account" address:

GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2

Memo text: "I agree http://tc.grid.tf v1"

IMPORTANT: please include this memo text for every transaction.

The particular amount of TFTAs would be destroyed once the transaction succeeded. A script then collects the destroyed amounts of TFTAs, the sending addresses, the memo text messages, and the transaction ID from the sender.

If the user provided the right memo text, the new TFTs will be issued to the sending addresses,
with the transaction ID, the memo_hash field as a proof of the transaction in between the destruction of the TFTAs and the issuance of the TFTs.

If the user provided a false memo text or left the memo text blank, the burned TFTAs will be re-issued back again to the sending addresses, with the transaction ID, the memo_hash field as a proof of the destruction of the TFTAs.

## 3BOT Wallet Transaction Fee

A fee amount of 0.1 TFTA incurs for every transfer transaction done using the 3Bot Wallet. Therefore, the sender would receive 0.1 TFT less after the conversion. Please contact support@threefold.io if this poses a problem. We would gladly send 0.1 TFT from a different wallet afterwards.

## Important Notice

 - You must read and agree to [Threefold's Disclaimer](https://wiki.threefold.io/#/disclaimer) before doing any TFTA-TFT conversion transaction.
- The "TFTA issuer account" address provided above is the only official address of the TFT Destruction. Please beware of scams and avoid sending TFTAs to addresses from unverified personal social media accounts. Threefold is not liable for any loss or damage caused by unverified transactions.
