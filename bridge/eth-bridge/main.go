package main

import (
	"context"
	"os"
	"os/signal"
	"syscall"
	"time"

	flag "github.com/spf13/pflag"
	"github.com/threefoldfoundation/tft-stellar/bridge/eth-bridge/api/bridge"

	"github.com/ethereum/go-ethereum/ethclient"
	"github.com/ethereum/go-ethereum/log"
)

func main() {
	log.Root().SetHandler(log.LvlFilterHandler(log.LvlInfo, log.StreamHandler(os.Stdout, log.TerminalFormat(true))))

	var ethClientUrl string
	var ethPort uint16
	var ethNetworkName string
	var contractAddress string

	var datadir string
	var persistencyFile string

	var accountJSON string
	var accountPass string

	var stellarSecret string
	var stellarNetwork string
	var rescanBridgeAccount bool

	var signers []string
	flag.StringVar(&ethClientUrl, "eth", "https://data-seed-prebsc-1-s1.binance.org:8545", "eth client url")
	flag.Uint16Var(&ethPort, "port", 23111, "eth port")
	flag.StringVar(&ethNetworkName, "ethnetwork", "smart-chain-testnet", "eth network name (defines storage directory name)")
	flag.StringVar(&contractAddress, "contract", "0x770b0AA8b5B4f140cdA2F4d77205ceBe5f3D3C7e", "smart contract address")

	flag.StringVar(&datadir, "datadir", "./storage", "chain data directory")
	flag.StringVar(&persistencyFile, "persistency", "./node.json", "file where last seen blockheight and stellar account cursor is stored")

	flag.StringVar(&accountJSON, "account", "", "ethereum account json")
	flag.StringVar(&accountPass, "password", "", "ethereum account password")

	flag.StringVar(&stellarSecret, "secret", "", "stellar secret")
	flag.StringVar(&stellarNetwork, "network", "testnet", "stellar network url")

	flag.StringArrayVar(&signers, "signer", nil, "list of signers service addresses")
	flag.BoolVar(&rescanBridgeAccount, "rescan", false, "if true is provided, we rescan the bridge stellar account and mint all transactions again")

	flag.Parse()

	ctx := context.Background()
	client, err := ethclient.Dial(ethClientUrl)
	if err != nil {
		panic(err)
	}

	t, cancel := context.WithTimeout(ctx, time.Second*15)
	defer cancel()

	id, err := client.ChainID(t)
	if err != nil {
		panic(err)
	}

	log.Debug("Chain ID %+v", id)

	cnl := make(chan struct{})

	br, err := bridge.NewBridge(ethPort, accountJSON, accountPass, ethNetworkName, nil, contractAddress, datadir, stellarNetwork, stellarSecret, rescanBridgeAccount, persistencyFile, signers)
	if err != nil {
		panic(err)
	}

	err = br.Start(cnl)
	if err != nil {
		panic(err)
	}

	sigs := make(chan os.Signal, 1)
	done := make(chan bool, 1)

	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		sig := <-sigs
		log.Debug("signal %+v", sig)
		done <- true
	}()

	log.Debug("awaiting signal")
	<-done
	err = br.Close()
	if err != nil {
		panic(err)
	}

	time.Sleep(time.Second * 5)
	log.Debug("exiting")
}
