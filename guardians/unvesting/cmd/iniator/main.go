package main

import (
	"context"
	"flag"
	"log"
	"time"

	"github.com/threefoldfoundation/tft-stellar/guardians/unvesting/communication"
)

func main() {
	var network string

	flag.StringVar(&network, "network", "public", "The stellar network to use: 'public' or 'test'")

	flag.Parse()

	log.Println("Starting iniator on the", network, "network")
	rootCtx, cancel := context.WithCancel(context.Background())
	defer cancel()

	connMgr := communication.NewConnectionManager()
	communicationCtx, cancel := context.WithCancel(rootCtx)
	defer cancel()
	connMgr.Start(communicationCtx, nil)
	for {
		time.Sleep(time.Second * 10)
	}
}
