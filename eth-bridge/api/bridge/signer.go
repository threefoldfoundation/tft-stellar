package bridge

import (
	"context"
	"crypto/ed25519"
	"fmt"
	"time"

	"github.com/ethereum/go-ethereum/log"
	"github.com/libp2p/go-libp2p"
	connmgr "github.com/libp2p/go-libp2p-connmgr"
	"github.com/libp2p/go-libp2p-core/crypto"
	"github.com/libp2p/go-libp2p-core/host"
	"github.com/libp2p/go-libp2p-core/peer"
	"github.com/libp2p/go-libp2p-core/routing"
	gorpc "github.com/libp2p/go-libp2p-gorpc"
	dht "github.com/libp2p/go-libp2p-kad-dht"
	libp2pquic "github.com/libp2p/go-libp2p-quic-transport"
	secio "github.com/libp2p/go-libp2p-secio"
	libp2ptls "github.com/libp2p/go-libp2p-tls"
	"github.com/stellar/go/strkey"
	"github.com/stellar/go/support/errors"
)

type SignerConfig struct {
	Secret   string
	BridgeID string
	Network  string
}

func (c *SignerConfig) Valid() error {
	if c.Network == "" {
		return fmt.Errorf("network is requires")
	}
	if c.Secret == "" {
		return fmt.Errorf("secret is required")
	}

	if c.BridgeID == "" {
		return fmt.Errorf("bridge identity is required")
	}

	return nil
}

func NewHost(ctx context.Context, secret string) (host.Host, routing.PeerRouting, error) {
	seed, err := strkey.Decode(strkey.VersionByteSeed, secret)
	if err != nil {
		return nil, nil, err
	}

	if len(seed) != ed25519.SeedSize {
		return nil, nil, fmt.Errorf("invalid seed size '%d' expecting '%d'", len(seed), ed25519.SeedSize)
	}

	sk := ed25519.NewKeyFromSeed(seed)

	privK, err := crypto.UnmarshalEd25519PrivateKey(sk)
	if err != nil {
		return nil, nil, err
	}

	return createLibp2pHost(ctx, privK)
}

func createLibp2pHost(ctx context.Context, privateKey crypto.PrivKey) (host.Host, routing.PeerRouting, error) {

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

type SignersClient struct {
	peers  []peer.ID
	host   host.Host
	router routing.PeerRouting
	client *gorpc.Client
}

type response struct {
	answer *SignResponse
	err    error
}

// NewSignersClient creates a signer client with given stellar addresses
// the addresses are going to be used to get libp2p ID where we connect
// to and ask them to sign
func NewSignersClient(ctx context.Context, host host.Host, router routing.PeerRouting, addresses []string) (*SignersClient, error) {
	var ids []peer.ID
	for _, address := range addresses {
		id, err := getPeerIDFromStellarAddress(address)
		if err != nil {
			return nil, errors.Wrap(err, "failed to get peer info")
		}
		ids = append(ids, id)
	}

	return &SignersClient{
		client: gorpc.NewClient(host, Protocol),
		host:   host,
		router: router,
		peers:  ids,
	}, nil
}

func (s *SignersClient) Sign(ctx context.Context, signRequest SignRequest) ([]SignResponse, error) {
	ch := make(chan response)
	defer close(ch)

	for _, addr := range s.peers {
		go func(peerID peer.ID) {
			// cancel context after 30 seconds
			signCtx, cancel := context.WithTimeout(ctx, time.Second*30)
			defer cancel()

			answer, err := s.sign(signCtx, peerID, signRequest)

			select {
			case <-signCtx.Done():
			case ch <- response{answer: answer, err: err}:
			}
		}(addr)
	}

	var results []SignResponse
	replies := 0
	for reply := range ch {
		replies++
		if reply.err != nil {
			log.Error("failed to get signature from", "err", reply.err.Error())
			continue
		}

		results = append(results, *reply.answer)
		if len(results) == signRequest.RequiredSignatures || replies == len(s.peers) {
			break
		}
	}

	if len(results) != signRequest.RequiredSignatures {
		return nil, fmt.Errorf("required number of signatures is not met")
	}

	return results, nil
}

func (s *SignersClient) sign(ctx context.Context, id peer.ID, signRequest SignRequest) (*SignResponse, error) {
	if len(s.host.Peerstore().Addrs(id)) == 0 {
		if err := connectToPeer(ctx, s.host, s.router, id); err != nil {
			return nil, errors.Wrapf(err, "failed to connect to host id '%s'", id.Pretty())
		}
	}

	var response SignResponse
	if err := s.client.CallContext(ctx, id, "SignerService", "Sign", &signRequest, &response); err != nil {
		return nil, err
	}

	return &response, nil
}

func getPeerIDFromStellarAddress(address string) (peerID peer.ID, err error) {

	versionbyte, pubkeydata, err := strkey.DecodeAny(address)
	if err != nil {
		return
	}
	if versionbyte != strkey.VersionByteAccountID {
		err = fmt.Errorf("%s is not a valid Stellar address", address)
		return
	}
	libp2pPubKey, err := crypto.UnmarshalEd25519PublicKey(pubkeydata)
	if err != nil {
		return
	}

	peerID, err = peer.IDFromPublicKey(libp2pPubKey)
	return peerID, err
}

func connectToPeer(ctx context.Context, p2phost host.Host, hostRouting routing.PeerRouting, peerID peer.ID) (err error) {

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
