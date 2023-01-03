# Testnet liquidity pools

## Purpose

- Provide a way for people to acquire testnet tokens without setting up and maintaing faucets. One can simply acquire testnet tokens through the Stellar dex.
- Provide liquidity to test swapping supported assets in the wallet through the Stellar dex.

## Pools

- XLM/TFT
- XLM/USDC
- USDC/TFT

## Create liquidity pools

in the js-ng shell create an account to deposit tokens in the liquidity pools:

```python
j.clients.stellar.new("testnetdeposit",network="TEST")
j.clients.stellar.testnetdeposit.activate_through_friendbot()
j.clients.stellar.testnetdeposit.add_known_trustline("TFT")
j.clients.stellar.testnetdeposit.add_trustline("USDC","GAHHZJT5OIK6HXDXLCSRDTTNPE52CMXFWW6YQXCBMHW2HUI6D365HPOO")
```

fund it with 1M testnet TFT and 100k testnet USDC.

Add liquidity:

```python
./lp.py XLM/TFT <testnetdeposit secret>
./lp.py XLM/USDC <testnetdeposit secret>
./lp.py TFT/USDC <testnetdeposit secret>
```
