module github.com/threefoldfoundation/tft-stellar/eth-bridge

go 1.16

replace github.com/ethereum/go-ethereum v1.10.1 => github.com/binance-chain/bsc v1.0.7

require (
	github.com/ethereum/go-ethereum v1.10.1
	github.com/libp2p/go-libp2p v0.13.0
	github.com/libp2p/go-libp2p-connmgr v0.2.4
	github.com/libp2p/go-libp2p-core v0.8.5
	github.com/libp2p/go-libp2p-gorpc v0.1.2
	github.com/libp2p/go-libp2p-kad-dht v0.11.1
	github.com/libp2p/go-libp2p-quic-transport v0.10.0
	github.com/libp2p/go-libp2p-secio v0.2.2
	github.com/libp2p/go-libp2p-tls v0.1.3
	github.com/multiformats/go-multiaddr v0.3.1
	github.com/pkg/errors v0.9.1
	github.com/rs/zerolog v1.21.0
	github.com/spf13/pflag v1.0.3
	github.com/stellar/go v0.0.0-20210331095526-7b139512d880
)
