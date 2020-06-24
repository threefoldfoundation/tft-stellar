# Initial TFTA to TFT conversion

## Concept

The total amount of TFTA+TFT can not change. This means that newly issued TFT requires the same amount of TFTA to be destroyed.

There is a [Functional description](https://wiki.threefold.io/#/threefold_marketmaker_bot) that describes the high level process for people wanting to convert.

Some [initial thoughts](./initial_thoughts.md) are available listing different options with pro's and cons.

The gradual conversion should only be in place until the end of 2020 after which all TFTA's  are allowed to be converted in to TFT's.

### Single TFTA holder

From the functional description:
> Every TFTA holder can place sell orders on the digitized market maker bot, only 1 order can be open at the same time per TFTA holder.

How do you define a single TFTA holder? Everyone can create as many Stellar accounts as they want.

Currently the best option is to link the trade orders to a 3bot connect user.

## Proposal

A website which requires a 3bot connect login  and where a new trade can be offered to the trader bot or where an existing trade offer can be cancelled.

A new trade offered to the trading bot will be presented to the user as a payment to be made with a genereated id which is required as a memotext. If the 3bot wallet is used, a qr-code can be scanned to prevent typing or copy-paste mistakes.

### Reasoning

A simple solution has been chosen honouring the Single TFTA holder concept and the ability for other Stellar wallets than the  3bot app one to be used.

## Solution

A website protected by a 3bot login to manage your trades.

### BCDB Schemas

```toml
@url = threefoldfoundation.tfta_to_tft__service.order

threebotid** = (S)
trade_id**= (S)

stellaraddress** = (S)
original_amount = (F)
payment_transaction_id = (S)
payment_received = (T)
amount_left= (F)
cancelled = False (B)
refund_transaction_id = (S)
distribution_ongoing = False (B)
```

```toml
@url = threefoldfoundation.tfta_to_tft__service.distribution

threebotid** = (S)
trade_id**= (S)

stellaraddress** = (S)

transaction_id = (T)
amount= (F)
```

### Transfer requests

Since there seems no fits all solution for payment requests that [all wallets support](https://github.com/threefoldfoundation/tft-stellar/issues/173). A qr code supported by the 3bot wallet will be shown together with the destination address and the trade id that needs to be supplied in the memo text field.

A messsage indicating that "If your wallet does not support the qr code, be sure to correctly copy the address and the memo text or your trade can not be accepted." must be shown to make this clear to the user.

### Trade Cancellation

A user can choose to cancel the outstanding trade, the remaining amount will be transferred back to the address it originates from, this address should be shown to the user after which a proceed/cancel option should be shown.

### Distribution

 The `distribution_ongoing` flag is set for all open trades. When this flag is set, no modifications or cancellations can be made for open trades.
