# Initial TFTA to TFT conversion

## Concept

The total amount of TFTA+TFT can not change. This means that newly issued TFT requires the same amount of TFTA to be destroyed.

There is a [Functional description](https://wiki.threefold.io/#/threefold_marketmaker_bot) that describes the high level process for people wanting to convert.

### Single TFTA holder

From the functional description:
> Every TFTA holder can place sell orders on the digitized market maker bot, only 1 order can be open at the same time per TFTA holder.

How do you define a single TFTA holder? Everyone can create as many Stellar accounts as they want.

Currently the best option is to link the trade orders to a 3bot connect user.
