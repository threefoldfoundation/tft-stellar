package communication

import (
	"bufio"
	"context"
	"log"
	"strings"

	"github.com/libp2p/go-libp2p-core/host"
	p2pnetwork "github.com/libp2p/go-libp2p-core/network"
	"github.com/libp2p/go-libp2p-core/routing"

	"github.com/libp2p/go-libp2p-core/crypto"
)

const protocolID = "/tft/guardians/unvesting/1.0.0"

//ConnectionManager handles streams amd connections
type ConnectionManager struct {
	Host     host.Host
	Routing  routing.PeerRouting
	Ctx      context.Context
	Messages chan string
}

//NewConnectionManager creates a new ConnectionManager
func NewConnectionManager() *ConnectionManager {
	c := &ConnectionManager{
		//All received messages are sent through this channel
		Messages: make(chan string),
	}
	return c
}

//Start creates a libp2p host and starts handling connections
func (c *ConnectionManager) Start(ctx context.Context, privateKey crypto.PrivKey) (err error) {
	c.Ctx = ctx
	libp2pCtx, unused := context.WithCancel(ctx)
	_ = unused // pacify vet lost cancel check: libp2pCtx is always canceled through its parent

	c.Host, c.Routing, err = CreateLibp2pHost(libp2pCtx, privateKey)
	if err != nil {
		return
	}

	c.Host.SetStreamHandler(protocolID, func(s p2pnetwork.Stream) {
		connection := s.Conn()
		remoteAddress, err := StellarAddressFromP2PPublicKey(connection.RemotePublicKey())
		if err != nil {
			log.Println("Failed to get the Stellar address from remote connection", connection.RemotePeer())
			return
		}
		log.Println("[DEBUG] Got a new stream from", remoteAddress)
		rw := bufio.NewReadWriter(bufio.NewReader(s), bufio.NewWriter(s))
		message, err := rw.ReadString('\n')
		if err != nil {
			log.Println("Failed to read message")
			return
		}
		message = strings.TrimSuffix(message, "\n")
		c.Messages <- message
		s.Close() //TODO: don't close it immediately but reuse when possible.
	})
	return nil
}

//connectTo connects to a peer with a specific Stellar address
func (c *ConnectionManager) connectTo(address string) {
	peerID, err := GetPeerIDFromStellarAddress(address)
	if err != nil {
		//Fatal since we got the address from the Stellar network so it should be valid
		log.Fatalln("ERROR getting peerID from signer", address, err)
	}

	ctx, unused := context.WithCancel(c.Ctx)
	_ = unused // pacify vet lost cancel check: libp2pCtx is always canceled through its parent

	err = ConnectToPeer(ctx, c.Host, c.Routing, peerID)
	if err != nil {
		log.Println("Failed to connect to ", address, err)
	} else {
		log.Println("Connected to ", address)
	}
}

//Send sends a message to a list of addresses
//TODO: do this in parallel to speed it up
func (c *ConnectionManager) Send(message string, addresses []string) {

	for _, cosignerAddress := range addresses {
		if c.Ctx.Err() != nil {
			return
		}
		peerID, err := GetPeerIDFromStellarAddress(cosignerAddress)
		if err != nil {
			//Fatal since we got the addresses from the Stellar network so they should be valid
			log.Fatalln("ERROR getting peerID from signer", cosignerAddress, ":", err)
		}
		ctx, cancel := context.WithCancel(c.Ctx)
		s, err := c.Host.NewStream(ctx, peerID, protocolID)

		if err != nil {
			log.Println("Failed to open a stream to", cosignerAddress, ":", err)
			cancel()
			continue
		}
		writer := bufio.NewWriter(s)
		_, err = writer.WriteString(message + "\n")

		err = writer.Flush()
		if err != nil {
			log.Println("Failed to send the transaction to sign to", cosignerAddress, ":", err)
		}
		log.Println("[DEBUG] Sent message to", cosignerAddress, ":'", message, "'")
		cancel()
	}
}
