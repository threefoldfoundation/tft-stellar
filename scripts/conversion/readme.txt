# Scripts to see the status of the conversion

## List locked accounts

```sh
./lockedaddresses.py > deauthorizations.txt
```

This will create a file with a `transactionid tfchainaddress` combination per line.

## List issued tokens

```sh
./issued.py > issued.txt
```

This will create a file with a `memo amount tokencode destination transactionid` combination per line.

## Check the status

```sh
./check.py
```
