package main

import (
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"log"
)

func test() {
	const s = "53d17EBE198ECDc387d3c6EB5964216dfda2d29E"
	decoded, err := hex.DecodeString(s)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("%s\n", decoded)

	str := base64.StdEncoding.EncodeToString(decoded)
	fmt.Println(str)

}
