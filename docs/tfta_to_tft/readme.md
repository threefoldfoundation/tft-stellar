# TFTA to TFT conversion

## Concept

The total amount of TFTA+TFT can not change. This means that newly issued TFT requires the same amount of TFTA to be destroyed.

People have to send this amount of TFTA to the TFTA issuer account `GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2`
This acually destroys the TFTA.

Next, a conversion bot hosted in Dubai collects the destroyed amounts, the sending addresses, the memo text messages  and the transaction id's.

Using this information,  if the memo text is correct (accepting the terms & conditions), new TFT are issued (using multisignature) to the sending addresses for these amounts with the transaction id the memo_hash field as a proof of the relationship between the destruction and the issuance.

If the memo text is not correct, The burned TFTA's are issued again to the sending addresses for these amounts with the transaction id the memo_hash field as a proof of the relationship between the destruction and the issuance.



## side effects

Since 0.1 TFTA is added as a transaction fee when using the 3bot wallet, 0.1 TFT less will be issued then. 
