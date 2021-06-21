package communication

import (
	"context"
	"log"

	"github.com/libp2p/go-libp2p-core/host"
	"github.com/libp2p/go-libp2p-core/routing"
	protocol "github.com/libp2p/go-libp2p-protocol"

	"github.com/libp2p/go-libp2p-core/crypto"
)

const ProtocolID = protocol.ID("/tft/guardians/unvesting/1.0.0")

//ConnectionManager handles streams amd connections
type ConnectionManager struct {
	Host    host.Host
	Routing routing.PeerRouting
	Ctx     context.Context
}

//NewConnectionManager creates a new ConnectionManager
func NewConnectionManager() *ConnectionManager {
	c := &ConnectionManager{}
	return c
}

//Start creates a libp2p host and starts handling connections
// If privateKey is nil, a libp2p host is started without a predefined peerID
func (c *ConnectionManager) Start(ctx context.Context, privateKey crypto.PrivKey) (err error) {
	c.Ctx = ctx
	libp2pCtx, unused := context.WithCancel(ctx)
	_ = unused // pacify vet lost cancel check: libp2pCtx is always canceled through its parent

	c.Host, c.Routing, err = CreateLibp2pHost(libp2pCtx, privateKey)
	return
}

//ConnectTo connects to a peer with a specific Stellar address
func (c *ConnectionManager) ConnectTo(address string) (err error) {
	peerID, err := GetPeerIDFromStellarAddress(address)
	if err != nil {
		//Fatal since it's a predetermined address so it should be valid
		log.Fatalln("ERROR getting peerID from signer", address, err)
	}
	err = ConnectToPeer(c.Ctx, c.Host, c.Routing, peerID)
	return
}
