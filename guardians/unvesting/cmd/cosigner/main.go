package main

import (
	"context"
	"flag"
	"log"
	"time"

	gorpc "github.com/libp2p/go-libp2p-gorpc"
	"github.com/stellar/go/keypair"
	"github.com/threefoldfoundation/tft-stellar/guardians/unvesting/communication"
	"github.com/threefoldfoundation/tft-stellar/guardians/unvesting/signer"
)

func main() {

	var accountSecret string
	var network string

	flag.StringVar(&accountSecret, "accountsecret", "", "The Cosigning account secret")
	flag.StringVar(&network, "network", "public", "The stellar network to use: 'public' or 'test'")

	flag.Parse()

	kp, err := keypair.ParseFull(accountSecret)
	if err != nil {
		flag.Usage()
		log.Fatalln("Invalid accountsecret")
	}
	if network != "public" && network != "test" {
		flag.Usage()
		log.Fatalln("Invalid network")
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
	signerService := signer.NewSigningService(network)
	server := gorpc.NewServer(connMgr.Host, signer.ProtocolID)
	server.Register(&signerService)
	for {
		time.Sleep(time.Second * 10)
	}
}
