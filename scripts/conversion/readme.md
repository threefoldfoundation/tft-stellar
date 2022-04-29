# Scripts to see the status of the conversion

## List locked accounts

```sh
./lockedaddresses.py > deauthorizations.txt
```

This will create a file with a `transactionid tfchainaddress` combination per line.

## List deauthorized balances

```sh
./tfchainbalances.py
```

This will create a file called `deauthorizedbalances.txt` with a `address Free: amount Locked: amount` combination per line.

## List balances before conversion for a list of tfchain addresses

```sh
./tfchainaddresses.py
```

## List issued tokens

```sh
./issued.py > issued.txt
```

This will create a file with a `memo amount tokencode destination transactionid` combination per line.

## Check the status for all migrations

This requires an up to date deauthorizations.txt and issued.txt file.

```sh
./check.py
```

## check the status for a single migration

This requires an up to date deauthorizations.txt and issued.txt file.

```sh
./checksingle.py <tfchainadress>
```
