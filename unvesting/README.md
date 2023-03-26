# Unvesting tool

This tool has 2 main functionalities:

- Signing unvesting transactions
- Aggregating unvestingen transactions signatures

## Installations

- Instal [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- Install [Go](https://go.dev/doc/install)

## Build

```sh
git clone https://github.com/threefoldfoundation/tft-stellar
cd tft-stellar/unvesting
go build .
```

## Signing transactions

If the file with unvesting transactions is named `unvesting_transactions.txt` and in the same folder as the unvesting executable, these can be signed as:

./unvesting sign --secret YOUR_STELLAR_SECRET

If the file with unvesting transactions is localted somewhere else, a `--path <path/filename>` option can be added.

**Make sure to have your secret key before you use this command.**

This will sign the transactions in `./unvesting_transactions.txt` and will output the signatures in `signed_unvesting_transactions_YOURSTELLARADDRESS.txt`

## Aggregating signatures

Will only be possible if 5 guardians have signed the transactions.

If you wish to aggregate the signatures given a directory of files that contain signatures of the guardians:

```sh
./unvesting aggregate --path unvesting_transactions.txt --dir in/
```

This will scan all the files in `in/` and output the final transactions as XDR in `signed_unvesting_transactions.txt`
