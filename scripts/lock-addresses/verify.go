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

	data, err := ioutil.ReadFile(filePath)
	if err != nil {
		panic(err)
	}
	file := string(data)

	for _, address := range addresses {
		for _, excludedAddress := range excludedAddresses {
			if address != excludedAddress && address != "000000000000000000000000000000000000000000000000000000000000000000000000000000" {
				contains := strings.Contains(file, address)
				if !contains {
					errorStr := fmt.Sprintf("Address %s does not exist in %s", address, filePath)
					panic(errorStr)
				}
			}
		}
	}
	fmt.Printf("File %s is verified and ready to be submitted to the network. \n", filePath)
}

var (
	dbAddress          string
	dbSlot             int
	filePath           string
	addressesToExclude string
)

func init() {
	flag.StringVar(&dbAddress, "redis-addr", ":6379", "(tcp) address of the redis db")
	flag.IntVar(&dbSlot, "redis-db", 0, "slot/index of the redis db")
	flag.StringVar(&filePath, "file", "./lock_adressess.txt", "file to verify")
	flag.StringVar(&addressesToExclude, "exclude", "", "addresses to exclude seperated by comma")
}
