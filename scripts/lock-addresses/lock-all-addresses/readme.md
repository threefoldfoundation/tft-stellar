## Locking addresses on tfchain

### Requirements

- Rexplorer: [https://github.com/threefoldfoundation/rexplorer](https://github.com/threefoldfoundation/rexplorer)
- Redis: to store addresses (if you wish to connect to the production rexplorer that is setup you need a wireguard to the office!)
- Synced consensus db, placed in the root of this folder with the name: `consensus.db`

### Usage

If you wish to exclude the blockcreator addresses, execute following first:

```golang
go run ./blockcreators.go
```
This will create an output file `blockcreators.txt` with all the blockcreator addresses inside. It also prints the amount of blockstakes. 
If the amount is not 500 you probably don't have a synced consensusdb. 

Now if you want to exclude them from the locking script:

`lock-addresses.go` has a repeatable flag which can point to a file that holds addresses to exclude.

```golang
go run ./lock-addresses.go [--redis-addr] [--redis-db] [--exclude blockcreators.txt] [--exclude file.txt] ...
```

for production

```sh
go run lock-addresses.go --exclude "../../../config/public/conversion/foundation.txt" --exclude "../../../config/public/conversion/exclude.txt"
```

This will create an output file `lock-all.sh` and prepare an authcoin transaction for each address that is fetched from the redis db. 

Executing this file can be done as:

```bash
chmod +x lock-all.sh
./lock-all.sh
```

This script will create another file called `lock_addresses.txt`, this file is to be passed to the other person that need to sign off on these transactions.

How to sign off on these transactions with this file: 
```bash 
bash lock_addresses.txt
```

### Verfiying output of lock-all.sh

Verifying the output with or without the excluded blockcreator addresses:

`verify.go` has a repeatable flag which can point to a file that holds addresses to exclude.

```bash
go run verify.go [[--redis-addr] [--redis-db] [--exclude blockcreators.txt] [--exclude file.txt] ...
```