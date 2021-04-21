package bridge

import (
	"context"
	"crypto/ed25519"
	"fmt"

	"github.com/ethereum/go-ethereum/log"
	"github.com/libp2p/go-libp2p"
	"github.com/libp2p/go-libp2p-core/crypto"
	"github.com/libp2p/go-libp2p-core/host"
	"github.com/libp2p/go-libp2p-core/peer"
	gorpc "github.com/libp2p/go-libp2p-gorpc"
	"github.com/multiformats/go-multiaddr"
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

func NewHost(secret string, allowId string, port int) (host.Host, error) {
	seed, err := strkey.Decode(strkey.VersionByteSeed, secret)
	if err != nil {
		return nil, err
	}

	if len(seed) != ed25519.SeedSize {
		return nil, fmt.Errorf("invalid seed size '%d' expecting '%d'", len(seed), ed25519.SeedSize)
	}

	sk := ed25519.NewKeyFromSeed(seed)

	privK, err := crypto.UnmarshalEd25519PrivateKey(sk)
	if err != nil {
		return nil, err
	}

	options := []libp2p.Option{
		libp2p.Identity(privK),
		libp2p.ListenAddrStrings(fmt.Sprintf("/ip4/0.0.0.0/tcp/%d", port)),
		libp2p.Ping(false),
		libp2p.DisableRelay(),
	}

	if allowId != "" {
		id, err := peer.Decode(allowId)
		if err != nil {
			return nil, err
		}
		filter := NewGater(id)
		options = append(options,
			libp2p.ConnectionGater(filter),
		)

	}

	ctx := context.Background()

	return libp2p.New(ctx, options...)
}

type SignersClient struct {
	peers  []string
	host   host.Host
	client *gorpc.Client
}

type response struct {
	answer *SignResponse
	err    error
}

func NewSignersClient(host host.Host, peers []string) *SignersClient {
	return &SignersClient{
		client: gorpc.NewClient(host, Protocol),
		host:   host,
		peers:  peers,
	}
}

func (s *SignersClient) Sign(ctx context.Context, signRequest SignRequest) ([]SignResponse, error) {
	ch := make(chan response)
	defer close(ch)

	for _, addr := range s.peers {
		go func(peerAddress string) {
			answer, err := s.sign(ctx, peerAddress, signRequest)

			select {
			case <-ctx.Done():
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

func (s *SignersClient) sign(ctx context.Context, target string, signRequest SignRequest) (*SignResponse, error) {
	ma, err := multiaddr.NewMultiaddr(target)
	if err != nil {
		return nil, errors.Wrap(err, "failed to parse target address")
	}

	pi, err := peer.AddrInfoFromP2pAddr(ma)
	if err != nil {
		return nil, errors.Wrap(err, "failed to extract peer info from address")
	}

	// it's okay to call Connect multiple times it will not
	// re create a connection with the peer if one already exists
	if err := s.host.Connect(ctx, *pi); err != nil {
		return nil, errors.Wrap(err, "failed to establish connection to peer")
	}

	var response SignResponse
	err = s.client.CallContext(ctx, pi.ID, "SignerService", "Sign", &signRequest, &response)
	if err != nil {
		return nil, err
	}

	return &response, nil
}
