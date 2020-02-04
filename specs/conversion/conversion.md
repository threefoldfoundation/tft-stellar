# Conversion of TFT from tfchain to the stellar platform

While new users can be placed on the Stellar platform directly, existing ones need to have their funds migrated.

[Rivine addresses can not be converted to Stellar addresses without knowing the private key](https://github.com/threefoldtech/rivine/blob/master/research/stellar/examples/accounts/readme.md#rivine-key-conversion).
The other way is possible though but it does mean that a script to transfer all funds from tfchain to the Stellar platform is not possible.

A possible solution is to provide a service to migrate the funds on demand, initiated by the user's wallet.

Before the conversion, all addresses on tfchain will be locked by unauthorizing them. [A seperate document explains why and the details](./locking.md).

## Flow

![Conversion sequence diagram](./Conversionflow.png)
