package main

import (
	"context"
	"os"
	"os/signal"
	"syscall"
	"time"

	flag "github.com/spf13/pflag"
	"github.com/threefoldfoundation/tft-stellar/eth-bridge/api/bridge"

	"github.com/ethereum/go-ethereum/ethclient"
	"github.com/ethereum/go-ethereum/log"
)

func main() {
	log.Root().SetHandler(log.LvlFilterHandler(log.LvlInfo, log.StreamHandler(os.Stdout, log.TerminalFormat(true))))

	var ethClientUrl string
	var port uint16

	var bridgeCfg bridge.BridgeConfig
	flag.StringVar(&ethClientUrl, "eth", "https://data-seed-prebsc-1-s1.binance.org:8545", "eth client url")
	flag.Uint16Var(&port, "port", 23111, "eth port")
	flag.StringVar(&bridgeCfg.EthNetworkName, "ethnetwork", "smart-chain-testnet", "eth network name (defines storage directory name)")
	flag.StringVar(&bridgeCfg.ContractAddress, "contract", "0x770b0AA8b5B4f140cdA2F4d77205ceBe5f3D3C7e", "smart contract address")
	flag.StringVar(&bridgeCfg.MultisigContractAddress, "mscontract", "0x8a511F1C6C94B051A6CFCF0FdC83e7FA37CF687F", "multisig smart contract address")

	flag.StringVar(&bridgeCfg.Datadir, "datadir", "./storage", "chain data directory")
	flag.StringVar(&bridgeCfg.PersistencyFile, "persistency", "./node.json", "file where last seen blockheight and stellar account cursor is stored")

	flag.StringVar(&bridgeCfg.AccountJSON, "account", "", "ethereum account json")
	flag.StringVar(&bridgeCfg.AccountPass, "password", "", "ethereum account password")

	flag.StringVar(&bridgeCfg.StellarSeed, "secret", "", "stellar secret")
	flag.StringVar(&bridgeCfg.StellarNetwork, "network", "testnet", "stellar network url")

	flag.StringArrayVar(&bridgeCfg.Signers, "signer", nil, "list of signers service addresses")
	flag.BoolVar(&bridgeCfg.RescanBridgeAccount, "rescan", false, "if true is provided, we rescan the bridge stellar account and mint all transactions again")

	flag.BoolVar(&bridgeCfg.Follower, "follower", false, "if true then the bridge will run in follower mode meaning that it will not submit mint transactions to the multisig contract, if false the bridge will also submit transactions")

	var cfg bridge.SignerConfig
	flag.StringVar(&cfg.BridgeID, "bridge", "", "bridge p2p identity as provided by the bridge. Only connections with that ID will be accepted")
	cfg.Secret = bridgeCfg.StellarSeed
	cfg.Network = bridgeCfg.StellarNetwork

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

	log.Debug("Chain ID %+v \n", id)

	cnl := make(chan struct{})

	bridgeCfg.Port = int(port)
	br, err := bridge.NewBridge(&bridgeCfg)
	if err != nil {
		panic(err)
	}

	err = br.Start(cnl)
	if err != nil {
		panic(err)
	}

	err = bridge.NewSigner(&cfg)
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
