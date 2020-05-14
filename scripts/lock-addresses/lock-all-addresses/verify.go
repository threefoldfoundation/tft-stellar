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

	var excludedAddresses []string
	if addressesToExclude != "" {
		excludedAddresses = strings.Split(addressesToExclude, ",")
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

	data, err := ioutil.ReadFile(filePath)
	if err != nil {
		panic(err)
	}
	file := string(data)

	excludedBlockStakeAddresses := ""
	if excludedBlockcreators != "" {
		blockCreatorsData, err := ioutil.ReadFile(excludedBlockcreators)
		if err != nil {
			fmt.Println(err)
			panic(err)
		}
		excludedBlockStakeAddresses = string(blockCreatorsData)
	}
	excludedBlockcreatorAddresses := strings.Split(excludedBlockStakeAddresses, "\n")

	if excludedBlockStakeAddresses != "" {
		excludedAddresses = append(excludedAddresses, excludedBlockcreatorAddresses...)
	}
	// exclude free for all address
	excludedAddresses = append(excludedAddresses, "000000000000000000000000000000000000000000000000000000000000000000000000000000")

	for _, address := range addresses {
		for _, excludedAddress := range excludedAddresses {
			if address == excludedAddress {
				if strings.Contains(file, address) {
					fmt.Printf("excluded addr %s contained \n", excludedAddress)
				}
			}
		}
	}
	fmt.Printf("File %s is verified and ready to be submitted to the network. \n", filePath)
}

var (
	dbAddress             string
	dbSlot                int
	filePath              string
	addressesToExclude    string
	excludedBlockcreators string
)

func init() {
	flag.StringVar(&dbAddress, "redis-addr", ":6379", "(tcp) address of the redis db")
	flag.IntVar(&dbSlot, "redis-db", 0, "slot/index of the redis db")
	flag.StringVar(&filePath, "file", "./lock_adressess.txt", "file to verify")
	flag.StringVar(&addressesToExclude, "exclude", "", "addresses to exclude seperated by comma")
	flag.StringVar(&excludedBlockcreators, "exclude-blockcreators", "", "blokcreator addresses to exclude")
}
