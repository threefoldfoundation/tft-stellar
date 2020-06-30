# TFTA selling during 2020

## Concept

TFTA is 100% the same as a TFT, this is just a technical detail for migrating all TFT's from one blockchain to the other and at the end of 2020 all TFTA will become TFT. Using 2 currency names TFT & TFTA allows to provide some price protection during 2020 which is to the benefit of the full ThreeFold community.

Exchanges only have TFT markets, making selling of TFTA very hard.

To facilitate people that want to sell TFTA, a trading service will be made available.
People can give TFTA to the trading service which sells it as TFT.
After the sell, the Resulting XLM or other currency is given back to the user.

There is a [Functional description](https://wiki.threefold.io/#/threefold_marketmaker_bot) that describes the high level process for people wanting to sell.

### Minimal prices during 2020

| Month | USD floor |
|-------|-----------|
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

A website (or a chatflow) protected by a 3bot login to manage your trades.

### BCDB Schemas

```toml
@url = threefoldfoundation.tfta_to_tft__service.order

threebotid** = (S)
trade_id**= (S)

stellaraddress** = (S)
original_amount = (F)
payment_transaction_id = (S)
payment_received = (T)
wanted_asset = "XLM" (S)
receiving_address = (S) 
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

## Trade offer creation

A logged in user can create a trade offer by supplying the amount of TFTA and the wanted price in USD.

A list of open trade offers grouped by price with the total amount next to it is also shown to have the user make its price decision.

Next to the orderbook, the floor amounts are also shown.

A user can only have 1 open trade offer.

### Transfer requests

Since there seems no fits all solution for payment requests that [all wallets support](https://github.com/threefoldfoundation/tft-stellar/issues/173). A qr code supported by the 3bot wallet will be shown together with the destination address and the trade id that needs to be supplied in the memo text field.

A messsage indicating that "If your wallet does not support the qr code, be sure to correctly copy the address and the memo text or your trade can not be accepted." must be shown to make this clear to the user.

### User initiated trade Cancellation

A user can choose to cancel the outstanding trade, the remaining amount will be transferred back to the address it originates from, this address should be shown to the user after which a proceed/cancel option should be shown.
When the `distribution_ongoing` flag is set, no cancellations can be made for the open trade.

### Forced trade cancellation

In the event of the requested USD price set at trade creation dropping below the floor because of passing on to a next month, the tyrade is forcefully cancellled and the remaining amount of TFTA is sent back to address is was received from.

## Selling bot

In a first phase the selling bot places its orders in TFT to XLM  on the Stellar DEX.
The selling price in XLM is derived from  the XLM USD price on [Kraken](https://www.kraken.com), where the middle of the spread is taken as a reference.

It receives XLM In return which is distributed back to the users.

Other exchanges and cryptocurrencies can be added in later phases.
- Check [kelp](https://github.com/stellar/kelp) and [selling strategy](https://github.com/stellar/kelp/blob/master/plugins/sellStrategy.go)

## Distribution

When the selling bot sold 20k of TFT or depleted the trade offfers for a specific price, the distribution processs is started.

The received amount is evenly distributed amongst the open trade offers, regardless of the amount of the trade offer,unless it is less than the distribution share off course, in which case the difference is divided amongst the rest.

The `distribution_ongoing` flag is set for all open trades. When this flag is set, no modifications or cancellations can be made for open trades.

### Price fluctuations

Since cryptocurrencyprices vary against USD,it might be that the received amount of XLM or other cryptocurrency might no longer correspond to UsD price for TFTA set at the  the trade offer creation.

## Problems

- The 3bot connect wallet only supports TFT, TFTA and FreeTFT, no way to manage  the XLM for example. The stellar secret of the 3bot connect wallet can be imported in another wallet like solar to send the received XLM to an exchange for example.
Another address can also be supplied in the trade offer to prevent sharing this secret between wallets.

- Bad user experience, especially for 3bot connect users.
- No notifications are included in this spec, can be addded later.
