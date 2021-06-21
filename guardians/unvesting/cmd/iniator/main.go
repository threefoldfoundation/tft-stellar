package main

import (
	"context"
	"flag"
	"log"
	"time"

	"github.com/threefoldfoundation/tft-stellar/guardians/unvesting/communication"
	"github.com/threefoldfoundation/tft-stellar/guardians/unvesting/signer"

	gorpc "github.com/libp2p/go-libp2p-gorpc"
)

func main() {
	var network string

	flag.StringVar(&network, "network", "public", "The stellar network to use: 'public' or 'test'")

	flag.Parse()

	if network != "public" && network != "test" {
		flag.Usage()
		log.Fatalln("Invalid network")
	}
	log.Println("Starting initiator on the", network, "network")
	rootCtx, cancel := context.WithCancel(context.Background())
	defer cancel()

	connMgr := communication.NewConnectionManager()
	communicationCtx, cancel := context.WithCancel(rootCtx)
	defer cancel()
	connMgr.Start(communicationCtx, nil)
	signerAddresses := signer.GetSignerAddresses(network)
	for _, signerAddress := range signerAddresses {
		err := connMgr.ConnectTo(signerAddress)
		if err != nil {
			log.Println("Failed to connect to signer", signerAddress, err)
		} else {
			log.Println("Connected to signer", signerAddress)
		}
	}
	signerClient := gorpc.NewClient(connMgr.Host, signer.ProtocolID)
	for {
		//Check the status of the signers every 10 minutes
		for _, signerAddress := range signerAddresses {
			peerID, _ := communication.GetPeerIDFromStellarAddress(signerAddress)
			var reply signer.GetStatusReply
			err := signerClient.Call(peerID, "SigningService", "GetStatus", signer.GetStatusRequest{}, &reply)
			if err != nil {
				log.Println("ERROR calling GetStatus for signer", signerAddress, ":", err)
			} else {
				log.Println("Status of", signerAddress, ":", reply.Message)
			}

		}
		time.Sleep(time.Minute * 10)
	}
}
