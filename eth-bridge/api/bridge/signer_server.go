package bridge

import (
	"context"
	"encoding/base64"
	"fmt"

	"github.com/ethereum/go-ethereum/log"
	"github.com/libp2p/go-libp2p-core/host"
	"github.com/libp2p/go-libp2p-core/protocol"
	gorpc "github.com/libp2p/go-libp2p-gorpc"
	"github.com/multiformats/go-multiaddr"
	"github.com/pkg/errors"
	"github.com/stellar/go/clients/horizonclient"
	"github.com/stellar/go/keypair"
	"github.com/stellar/go/network"
	"github.com/stellar/go/protocols/horizon/effects"
	"github.com/stellar/go/txnbuild"
	"github.com/stellar/go/xdr"
)

const (
	Protocol = protocol.ID("/p2p/rpc/signer")
)

type SignRequest struct {
	TxnXDR             string
	RequiredSignatures int
	Block              int
	TxInfo             TransactionInfo
}

type TransactionInfo struct {
	TxHash  string
	Amount  uint64
	From    string
	To      string
	Network string
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

	// todo validate
	for _, op := range txn.Operations() {
		opXDR, err := op.BuildXDR()
		if err != nil {
			return fmt.Errorf("failed to build operation xdr")
		}

		if opXDR.Body.Type != xdr.OperationTypePayment {
			continue
		}

		paymentOperation := opXDR.Body.PaymentOp

		if paymentOperation.Destination.GoString() != request.TxInfo.From {
			return fmt.Errorf("wrong source")
		}

		if paymentOperation.Destination.GoString() != request.TxInfo.To {
			return fmt.Errorf("wrong destination")
		}

		if paymentOperation.Amount != xdr.Int64(request.TxInfo.Amount) {
			return fmt.Errorf("wrong amount")
		}
	}

	txn, err = txn.Sign(s.getNetworkPassPhrase(), s.kp)
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

func newSignerServer(host host.Host, network, secret string) (*gorpc.Server, error) {
	full, err := keypair.ParseFull(secret)
	if err != nil {
		return nil, err
	}
	log.Debug("wallet address", "address", full.Address())
	server := gorpc.NewServer(host, Protocol)

	signer := SignerService{
		network: network,
		kp:      full,
	}

	err = server.Register(&signer)
	return server, err
}

// getNetworkPassPhrase gets the Stellar network passphrase based on the wallet's network
func (s *SignerService) getNetworkPassPhrase() string {
	switch s.network {
	case "testnet":
		return network.TestNetworkPassphrase
	case "production":
		return network.PublicNetworkPassphrase
	default:
		return network.TestNetworkPassphrase
	}
}

// GetHorizonClient gets the horizon client based on the wallet's network
func (s *SignerService) getHorizonClient() (*horizonclient.Client, error) {
	switch s.network {
	case "testnet":
		return horizonclient.DefaultTestNetClient, nil
	case "production":
		return horizonclient.DefaultPublicNetClient, nil
	default:
		return nil, errors.New("network is not supported")
	}
}

func (s *SignerService) getTransactionEffects(txHash string) (effects effects.EffectsPage, err error) {
	client, err := s.getHorizonClient()
	if err != nil {
		return effects, err
	}

	effectsReq := horizonclient.EffectRequest{
		ForTransaction: txHash,
	}
	effects, err = client.Effects(effectsReq)
	if err != nil {
		return effects, err
	}

	return effects, nil
}

func NewSignerServer(host host.Host, network, secret string) error {
	log.Info("server started", "identity", host.ID().Pretty())
	ipfs, err := multiaddr.NewMultiaddr(fmt.Sprintf("/ipfs/%s", host.ID().Pretty()))
	if err != nil {
		return err
	}

	for _, addr := range host.Addrs() {
		full := addr.Encapsulate(ipfs)
		log.Info("p2p node address", "address", full.String())
	}

	_, err = newSignerServer(host, network, secret)
	return err
}
