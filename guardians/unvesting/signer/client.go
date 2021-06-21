package signer

import (
	"github.com/libp2p/go-libp2p-core/host"
	gorpc "github.com/libp2p/go-libp2p-gorpc"

	"github.com/threefoldfoundation/tft-stellar/guardians/unvesting/communication"
)

type SigningClient struct {
	RPCClient *gorpc.Client
}

func NewSigningClient(h host.Host) *SigningClient {
	c := SigningClient{
		RPCClient: gorpc.NewClient(h, ProtocolID),
	}
	return &c
}

func (c *SigningClient) CallGetStatus(address string) (statusMessage string, err error) {

	peerID, err := communication.GetPeerIDFromStellarAddress(address)
	if err != nil {
		return
	}
	var reply GetStatusReply
	err = c.RPCClient.Call(peerID, "SigningService", "GetStatus", GetStatusRequest{}, &reply)
	if err != nil {
		return
	}
	statusMessage = reply.Message
	return
}
