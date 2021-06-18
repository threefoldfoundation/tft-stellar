package main

import (
	"context"
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

func CreateLibp2pHost(ctx context.Context, privateKey crypto.PrivKey) (host.Host, routing.PeerRouting, error) {

	var idht *dht.IpfsDHT
	var err error
	libp2phost, err := libp2p.New(ctx,
		// Use the keypair we generated
		libp2p.Identity(privateKey),
		// Multiple listen addresses
		libp2p.ListenAddrStrings(
			"/ip4/0.0.0.0/tcp/0",      // regular tcp connections
			"/ip4/0.0.0.0/udp/0/quic", // a UDP endpoint for the QUIC transport
		),
		// support TLS connections
		libp2p.Security(libp2ptls.ID, libp2ptls.New),
		// support secio connections
		libp2p.Security(secio.ID, secio.New),
		// support QUIC
		libp2p.Transport(libp2pquic.NewTransport),
		// support any other default transports (TCP)
		libp2p.DefaultTransports,
		// Let's prevent our peer from having too many
		// connections by attaching a connection manager.
		libp2p.ConnectionManager(connmgr.NewConnManager(
			100,         // Lowwater
			400,         // HighWater,
			time.Minute, // GracePeriod
		)),
		// Attempt to open ports using uPNP for NATed hosts.
		libp2p.NATPortMap(),
		// Let this host use the DHT to find other hosts
		libp2p.Routing(func(h host.Host) (routing.PeerRouting, error) {
			idht, err = dht.New(ctx, h)
			return idht, err
		}),
		// Let this host use relays and advertise itself on relays if
		// it finds it is behind NAT. Use libp2p.Relay(options...) to
		// enable active relays and more.
		libp2p.EnableAutoRelay(),
	)
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
