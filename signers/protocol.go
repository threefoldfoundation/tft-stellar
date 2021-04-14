package signers

import (
	"context"
	"crypto/ed25519"

	"github.com/libp2p/go-libp2p-core/host"
	"github.com/libp2p/go-libp2p-core/protocol"
	gorpc "github.com/libp2p/go-libp2p-gorpc"
)

const (
	Protocol = protocol.ID("/p2p/rpc/signer")
)

type SignRequest struct {
	Message []byte
}

type SignResponse struct {
	Signature []byte
}

type SignerService struct {
	sk ed25519.PrivateKey
}

func (s *SignerService) Sign(ctx context.Context, request SignRequest, response *SignResponse) error {
	response.Signature = ed25519.Sign(s.sk, request.Message)
	return nil
}

func NewServer(host host.Host, sk ed25519.PrivateKey) (*gorpc.Server, error) {
	server := gorpc.NewServer(host, Protocol)

	signer := SignerService{sk}
	err := server.Register(&signer)
	return server, err
}
