package bridge

import (
	"context"
	"crypto/ed25519"
	"fmt"

	"github.com/libp2p/go-libp2p"
	"github.com/libp2p/go-libp2p-core/crypto"
	"github.com/libp2p/go-libp2p-core/peer"
	"github.com/multiformats/go-multiaddr"
	"github.com/rs/zerolog/log"
	"github.com/stellar/go/strkey"
	"github.com/threefoldfoundation/tft-stellar/eth-bridge/signers"
)

type SignerConfig struct {
	Secret   string
	BridgeID string
	Network  string
}

func (c *SignerConfig) Valid() error {
	if c.Network == "" {
		return fmt.Errorf("network is requires")
	}
	if c.Secret == "" {
		return fmt.Errorf("secret is required")
	}

	if c.BridgeID == "" {
		return fmt.Errorf("bridge identity is required")
	}

	return nil
}

func NewSigner(cfg *SignerConfig) error {
	if err := cfg.Valid(); err != nil {
		return err
	}

	seed, err := strkey.Decode(strkey.VersionByteSeed, cfg.Secret)
	if err != nil {
		return err
	}

	if len(seed) != ed25519.SeedSize {
		return fmt.Errorf("invalid seed size '%d' expecting '%d'", len(seed), ed25519.SeedSize)
	}

	sk := ed25519.NewKeyFromSeed(seed)

	privK, err := crypto.UnmarshalEd25519PrivateKey(sk)
	if err != nil {
		return err
	}

	id, err := peer.Decode(cfg.BridgeID)
	if err != nil {
		return err
	}

	filter := NewGater(id)
	ctx := context.Background()
	host, err := libp2p.New(ctx,
		libp2p.Identity(privK),
		libp2p.ListenAddrStrings("/ip4/0.0.0.0/tcp/14000"),
		libp2p.Ping(false),
		libp2p.DisableRelay(),
		libp2p.ConnectionGater(filter),
	)

	log.Info().Str("Identity", host.ID().Pretty()).Msg("server started")
	if err != nil {
		return err
	}

	ipfs, err := multiaddr.NewMultiaddr(fmt.Sprintf("/ipfs/%s", host.ID().Pretty()))
	if err != nil {
		return err
	}

	for _, addr := range host.Addrs() {
		full := addr.Encapsulate(ipfs)
		log.Info().Str("address", full.String()).Msg("p2p node address")
	}

	_, err = signers.NewServer(host, cfg.Network, cfg.Secret)
	if err != nil {
		return err
	}

	select {}
}

// func NewSigner(config SignerConfig) error {
// 	// var debug bool
// 	var cfg SignerConfig

// 	// flag.BoolVar(&debug, "debug", false, "print debug messages")
// 	// flag.Parse()

// 	// if debug {
// 	// 	zerolog.SetGlobalLevel(zerolog.DebugLevel)
// 	// } else {
// 	// 	zerolog.SetGlobalLevel(zerolog.InfoLevel)
// 	// }

// 	if err := cfg.Valid(); err != nil {
// 		fmt.Println(err)
// 		flag.Usage()
// 		os.Exit(1)
// 	}

// 	if err := app(&cfg); err != nil {
// 		log.Fatal().Err(err).Msg("server exits")
// 		os.Exit(1)
// 	}

// 	return nil
// }
