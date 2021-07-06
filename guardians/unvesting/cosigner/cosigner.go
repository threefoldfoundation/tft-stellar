package cosigner

import (
	"context"
	"log"
	"time"

	gorpc "github.com/libp2p/go-libp2p-gorpc"
	"github.com/stellar/go/keypair"
	"github.com/threefoldfoundation/tft-stellar/guardians/unvesting/communication"
	"github.com/threefoldfoundation/tft-stellar/guardians/unvesting/signer"
)

//Start starts a cosigner
func Start(accountSecret string, network string) (err error) {

	kp, err := keypair.ParseFull(accountSecret)
	if err != nil {
		return
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
