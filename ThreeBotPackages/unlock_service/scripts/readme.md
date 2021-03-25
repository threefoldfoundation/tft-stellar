# Unlock service scripts

A Python environment as described in the [main scripts readme](../../../scripts/readme.md) is required to run these scripts.

The export script fetches the used unlocktransactions from the unlock service for TFT and TFTA using the Stellar network as input. No special setup is needed to acquire access to the unlockservice's resources. they are exported over the public api.

## Examples

Export the testnet transactions:

```sh
./export.py --network=test > testnetdata
```
