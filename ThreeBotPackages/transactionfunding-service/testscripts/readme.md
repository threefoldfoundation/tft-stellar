# Testscripts for the transaction funding Service

## Testnet

Generate an unfunded TFT payment:
`./createunfundedpayment.py`

Generate an unfunded TFTA payment:

`./createunfundedpayment.py --asset="TFTA:GB55A4RR4G2MIORJTQA4L6FENZU7K4W7ATGY6YOT2CW47M5SZYGYKSCT"`

Generate an unfunded FreeTFT payment:
`./createunfundedpayment.py --asset="FreeTFT:GBLDUINEFYTF7XEE7YNWA3JQS4K2VD37YU7I2YAE7R5AHZDKQXSS2J6R"`

Generate an unfunded TFT from unknown issuer payment:
`./createunfundedpayment.py --asset="TFT:GAKONCKYJ7PRRKBZSWVPG3MURUNX4H44AB3CU2YGVKF2FD7KXJBB3XID"`

## Submit to funding service

localhost:

```sh
curl -v -H "Content-Type: application/json" -d '{ "args": { "transaction": "" }}' "http://localhost:7000/threefoldfoundation/transactionfunding_service/fund_transaction"
```

testnet:

```sh
curl -v -H "Content-Type: application/json" -d '{ "args": { "transaction": "" }}' "https://testnet.threefold.io/threefoldfoundation/transactionfunding_service/fund_transaction"
```
