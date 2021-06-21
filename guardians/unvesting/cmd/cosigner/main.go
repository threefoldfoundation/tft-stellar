package main

import (
	"context"
	"flag"
	"log"
	"time"

	"github.com/stellar/go/keypair"
	"github.com/threefoldfoundation/tft-stellar/guardians/unvesting/communication"
)

func main() {

	var accountSecret string
	var network string

	flag.StringVar(&accountSecret, "accountsecret", "", "The Cosigning account secret")
	flag.StringVar(&network, "network", "public", "The stellar network to use: 'public' or 'test'")

	flag.Parse()

	kp, err := keypair.ParseFull(accountSecret)
	if err != nil {
		log.Fatalln("Invalid accountsecret")
	}
	log.Println("Starting cosigner with account", kp.Address(), "on the", network, "network")
	libp2pPrivKey := communication.GetLibp2pPrivateKeyFromStellarSeed(accountSecret)
	//stellarKP := keypair.MustParseFull(walletSecret)
	rootCtx, cancel := context.WithCancel(context.Background())
	defer cancel()

	connMgr := communication.NewConnectionManager()
	communicationCtx, cancel := context.WithCancel(rootCtx)
	defer cancel()
	connMgr.Start(communicationCtx, libp2pPrivKey)

	for {
		time.Sleep(time.Second * 10)
	}
}
