package main

import (
	"context"
	"flag"

	"github.com/threefoldfoundation/tft-stellar/guardians/unvesting/communication"
)

func main() {

	var accountSecret string
	var network string

	flag.StringVar(&walletSecret, "accountsecret", "", "The Cosigning account secret")
	flag.StringVar(&network, "network", "public", "The stellar network to use: 'public' or 'test'")

	flag.Parse()

	libp2pPrivKey := communication.GetLibp2pPrivateKeyFromStellarSeed(accountSecret)
	//stellarKP := keypair.MustParseFull(walletSecret)
	rootCtx, cancel := context.WithCancel(context.Background())
	defer cancel()

	connMgr := communication.NewConnectionManager()
	communicationCtx, cancel := context.WithCancel(rootCtx)
	defer cancel()
	connMgr.Start(communicationCtx, libp2pPrivKey)
}
