package communication

import (
	"bytes"
	"fmt"
	"log"

	"github.com/libp2p/go-libp2p-core/crypto"
	"github.com/libp2p/go-libp2p-core/peer"
	"github.com/stellar/go/strkey"
)

func GetLibp2pPrivateKeyFromStellarSeed(seed string) crypto.PrivKey {
	versionbyte, rawSecret, err := strkey.DecodeAny(seed)
	if err != nil {
		log.Fatal(err)
	}

	if versionbyte != strkey.VersionByteSeed {
		log.Fatalf("%s is not a valid Stellar seed", seed)
	}

	secretreader := bytes.NewReader(rawSecret)
	libp2pPrivKey, _, err := crypto.GenerateEd25519Key(secretreader)
	if err != nil {
		log.Fatal(err)
	}
	return libp2pPrivKey
}

func GetPeerIDFromStellarAddress(address string) (peerID peer.ID, err error) {

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

func StellarAddressFromP2PPublicKey(pubKey crypto.PubKey) (address string, err error) {
	rawPubKey, err := pubKey.Raw()
	if err != nil {
		return
	}
	address, err = strkey.Encode(strkey.VersionByteAccountID, rawPubKey)
	return
}
