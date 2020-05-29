# Limited TFTA to TFT conversion

This document is not about who is allowed to convert how much and when. It only describes the technical process for a limited conversion of TFTA to TFT.

## Concept

The total amount of TFTA+TFT can not change. This means that newly issued TFT requires the same amount of TFTA to be destroyed.

A list of addresses is collected together with the amount they are allowed to convert.

These people have to send this amount of TFTA to the TFTA issuer account `GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2`
This acually destroys the TFTA.

Next, a script collects the destroyed amounts, the sending addresses and the transaction id's.
Using this information, new TFT are issued  to the sending addresses for these amounts with the transaction id the memo_hash field to proove the relationship between the destruction and the issuance.

## side effects

Since 0.1 TFTA is added as a transaction fee when using the 3bot wallet, 0.1 TFTA less then the allowed amount has to be sent from the wallet or the transaction will fail.

Also, 0.1 TFT less then the allowed amount will be issued then. If this poses a problem for some people, we will send 0.1 TFT from a different wallet afterwards.
