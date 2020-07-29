# Statistics about TFT/TFTA/FreeTFT

## Requirements

- [js-sdk](https://github.com/threefoldtech/js-sdk)

## Run it standalone

From the js-sdk shell (`poetry shell` in the js-sdk folder),navigate to this folder and execute

`./stats.py`

By default the stats for TFT are shown but the ones for TFTA and FreeTFT  can also be shown by passing the tokencode as an argument.

For example the stats for TFTA:

`./stats.py TFTA`

## Lock time information

When passing the `--detailed` flag, the locked amounts per locktime are also calculated.
