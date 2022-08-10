# L2 validator application on Stellar

Gep in which this is accepted: [GEP suggestion to wait with deployment of validators L2](https://forum.threefold.io/t/gep-suggestion-to-wait-with-deployment-of-validators-l2-closed/3164)

> Lock the current validator application on the current money blockchain (Stellar) to allow the reservation of validators and secure their position.

## Requirements

1. A way to mark a specific amount of TFT for an L2 validator application on the Stellar chain.
2. The TFT's marked can be reclaimed by the applicant itself.
3. It should be easy way to list the applicants and the TFT amounts.
4. It should not be possible to accidentially spend the TFT used for a reservation.

## Solution on the Stellar level

[Claimable balances](https://developers.stellar.org/docs/glossary/claimable-balance/) are a core Stellar feature that can be used for this. The [Aquarius project](https://aqua.network) also uses this to register votes with the associated amount of locked Aqua tokens.

A participation claimable balance has 2 destination Stellar accounts:

- `GATFL2VALIDATORAPPLICATIONAAAAAAAAAAAAAAAAAAAAAAAAAAA4TT` to indicate it is an application for an L2 Validator. Even though it is obvious that no-one has the private key for this address, the predicate is is set to `not:{}`
- The participant itself without restrictions.

### List the applications

Horizon provides [an api to list claimable balances](https://developers.stellar.org/api/resources/claimablebalances/list/). By providing the `GATFL2VALIDATORAPPLICATIONAAAAAAAAAAAAAAAAAAAAAAAAAAA4TT` address as claimant parameter and TFT as asset parameter, we only get the applications together with the applicant address and the TFT amount.  

## Addresses to human readable whoami

Adresses alone do not show to the public who someone is ( to support the validatorship for example).

In the claimable balance creation, a 28 character text can be supplied but that's not very long.

A better option is that on the website where the validator applications are visualized a participant can add a whoami and the website stores it itself. Verification of the supplied information can be done by having the participant sign the text.

## Required XLM

A claimable balance in this way requires the partipant to have 1 free XLM that will be locked during the lifetime of the claimable balance.

If the account does not have 1 free XLM, it can be acquired by performing a swap, technically, a [Path Payment Strict Receive](https://developers.stellar.org/api/resources/operations/object/path-payment-strict-receive/). The optimal path can be  [requested at an horizon server](https://developers.stellar.org/api/aggregations/paths/). There is a [working go example to swap TFT to 1 XLM available](./swap).

The transaction fees can be supported by giving 0.1 TFT to the feebump service as it already works now for other transactions.

## User experience

A seperate website or panel with 2 functionalities:

- List the L2 validator applications
- Register/modify your validator application

### Managing a validator application

An applicant signs in using the Threefold connect app.

#### New application

when creating a new validator application, the applicant selects it's account if there are multiple and fills in the amount of TFT for the application.

When confirming, the prepared transaction is sent to the applicant's wallet where it can be signed.

#### Add/modify publicly visible text( whoami)

As explained above, the participant can enter a whoami on the website. Since the participant already logged in, signing the text might not be necessary but it would provide an extra layer of security.

## Remarks

Address `GATFL2VALIDATORAPPLICATIONAAAAAAAAAAAAAAAAAAAAAAAAAAA4TT` is constructed to be a valid Stellar adress using <./destinationaddress>  

## TODO

Spec supporting someone else's validator appication.
