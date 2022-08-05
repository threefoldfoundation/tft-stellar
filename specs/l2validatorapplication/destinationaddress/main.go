package main

/*
This program makes a valid Stellar adress from a wanted prefix.
*/

import (
	"encoding/base32"
	"fmt"

	"github.com/stellar/go/strkey"
)

func main() {

	wantedAddress := "GATFL2VALIDATORAPPLICATIONAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
	wantedPublicKey, err := base32.StdEncoding.WithPadding(base32.NoPadding).DecodeString(wantedAddress)
	if err != nil {
		panic(err)
	}
	fmt.Println("Wanted public key:", wantedPublicKey)

	fmt.Println("Pure public key:", wantedPublicKey[1:33])
	address, err := strkey.Encode(strkey.VersionByteAccountID, wantedPublicKey[1:33])
	if err != nil {
		panic(err)
	}
	fmt.Println(address)

}
