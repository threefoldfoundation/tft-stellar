package signers

import (
	"context"
	"encoding/base64"
	"fmt"

	"github.com/libp2p/go-libp2p-core/host"
	"github.com/libp2p/go-libp2p-core/protocol"
	gorpc "github.com/libp2p/go-libp2p-gorpc"
	"github.com/stellar/go/keypair"
	"github.com/stellar/go/txnbuild"
)

const (
	Protocol = protocol.ID("/p2p/rpc/signer")
)

type SignRequest struct {
	TxnXDR string
}

type SignResponse struct {
	// Signature is a base64 of the signautre
	Signature string
	// The account address
	Address string
}

type SignerService struct {
	network string
	kp      *keypair.Full
}

func (s *SignerService) Sign(ctx context.Context, request SignRequest, response *SignResponse) error {
	loaded, err := txnbuild.TransactionFromXDR(request.TxnXDR)
	if err != nil {
		return err
	}

	txn, ok := loaded.Transaction()
	if !ok {
		return fmt.Errorf("provided transaction is of wrong type")
	}

	txn, err = txn.Sign(s.network, s.kp)
	if err != nil {
		return err
	}

	signatures := txn.Signatures()
	if len(signatures) != 1 {
		return fmt.Errorf("invalid number of signatures on the transaction")
	}

	response.Address = s.kp.Address()
	response.Signature = base64.StdEncoding.EncodeToString(signatures[0].Signature)
	return nil
}

func NewServer(host host.Host, network, secret string) (*gorpc.Server, error) {
	full, err := keypair.ParseFull(secret)
	if err != nil {
		return nil, err
	}
	server := gorpc.NewServer(host, Protocol)

	signer := SignerService{
		network: network,
		kp:      full,
	}

	err = server.Register(&signer)
	return server, err
}
