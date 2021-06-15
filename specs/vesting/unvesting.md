# Unvesting

## Price determination

The price for a month is determined using [stellar.expert](https://stellar.expert) data.
A [script](../scrips/info/stellarexpert/tftprice.py) to determine the weighted average price for a month is available so everyone can check.

## Ckecking vesting accounts

Even though everyone can check for vesting accounts on the Stellar network and calculate  the free and vested amounts themselves, a service is available to make this process easier: the vesting_accounts endpoint on the [vesting service](../../ThreeBotPackages/vesting_service/readme.md).

It returns the vesting accounts for an owner addresss and for each vesting account the total, free and vested tft blances.  


