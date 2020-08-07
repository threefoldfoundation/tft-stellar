# TFTA to TFT conversion

## Concept

The total amount of TFTA+TFT can not change. This means that newly issued TFT requires the same amount of TFTA to be destroyed.
This also gets verified by the validation scripts.

People have to send  TFTA to the TFTA issuer account `GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2`
This acually destroys the TFTA.

A bot hosted in Dubai collects the destroyed amounts, the sending addresses and the transaction id's and prepares the required minting action.

Verification scripts will check the transaction & get to consensus (5/7) to make sure all goes as it should.
The consensus is done by means of multisignature feature on Stellar blockchain.

Using this information, new TFT are issued  to the sending addresses for these amounts with the transaction id the memo_hash field as a proof of the relationship between the destruction and the issuance.

## side effects

Since 0.1 TFTA is added as a transaction fee when using the 3bot wallet, 0.1 TFT less will be issued tan the user has totally spent. 
