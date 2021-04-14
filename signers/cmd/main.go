package main

import (
	"context"
	"crypto/ed25519"
	"encoding/hex"
	"flag"
	"fmt"
	"os"
	"time"

	"github.com/libp2p/go-libp2p"
	"github.com/libp2p/go-libp2p-core/crypto"
	"github.com/libp2p/go-libp2p-core/peer"
	"github.com/multiformats/go-multiaddr"
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"github.com/threefoldfoundation/tft-stellar/signers"
)

type Config struct {
	Seed     string
	BridgeID string
}

func (c *Config) Valid() error {
	if c.Seed == "" {
		return fmt.Errorf("seed is required")
	}

	if c.BridgeID == "" {
		return fmt.Errorf("bridge identity is required")
	}

	return nil
}
func app(cfg *Config) error {

	seed, err := hex.DecodeString(cfg.Seed)
	if err != nil {
		return err
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
		log.Info().Str("address", full.String()).Msg("address")
	}

	_, err = signers.NewServer(host, sk)
	if err != nil {
		return err
	}

	select {}
}

func main() {
	log.Logger = log.Output(zerolog.ConsoleWriter{
		TimeFormat: time.RFC3339,
		Out:        os.Stdout,
	})

	var debug bool
	var cfg Config
	flag.StringVar(&cfg.Seed, "seed", "", "seed used for signing and p2p identity")
	flag.StringVar(&cfg.BridgeID, "bridge", "", "bridge p2p identity as provided by the bridge. Only connections with that ID will be accepted")
	flag.BoolVar(&debug, "debug", false, "print debug messages")
	flag.Parse()

	if debug {
		zerolog.SetGlobalLevel(zerolog.DebugLevel)
	} else {
		zerolog.SetGlobalLevel(zerolog.InfoLevel)
	}

	if err := cfg.Valid(); err != nil {
		fmt.Println(err)
		flag.Usage()
		os.Exit(1)
	}

	if err := app(&cfg); err != nil {
		log.Fatal().Err(err).Msg("server exits")
		os.Exit(1)
	}
}
