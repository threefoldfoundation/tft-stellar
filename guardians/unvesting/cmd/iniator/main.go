package main

import (
	"context"
	"flag"

	"github.com/threefoldfoundation/tft-stellar/guardians/unvesting/communication"
)

func main() {
	var network string

	flag.StringVar(&network, "network", "public", "The stellar network to use: 'public' or 'test'")

	flag.Parse()

	rootCtx, cancel := context.WithCancel(context.Background())
	defer cancel()

	connMgr := communication.NewConnectionManager()
	communicationCtx, cancel := context.WithCancel(rootCtx)
	defer cancel()
	connMgr.Start(communicationCtx, nil)
}
