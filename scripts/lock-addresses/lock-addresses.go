package main

import (
	"flag"
	"fmt"
	"os"

	"github.com/gomodule/redigo/redis"
)

func main() {
	flag.Parse()

	args := flag.Args()
	if len(args) != 0 {
		panic("usage: " + os.Args[0])
	}

	conn, err := redis.Dial("tcp", dbAddress, redis.DialDatabase(dbSlot))
	if err != nil {
		panic(err)
	}

	addresses, err := redis.Strings(conn.Do("SMEMBERS", "addresses"))
	if err != nil {
		if err != redis.ErrNil {
			panic("failed to get addresses " + err.Error())
		}
		addresses = nil
	}
	if len(addresses) == 0 {
		panic("no addresses found")
	}

	outputFilePath := "lock-all.sh"

	if fileExists(outputFilePath) {
		os.Remove(outputFilePath)
	}

	f, err := os.Create(outputFilePath)
	if err != nil {
		panic(err)
	}

	f.WriteString("#!/bin/bash\n")
	for _, address := range addresses {
		fstr := fmt.Sprintf("echo \"tfchainc wallet send transaction \\\"\\$(tfchainc wallet sign '$(tfchainc wallet sign \"$(tfchainc wallet authcoin authaddresses --deauth \"%s\")\")')\\\"\" >> lock_adressess.txt\n", address)
		f.WriteString(fstr)
	}
	fmt.Printf("Bash file with all addresses written in: %s \n", outputFilePath)
}

// fileExists checks if a file exists and is not a directory before we
// try using it to prevent further errors.
func fileExists(filename string) bool {
	info, err := os.Stat(filename)
	if os.IsNotExist(err) {
		return false
	}
	return !info.IsDir()
}

var (
	dbAddress string
	dbSlot    int
)

func init() {
	flag.StringVar(&dbAddress, "redis-addr", ":6379", "(tcp) address of the redis db")
	flag.IntVar(&dbSlot, "redis-db", 0, "slot/index of the redis db")
}
