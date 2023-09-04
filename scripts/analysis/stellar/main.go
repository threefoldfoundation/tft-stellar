package main

import (
	"database/sql"
	"flag"
	"fmt"

	"github.com/tobgu/qframe"
	qsql "github.com/tobgu/qframe/config/sql"
	_ "modernc.org/sqlite"
)

const (
	CREATE_TABLE_STATEMENT = `
	CREATE TABLE IF NOT EXISTS stellartxs (
		"transaction" TEXT,
		"from" TEXT,
		"amount" TEXT,
		"to" TEXT,
		"timestamp" INT
	);`
)

func main() {
	var dbPath string
	var preview bool
	flag.StringVar(&dbPath, "db", "tft_data.db", "Path of the sqlite db")
	flag.BoolVar(&preview, "preview", false, "Print the information instead of storing it in the db")
	flag.Parse()
	db, err := sql.Open("sqlite", dbPath)
	if err != nil {
		panic(err)
	}
	defer db.Close()

	_, err = db.Exec(CREATE_TABLE_STATEMENT)
	tx, err := db.Begin()
	if err != nil {
		panic(err)
	}
	mintToAddresses := qframe.ReadSQL(tx,
		qsql.Query(`SELECT "to" FROM minted`),
		qsql.SQLite(),
	)
	distinctMintToAddresses, err := mintToAddresses.Distinct().StringView("to")
	if err != nil {
		panic(err)
	}

	for _, address := range distinctMintToAddresses.Slice() {
		fmt.Println("Address:", *address)

	}

	if err != nil {
		panic(err)
	}
}
