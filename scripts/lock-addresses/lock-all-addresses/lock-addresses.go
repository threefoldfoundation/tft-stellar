package main

import (
	"errors"
	"flag"
	"fmt"
	"os"
	"strings"
	"time"

	bolt "github.com/coreos/bbolt"
	"github.com/gomodule/redigo/redis"
	"github.com/threefoldtech/rivine/pkg/encoding/siabin"
	"github.com/threefoldtech/rivine/types"
)

// Metadata contains the header and version of the data being stored.
type Metadata struct {
	Header, Version string
}

// BoltDatabase is a persist-level wrapper for the bolt database, providing
// extra information such as a version number.
type BoltDatabase struct {
	Metadata
	*bolt.DB
}

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

	db, err := LoadCsDB()
	if err != nil {
		panic(err)
	}

	excludedBlockStakeAddress, err := db.GetBlockStakeAddresses()
	if err != nil {
		panic(err)
	}

	f.WriteString("#!/bin/bash\n")
	for _, address := range addresses {
		for _, excludedAddress := range excludedAddresses {
			for _, excludedBlockStakeAddress := range excludedBlockStakeAddress {
				if address != excludedBlockStakeAddress.String() {
					if address != excludedAddress {
						fstr := fmt.Sprintf("echo \"tfchainc wallet send transaction \\\"\\$(tfchainc wallet sign '$(tfchainc wallet sign \"$(tfchainc wallet authcoin authaddresses --deauth \"%s\")\")')\\\"\" >> lock_adressess.txt\n", address)
						f.WriteString(fstr)
					}
				}
			}
		}
	}
	fmt.Printf("output written in %s \n", outputFilePath)
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
	dbAddress          string
	dbSlot             int
	addressesToExclude string
)

func init() {
	flag.StringVar(&dbAddress, "redis-addr", ":6379", "(tcp) address of the redis db")
	flag.IntVar(&dbSlot, "redis-db", 0, "slot/index of the redis db")
	flag.StringVar(&addressesToExclude, "exclude", "", "addresses to exclude seperated by comma")
}

// updateMetadata will set the contents of the metadata bucket to the values
// in db.Metadata.
func (db *BoltDatabase) updateMetadata(tx *bolt.Tx) error {
	bucket, err := tx.CreateBucketIfNotExists([]byte("Metadata"))
	if err != nil {
		return err
	}
	err = bucket.Put([]byte("Header"), []byte(db.Header))
	if err != nil {
		return err
	}
	err = bucket.Put([]byte("Version"), []byte(db.Version))
	if err != nil {
		return err
	}
	return nil
}

// Close closes the database.
func (db *BoltDatabase) Close() error {
	return db.DB.Close()
}

// OpenDatabase opens a database and validates its metadata.
func OpenDatabase(md Metadata, filename string) (*BoltDatabase, error) {
	// Open the database using a 3 second timeout (without the timeout,
	// database will potentially hang indefinitely.
	db, err := bolt.Open(filename, 0600, &bolt.Options{Timeout: 3 * time.Second})
	if err != nil {
		return nil, err
	}

	// Check the metadata.
	boltDB := &BoltDatabase{
		Metadata: md,
		DB:       db,
	}

	return boltDB, nil
}

var (
	dbMetadata = Metadata{
		Header:  "Consensus Set Database",
		Version: "1.1.0",
	}
	CoinOutputs = []byte("BlockStakeOutputs")
)

func LoadCsDB() (*BoltDatabase, error) {
	return OpenDatabase(dbMetadata, "consensus.db")
}

func (db *BoltDatabase) GetBlockStakeAddresses() (map[types.BlockStakeOutputID]types.UnlockHash, error) {
	cos := make(map[types.BlockStakeOutputID]types.UnlockHash)
	var value types.Currency
	err := db.View(func(tx *bolt.Tx) error {
		cob := tx.Bucket(CoinOutputs)
		if cob == nil {
			return errors.New("co bucket does not exist")
		}
		c := cob.Cursor()
		for k, v := c.First(); k != nil; k, v = c.Next() {
			var id types.BlockStakeOutputID
			var co types.BlockStakeOutput
			copy(id[:], k)
			err := siabin.Unmarshal(v, &co)
			if err != nil {
				return err
			}
			value = value.Add(co.Value)
			cos[id] = co.Condition.UnlockHash()
		}
		return nil
	})

	fmt.Printf("Total amount of blockstakes: %+v \n \n ", value.String())

	return cos, err
}
