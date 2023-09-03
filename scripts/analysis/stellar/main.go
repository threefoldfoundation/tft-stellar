package main

import (
	"flag"
)

func main() {
	var dbPath string
	flag.StringVar(&dbPath, "db", "tft_data.db", "Path of the sqlite db")
	flag.Parse()

}
