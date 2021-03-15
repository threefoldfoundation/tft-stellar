# Testscripts for the transaction funding Service

## Unsigned payments

### Testnet

Generate an unsigned TFT payment:
`./createunfundedpayment.py`

Generate an unsigned TFTA payment:

`./createunfundedpayment.py --asset="TFTA:GB55A4RR4G2MIORJTQA4L6FENZU7K4W7ATGY6YOT2CW47M5SZYGYKSCT"`

Generate an unsigned TFT from unknown issuer payment:
`./createunfundedpayment.py --asset="TFT:GAKONCKYJ7PRRKBZSWVPG3MURUNX4H44AB3CU2YGVKF2FD7KXJBB3XID"`

## Signed payments

Signed payments already include a fee payment operation in the asset that one is transferring

## Submit to thefunding service

localhost:

```sh
curl -v -H "Content-Type: application/json" -d '{ "args": { "transaction": "" }}' "http://localhost:7000/threefoldfoundation/transactionfunding_service/fund_transaction"
```

testnet:

```sh
curl -v -H "Content-Type: application/json" -d '{ "args": { "transaction": "" }}' "https://testnet.threefold.io/threefoldfoundation/transactionfunding_service/fund_transaction"
```

## Production

Generate an unfunded TFT payment:

`./createunfundedpayment.py --asset="TFT:GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47" --network=public`

```sh
curl -v -H "Content-Type: application/json" -d '{ "args": { "transaction": "" }}' "https://tokenservices.threefold.io/threefoldfoundation/transactionfunding_service/fund_transaction"
```
