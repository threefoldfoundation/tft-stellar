# Conversion of TFT from tfchain to the stellar platform

[Rivine addresses can not be converted to Stellar addresses without knowing the private key](https://github.com/threefoldtech/rivine/blob/master/research/stellar/examples/accounts/readme.md#rivine-key-conversion).
The other way is possible though but it does mean that a script to transfer all funds from tfchain to the Stellar platform is not possible.

A possible solution is to provide a service to migrate the funds on demand, initiated by the user's wallet.

## Lock an account on Tfchain

The new release of Tfchain enables deathorization of an address. When we migrate funds from Tfchain to Stellar we should
deactivate the address on Tfchain. This will disable all functionality for this address on Tfchain.

## Issue the credit on the Stellar network

When the Tfchain address is deathorized we should issue the same amount of tokens (locked and unlocked) to a new address on
the Stellar network. 

The conversion rate is 1:1, so for every token (locked and unlocked) the user will receive 1 token on their Stellar address.

## Create a script

To migrate funds from Tfchain to Stellar we should create an automated script which will hold and distribute all the Stellar tokens (TFT-Stellar).
If we wish to activate this script this should be signed by a multisignature wallet.

This script should atleast do following:
* Get the balance of an address on the Tfchain blockchain
* Be able to create Stellar keypairs
* Swap Tfchain TFT's 1:1 for Stellar TFT's (locked and unlocked tokens)
* Deauthorize (lock) the Tfchain address on the Tfchain blockchain

## Proposed swap methods

### Web swap 

Should we make a portal where the users of Tfchain can swap their tokens for Stellar tokens if they wish?

* How are we going to communicate this?
* In this case, how will our wallets support this? There will be users that have Tfchain TFT balance and Stellar TFT balance.

![alt text](./conversion-web.png "Conversion flow web")

### Mobile swap 

Another option might be to perform this swap in the Threebot mobile app without asking permission from the user (enforced swap).

![alt text](./conversion-mobile.png "Conversion mobile flow")

 
### To be defined

* Which swap method will we use?
* Can we scan all addressess on the Tfchain blockchain and for each address convert to Stellar tokens? 
    * How can the user get access to this newly created Stellar account?
* Should we disable the Tfchain network when all tokens are swapped? How can we verify that every address is swapped?
