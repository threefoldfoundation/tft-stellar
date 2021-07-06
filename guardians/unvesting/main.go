package main

import (
	"flag"
	"log"

	"github.com/stellar/go/keypair"

	"github.com/threefoldfoundation/tft-stellar/guardians/unvesting/cosigner"

	"github.com/threefoldfoundation/tft-stellar/guardians/unvesting/initiator"
)

func main() {

	var accountSecret string
	var network string

	flag.StringVar(&accountSecret, "accountsecret", "", "The Cosigning account secret, if not bgiven, an initiator is started")
	flag.StringVar(&network, "network", "test", "The stellar network to use: 'public' or 'test'")

	flag.Parse()

	if network != "public" && network != "test" {
		flag.Usage()
		log.Fatalln("Invalid network")
	}

	if accountSecret == "" {
		initiator.Start(network)
	} else {
		_, err := keypair.ParseFull(accountSecret)
		if err != nil {
			flag.Usage()
			log.Fatalln("Invalid accountsecret")
		}
		err = cosigner.Start(accountSecret, network)
		if err != nil {
			log.Fatalln(err)
		}
	}
}
