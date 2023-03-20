# Unvesting tool

This tool has 2 main functionalities:

- Signing unvesting transactions
- Aggregating unvestingen transactions signatures

## Build

```
go build .
```

## Signing transactions

Given a file of unvesting transactions, these can be signed as:

```
./unvesting sign --secret YOUR_STELLAR_SECRET --path ./unvesting_tx.text --out ./signatures.txt
```

This will sign the transactions in `./unvesting_tx.text` and will output the signatures in `./signatures.txt`

## Aggregating signatures

Will only be possible if 5 guardians have signed the transactions.

If you wish to aggregate the signatures given a directory of files that contain signatures of the guardians:

```
./unvesting aggregate --path unvesting_tx.text --dir in/ --out final.txt
```

This will scan all the files in `in/` and output the final transactions as XDR in `final.txt`
