package bridge

import (
	"context"

	"github.com/ethereum/go-ethereum/log"
	"github.com/threefoldfoundation/tft-stellar/eth-bridge/signers"
)

type Signers struct {
	client    *signers.Signer
	addresses []string
}

type response struct {
	answer  *signers.SignResponse
	address string
	err     error
}

func NewSigners(client *signers.Signer, addresses []string) *Signers {
	return &Signers{
		client:    client,
		addresses: addresses,
	}
}

func (s *Signers) Sign(message string, require int) []signers.SignResponse {
	ctx, cancel := context.WithCancel(context.Background())

	defer cancel()

	ch := make(chan response)
	defer close(ch)

	for _, addr := range s.addresses {
		go func(addr string) {
			answer, err := s.client.Sign(ctx, addr, message)

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
		}
	}

	return results
}
