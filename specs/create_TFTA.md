# Create TFTA on Stellar

The TFTs on TFchain need to be converted into Stellar, through the conversion service and used by 3Bot Connect app. These tokens on Stellar will be called TFTA (the '1.0 grid tokens'). 
These TFTAs can then be converted into Stellar TFT (called also '2.0 Grid tokens') tokens through 2 possible paths : 

## Exchange through trade 1:1
Exchange service TFTA to TFT (1:1, so 1 TFTA becomes 1 TFT), under conditions to avoid dumping of tokens. Idea is that TFTA can only be converted after July 1, if the price of the token is higher than 0.15USD + price increase of x% per month. 

## Pay capacity with TFTAs
A user can reserve capacity using TFTA in the same way as he can use TFTs. The TFTA will arrive on an escrow account, that will split up the amount over the different farmers that rent out the capacity. 
In the end, farmers will receive TFTs on his wallet, so a 1:1 conversion needs to happen on the escrow account. 
As the escrow account is a central account in the payment reservation process and likely to be targeted by hackers, there is a request to limit as much as possible the tokens residing on an account. 

## To do

- Define asset and issuer for TFTA on Stellar testnet
- Define asset and issuer for TFTA on Stellar mainnet
- Replace TFT by TFTA in conversion service (used by 3Bot connect app)
- Allow a mechanism to convert TFTA to TFT on escrow account when capacity payment is done in TFTA

## Digitized market maker
(to be confirmed whether this info has evolved)

- Starting July 1, TFTA can be sold as TFT on Stellar using a digitized market maker
- Until end of 2020 TFTA can only be sold if price is higher than the min TFT price compared to USD
- Min TFT price by market maker is USD 0.15 starting april 30, going up 4% per month compared to the gold price
- End 2020, all TFTA get converted into TFT at same conditions is on TFTA chain (same lockup periods), which means TFTA stops to exist. 
- Every TFTA holder can place sell orders on the digitized market maker bot, only 1 bot can be open at the same time. 
- The digitized market maker bot will sell per USD 20k unto the market and sales done get distributed evenly over the sell orders in the order book. 
- As long as price is higher than the minimum price the digitized market maker bot will keep on selling if orderbook is not empty.
- TFTA holders can set the sales price (min sales price) or they can sell at market. 
- The sales orders are always done versus XLM which is the native Stellar currency which will also sell to other currencies like BTC, ETH, ... up to 6 levels deep. 
   - this means if someone wants to buy TFT for BTC, it will still work, Stellar payments network will convert to XLM and then to TFT. 
