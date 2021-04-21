package signers

import (
	"context"

	"github.com/libp2p/go-libp2p-core/host"
	"github.com/libp2p/go-libp2p-core/peer"
	gorpc "github.com/libp2p/go-libp2p-gorpc"
	"github.com/multiformats/go-multiaddr"
	"github.com/pkg/errors"
)

type Signer struct {
	host   host.Host
	client *gorpc.Client
}

func NewSigner(host host.Host) *Signer {
	return &Signer{
		host:   host,
		client: gorpc.NewClient(host, Protocol),
	}
}

func (s *Signer) Sign(ctx context.Context, target string, signRequest SignRequest) (*SignResponse, error) {
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
