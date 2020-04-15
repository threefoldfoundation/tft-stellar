# Address activation

Stellar addresses need to be activated and a minimal amount of XLM has to be kept on the account to be active.

To minimize the burdon for (Free)TFT holders, the threefoldfoundation will activate accounts for their users.

All very cool but the risk is real that others will abuse this service to activate non TFT related accounts or steal XLM from the foundation by repeatedly having accounts activated after which the Lumens are transferred away.

## During conversion

Activation during the conversion from the Rivine platform can be secured by requiring the Rivine address. Since a Rivine address can be deducted from a Stellar address, this means the requester has the secret and needs it's TFT to be transferred. A check is also built to see if this is an unused stellar addressin so  this activation is only done once so repeatedly activating and merging the account to another one is not possible.

## Starting balance

The starting balance for an account is 2.6 XLM, 2 minimum balance, 0.5 for the trustline and a little extra to pay for the trustline transaction fee.

## Implementation

The activation during conversion is built in to the [conversion service](../ThreeBotPackages/conversion-service/readme.md).
