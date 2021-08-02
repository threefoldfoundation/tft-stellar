package communication

import (
	"context"

	"github.com/libp2p/go-libp2p-core/host"
	dht "github.com/libp2p/go-libp2p-kad-dht"
	protocol "github.com/libp2p/go-libp2p-protocol"

	"github.com/libp2p/go-libp2p-core/crypto"
)

const ProtocolID = protocol.ID("/tft/guardians/unvesting/1.0.0")

//ConnectionManager handles streams amd connections
type ConnectionManager struct {
	Host    host.Host
	Routing *dht.IpfsDHT
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
