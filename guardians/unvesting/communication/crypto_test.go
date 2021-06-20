package communication

import (
	"encoding/hex"

	"testing"

	"github.com/libp2p/go-libp2p-core/crypto"
	"github.com/stretchr/testify/assert"
)

func TestStellarAddressFromP2PPublicKey(t *testing.T) {
	rawPublicKeyAsHex := "e0133c5674ad93730d7b9f57ec419017cdf4196ab3a3e79baadaea9ae1b1b54e"
	expectedAddress := "GDQBGPCWOSWZG4YNPOPVP3CBSAL435AZNKZ2HZ43VLNOVGXBWG2U5XRS"
	rawPublicKey, _ := hex.DecodeString(rawPublicKeyAsHex)
	publicKey, _ := crypto.UnmarshalEd25519PublicKey(rawPublicKey)
	address, err := StellarAddressFromP2PPublicKey(publicKey)
	assert.NoError(t, err)
	assert.Equal(t, expectedAddress, address)
}
