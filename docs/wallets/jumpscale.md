# Jumpscale wallet

[Jumpscale Wallet](https://github.com/threefoldtech/jumpscaleX_libs/tree/development/JumpscaleLibs/clients/stellar)

## tricks

Export all your wallets to a script to recreate them in another environment:

```python
walletnames=j.clients.stellar._children_names_get()
for walletname in walletnames:
    print("j.clients.stellar.new('"+walletname+"',network='"+str(j.clients.stellar.get(walletname).network)+"',secret='"+str(j.clients.stellar.get(walletname).secret)+"')")
```
