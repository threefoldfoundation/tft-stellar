package main

import (
	"database/sql"
	"strings"
)

const (
	CREATE_TABLE_STATEMENT = `
	CREATE TABLE IF NOT EXISTS stellartxs (
		"transaction" TEXT,
		"from" TEXT,
		"amount" TEXT,
		"to" TEXT,
		"token" TEXT,
		"textmemo" TEXT,
		"timestamp" INT
	);`

	CREATE_TXCURSOR_STATEMENT = `
	CREATE TABLE IF NOT EXISTS stellartxcursor (
		"address" TEXT PRIMARY KEY,
		"cursor" TEXT
	);`
)

func createStellarTables(db *sql.DB) (err error) {
	_, err = db.Exec(CREATE_TABLE_STATEMENT)
	if err != nil {
		return
	}
	_, err = db.Exec(CREATE_TXCURSOR_STATEMENT)
	return
}

func LoadAddressesToAnalyse(db *sql.DB) (addresses map[string]bool, err error) {
	if addresses, err = loadMintToAddresses(db); err != nil {
		return
	}
	err = addDestinationAdresses(db, addresses)
	return
}
func loadMintToAddresses(db *sql.DB) (mintToAddresses map[string]bool, err error) {
	mintedRows, err := db.Query(`SELECT "to" FROM minted`)
	if err != nil {
		return
	}
	defer mintedRows.Close()
	mintToAddresses = make(map[string]bool)
	for mintedRows.Next() {
		var address string
		if err = mintedRows.Scan(&address); err != nil {
			return
		}
		mintToAddresses[address] = true
	}
	err = mintedRows.Err()
	return
}

func addDestinationAdresses(db *sql.DB, addresses map[string]bool) (err error) {
	rows, err := db.Query(`SELECT "to" FROM stellartxs`)
	if err != nil {
		return
	}
	defer rows.Close()
	for rows.Next() {
		var address string
		if err = rows.Scan(&address); err != nil {
			return
		}
		if !strings.HasPrefix(address, "lp ") {
			addresses[address] = true
		}
	}
	err = rows.Err()
	return
}

func loadTransactionCursor(db *sql.DB, address string) (cursor string, err error) {
	cursorRows, err := db.Query(`SELECT "cursor" FROM stellartxcursor WHERE "address" = ?`, address)
	if err != nil {
		return
	}
	defer cursorRows.Close()
	if cursorRows.Next() {
		err = cursorRows.Scan(&cursor)
	}
	if err == nil {
		err = cursorRows.Err()
	}
	return
}

func storeTransactionCursor(tx *sql.Tx, adddress string, cursor string) (err error) {
	_, err = tx.Exec(`INSERT INTO stellartxcursor(address,cursor) VALUES(?,?) ON CONFLICT(address) DO UPDATE SET cursor=excluded.cursor;`, adddress, cursor)

	return
}
func StorePayment(tx *sql.Tx, transactionID string, from string, amount string, to string, token string, textMemo string, timestamp int64) (err error) {
	_, err = tx.Exec(`INSERT INTO stellartxs("transaction","from","amount","to","token","textmemo","timestamp") VALUES(?,?,?,?,?,?,?)`, transactionID, from, amount, to, token, textMemo, timestamp)

	return
}
