# TFTA to TFT

## Who and how much

From a functional perspective, a conversion strategy needs to be defined, in other words, who can convert how much.

There is a [Functional description](https://wiki.threefold.io/#/threefold_marketmaker_bot) that describes the high level process.

### Problems with Functional description

> Every TFTA holder can place sell orders on the digitized market maker bot, only 1 order can be open at the same time per TFTA holder.

How do you define a single TFTA holder? Everyone can create as many accounts as they want.

## Basic Principle

The total amount of TFTA+TFT can not change. This means that newly issued TFT requires the same amount of TFTA to be destroyed.

## First thought options

### The user sends to the TFTA issuer and gets TFT back

This immediately destroys the TFTA and creates a transaction id in the process.

A service collects the destroyed amounts, the sending addresses and the transaction id's.
Using this information, new TFT are issued  to the sending addresses for these amounts with the transaction id the memo_hash field to proove the relationship between the destruction and the issuance.

#### Side effects

Since 0.1 TFTA is added as a transaction fee when using the 3bot wallet, 0.1 TFTA less then the wallet balance can be sent from the wallet or the transaction will fail.

Also, 0.1 TFT less then the allowed amount will be issued then. 

If this poses a problem, we can send 0.1 TFT from a different wallet. We recuperate it anyway since the transaction funding service received the 0.1 TFTA transaction fee. 

### Atomic swap

- The wallet needs to support this process
- Requires a TFT pool that destroys and reissues afterwards

### Stellar DEX

People use the default Stellar Dex to place sell orders

## Options given the functional description 

According to the [Functional description](https://wiki.threefold.io/#/threefold_marketmaker_bot), when the market maker bot reaches it's treshold:
> sales done gets distributed evenly over the sell orders in the order book

### Stellar DEX

On the Dex, matching is done by the protocol, "For offers placed at the same price, the older offer is filled before the newer one". This means we can not choose which orders to fulfill and distribute evenly.

### Atomic swap

- It's an all or nothing, the entire swap gets executed or not at all.
- Timeouts are set at the creation of the swap
- price is set against the other cryptocurrency at the creation of the swap

### The user sends to the TFTA issuer and gets TFT back

**Cons:**

- No direct price setting ( can be done through the memofield)
- Cancelling the order needs to be requested at a seperate service

**Pros:**

- The TFTA is known to be availanle
- The trading service has immediate access to the funds in TFT
- Easy to distribute fractionally and evenly

### Using Escrow accounts

**Cons:**

- No direct price setting ( can be done through the memofield)
- Need to create and manage escrow accounts
- More difficult to explain the process

**Pros:**

- Easy to distribute fractionally and evenly
- The user can withdraw TFTA from the escrow account itself, cancelling the order in this way

### Send TFTA to the trader bot

**Cons:**

- No direct price setting ( can be done through the memofield)
- Very centralized
- Cancelling the order needs to be done through a signed service request

**Pros:**

- Simple
