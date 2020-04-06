# Testscripts for the transaction funding Service

# Testnet


Generate an unfunded TFT payment:
`./createunfundedpayment.py`


Generate an unfunded FreeTFT payment:
`./createunfundedpayment.py --asset="FreeTFT:GBLDUINEFYTF7XEE7YNWA3JQS4K2VD37YU7I2YAE7R5AHZDKQXSS2J6R"`


Generate an unfunded TFT from unknown issuer payment:
`./createunfundedpayment.py --asset="TFT:GAKONCKYJ7PRRKBZSWVPG3MURUNX4H44AB3CU2YGVKF2FD7KXJBB3XID"`


## Submit to funding service


```sh
curl -v -H "Content-Type: application/json" -d '{ "args": { "transaction": "" }}' "http://localhost/threefoldfoundation/transactionfunding_service/fund_transaction"
```
