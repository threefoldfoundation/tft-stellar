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
	"github.com/multiformats/go-multiaddr"
	"github.com/stellar/go/strkey"
	"github.com/threefoldfoundation/tft-stellar/eth-bridge/signers"
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

func NewSigner(host host.Host, network, secret string) error {
	log.Info("server started", "identity", host.ID().Pretty())
	ipfs, err := multiaddr.NewMultiaddr(fmt.Sprintf("/ipfs/%s", host.ID().Pretty()))
	if err != nil {
		return err
	}

	for _, addr := range host.Addrs() {
		full := addr.Encapsulate(ipfs)
		log.Info("p2p node address", "address", full.String())
	}

	_, err = signers.NewServer(host, network, secret)
	return err
}

type SignersClient struct {
	client *signers.Signer
	peers  []string
}

type response struct {
	answer *signers.SignResponse
	err    error
}

func NewSignersClient(host host.Host, peers []string) *SignersClient {
	return &SignersClient{
		client: signers.NewSigner(host),
		peers:  peers,
	}
}

func (s *SignersClient) Sign(message string, require int) ([]signers.SignResponse, error) {
	ctx, cancel := context.WithCancel(context.Background())

	defer cancel()

	ch := make(chan response)
	defer close(ch)

	for _, addr := range s.peers {
		go func(peerAddress string) {
			answer, err := s.client.Sign(ctx, peerAddress, message)

			select {
			case <-ctx.Done():
			case ch <- response{answer: answer, err: err}:
			}
		}(addr)
	}

	var results []signers.SignResponse
	for reply := range ch {
		if reply.err != nil {
			log.Error("failed to get signature from ''")
			continue
		}

		results = append(results, *reply.answer)
		if len(results) == require {
			break
		}
	}

	if len(results) != require {
		return nil, fmt.Errorf("required number of signatures is not met")
	}

	return results, nil
}
