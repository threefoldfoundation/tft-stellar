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
	var f *os.File
	if !dryRun {
		if fileExists(outputFilePath) {
			os.Remove(outputFilePath)
		}

		f, err = os.Create(outputFilePath)
		if err != nil {
			panic(err)
		}
	}

	addressesToExclude := ""
	if len(filesToExclude) != 0 {
		for _, file := range filesToExclude {
			data, err := ioutil.ReadFile(file)
			if err != nil {
				panic(err)
			}
			addressesToExclude += string(data)
		}
	}
	if !dryRun {
		fmt.Printf("%d addresses were found on the rexplorer \n", len(addresses))
	}
	excludedCount := 0
	if !dryRun {
		f.WriteString("#!/bin/bash\n")
	}
	for _, address := range addresses {
		// if the file path is passed only then check if it contains a block creator address
		containsBlockCreator := strings.Contains(addressesToExclude, address)
		if containsBlockCreator {
			excludedCount++
			continue
		}
		if dryRun {
			fmt.Printf("%s\n", address)
		}
		fstr := fmt.Sprintf("echo \"tfchainc wallet send transaction \\\"\\$(tfchainc wallet sign '$(tfchainc wallet sign \"$(tfchainc wallet authcoin authaddresses --deauth \"%s\")\")')\\\"\" >> lock_adressess.txt\n", address)
		f.WriteString(fstr)

	}
	if !dryRun {
		fmt.Printf("%d addresses were excluded \n \n", excludedCount)
		fmt.Printf("output written in %s \n", outputFilePath)
	}
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

type files []string

func (i *files) String() string {
	return "my string representation"
}

func (i *files) Set(value string) error {
	*i = append(*i, value)
	return nil
}

var (
	dbAddress      string
	dbSlot         int
	filesToExclude files
	dryRun         bool
)

func init() {
	flag.StringVar(&dbAddress, "redis-addr", ":6379", "(tcp) address of the redis db")
	flag.IntVar(&dbSlot, "redis-db", 0, "slot/index of the redis db")
	flag.Var(&filesToExclude, "exclude", "repeatable flag, points to a file which contains addresses to exclude")
	flag.BoolVar(&dryRun, "dryrun", false, "Outputs the addresses that would be locked instead of creating a script")
}
