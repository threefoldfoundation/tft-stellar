## Locking addresses on tfchain

### Requirements

- Rexplorer: [https://github.com/threefoldfoundation/rexplorer](https://github.com/threefoldfoundation/rexplorer)
- Redis: to store addresses

### Usage

```golang
go build ./lock-addresses.go
go run ./lock-addresses.go [--redis-addr] [--redis-db]
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

```bash
go run verify.go
```