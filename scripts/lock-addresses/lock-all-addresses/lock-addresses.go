package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"strings"

	"github.com/gomodule/redigo/redis"
)

func main() {
	flag.Parse()

	args := flag.Args()
	if len(args) != 0 {
		panic("usage: " + os.Args[0])
	}

	excludedAddresses := strings.Split(addressesToExclude, ",")

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

	excludedBlockStakeAddresses := ""
	if excludedBlockcreators != "" {
		blockCreatorsData, err := ioutil.ReadFile(excludedBlockcreators)
		if err != nil {
			fmt.Println(err)
			panic(err)
		}
		excludedBlockStakeAddresses = string(blockCreatorsData)
	}
	fmt.Println(len(addresses))

	f.WriteString("#!/bin/bash\n")
	for _, address := range addresses {
		for _, excludedAddress := range excludedAddresses {
			if address != excludedAddress {
				// if the file path is passed only then check if it contains a block creator address
				containsBlockCreator := strings.Contains(excludedBlockStakeAddresses, address)
				if !containsBlockCreator {
					fstr := fmt.Sprintf("echo \"tfchainc wallet send transaction \\\"\\$(tfchainc wallet sign '$(tfchainc wallet sign \"$(tfchainc wallet authcoin authaddresses --deauth \"%s\")\")')\\\"\" >> lock_adressess.txt\n", address)
					f.WriteString(fstr)
				}
			}
		}
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
	dbAddress             string
	dbSlot                int
	addressesToExclude    string
	excludedBlockcreators string
)

func init() {
	flag.StringVar(&dbAddress, "redis-addr", ":6379", "(tcp) address of the redis db")
	flag.IntVar(&dbSlot, "redis-db", 0, "slot/index of the redis db")
	flag.StringVar(&addressesToExclude, "exclude", "", "addresses to exclude seperated by comma")
	flag.StringVar(&excludedBlockcreators, "exclude-blockcreators", "", "blokcreator addresses to exclude")
}
