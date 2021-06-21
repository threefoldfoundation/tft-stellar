package communication

import (
	"context"
	"log"
	"time"

	"github.com/libp2p/go-libp2p-core/host"

	"github.com/libp2p/go-libp2p"
	connmgr "github.com/libp2p/go-libp2p-connmgr"
	"github.com/libp2p/go-libp2p-core/peer"
	"github.com/libp2p/go-libp2p-core/routing"
	dht "github.com/libp2p/go-libp2p-kad-dht"
	libp2pquic "github.com/libp2p/go-libp2p-quic-transport"
	secio "github.com/libp2p/go-libp2p-secio"
	libp2ptls "github.com/libp2p/go-libp2p-tls"

	"github.com/libp2p/go-libp2p-core/crypto"
)

//CreateLibp2pHost creates a libp2p host with peerRouting enabled and connects to the bootstrap nodes
// If privateKey is nil, a libp2p host is started without a predefined peerID
func CreateLibp2pHost(ctx context.Context, privateKey crypto.PrivKey) (host.Host, routing.PeerRouting, error) {

	var idht *dht.IpfsDHT
	var err error
	options := make([]libp2p.Option, 0, 0)
	if privateKey != nil {
		options = append(options,
			libp2p.Identity(privateKey))
	}
	// Multiple listen addresses
	options = append(options, libp2p.ListenAddrStrings(
		"/ip4/0.0.0.0/tcp/0",      // regular tcp connections
		"/ip4/0.0.0.0/udp/0/quic", // a UDP endpoint for the QUIC transport
	))
	// support TLS connections
	options = append(options,
		libp2p.Security(libp2ptls.ID, libp2ptls.New))
	// support secio connections
	options = append(options,
		libp2p.Security(secio.ID, secio.New))

	// support QUIC
	options = append(options,
		libp2p.Transport(libp2pquic.NewTransport))

	// support any other default transports (TCP)
	options = append(options,
		libp2p.DefaultTransports)
	// Let's prevent our peer from having too many
	// connections by attaching a connection manager.
	options = append(options,
		libp2p.ConnectionManager(connmgr.NewConnManager(
			100,         // Lowwater
			400,         // HighWater,
			time.Minute, // GracePeriod
		)))
	// Attempt to open ports using uPNP for NATed hosts.
	options = append(options,
		libp2p.NATPortMap())
	// Let this host use the DHT to find other hosts
	options = append(options,
		libp2p.Routing(func(h host.Host) (routing.PeerRouting, error) {
			idht, err = dht.New(ctx, h)
			return idht, err
		}))

	// Let this host use relays and advertise itself on relays if
	// it finds it is behind NAT. Use libp2p.Relay(options...) to
	// enable active relays and more.
	options = append(options, libp2p.EnableAutoRelay())

	libp2phost, err := libp2p.New(ctx, options...)
	log.Println("Libp2p host started with PeerID", libp2phost.ID())
	// This connects to public bootstrappers
	for _, addr := range dht.DefaultBootstrapPeers {
		pi, _ := peer.AddrInfoFromP2pAddr(addr)
		// We ignore errors as some bootstrap peers may be down
		// and that is fine.
		libp2phost.Connect(ctx, *pi)
	}
	return libp2phost, idht, err
}
func ConnectToPeer(ctx context.Context, p2phost host.Host, hostRouting routing.PeerRouting, peerID peer.ID) (err error) {

	findPeerCtx, cancel := context.WithCancel(ctx)
	defer cancel()
	peeraddrInfo, err := hostRouting.FindPeer(findPeerCtx, peerID)
	if err != nil {
		return
	}
	ConnectPeerCtx, cancel := context.WithCancel(ctx)
	defer cancel()
	err = p2phost.Connect(ConnectPeerCtx, peeraddrInfo)
	return
}
