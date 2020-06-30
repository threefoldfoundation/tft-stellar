# TFTA selling during 2020

## Concept

TFTA is 100% the same as a TFT, this is just a technical detail for migrating all TFT's from one blockchain to the other and at the end of 2020 all TFTA will become TFT. Using 2 currency names TFT & TFTA allows to provide some price protection during 2020 which is to the benefit of the full ThreeFold community.

Exchanges only have TFT markets, making selling of TFTA very hard.

To facilitate people that want to sell TFTA, a trading service will be made available.
People can give TFTA to the trading service which sells it as TFT.
After the sell, the Resulting XLM or other currency is given back to the user.

There is a [Functional description](https://wiki.threefold.io/#/threefold_marketmaker_bot) that describes the high level process for people wanting to sell.

### Minimal prices during 2020

| Month | USD |
|-------|-----|
|July 2020 | 0.15606 |
|August 2020 | 0.1591812 |
|September 2020 | 0.162364824 |
|October 2020 | 0.1656121205 |
|November 2020 | 0.1689243629 |
|December 2020 | 0.1723028501 |

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
wanted_asset = "TFT:GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47" (S)
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
When the `distribution_ongoing` flag is set, no cancellations can be made for the open trade.

## Selling bot

The selling bot places it's orders in TFT on the Stellar DEX. It receives XLM In return.

## Distribution

The `distribution_ongoing` flag is set for all open trades. When this flag is set, no modifications or cancellations can be made for open trades.

Users by default get XLM back.

## Problems

- Bad user experience, especially for 3bot connect users.
- The 3bot connect wallet only supports TFT, TFTA and FreeTFT, no way to manage  the XLM for example. The stellar secret of the 3bot connect wallet can be imported in another wallet like solar to send the received XLM to an exchange for example.
Another address can also be supplied in the trade offer to prevent sharing this secret between wallets.
