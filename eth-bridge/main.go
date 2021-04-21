package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/multiformats/go-multiaddr"
	flag "github.com/spf13/pflag"
	"github.com/threefoldfoundation/tft-stellar/eth-bridge/api/bridge"

	"github.com/ethereum/go-ethereum/ethclient"
	"github.com/ethereum/go-ethereum/log"
)

func main() {
	log.Root().SetHandler(log.LvlFilterHandler(log.LvlInfo, log.StreamHandler(os.Stdout, log.TerminalFormat(true))))

	var ethClientUrl string
	var bridgeCfg bridge.BridgeConfig
	flag.StringVar(&ethClientUrl, "eth", "https://data-seed-prebsc-1-s1.binance.org:8545", "eth client url")
	flag.Uint16Var(&bridgeCfg.EthPort, "port", 23111, "eth port")
	flag.StringVar(&bridgeCfg.EthNetworkName, "ethnetwork", "smart-chain-testnet", "eth network name (defines storage directory name)")
	flag.StringVar(&bridgeCfg.ContractAddress, "contract", "0x770b0AA8b5B4f140cdA2F4d77205ceBe5f3D3C7e", "smart contract address")
	flag.StringVar(&bridgeCfg.MultisigContractAddress, "mscontract", "0x8a511F1C6C94B051A6CFCF0FdC83e7FA37CF687F", "multisig smart contract address")

	flag.StringVar(&bridgeCfg.Datadir, "datadir", "./storage", "chain data directory")
	flag.StringVar(&bridgeCfg.PersistencyFile, "persistency", "./node.json", "file where last seen blockheight and stellar account cursor is stored")

	flag.StringVar(&bridgeCfg.AccountJSON, "account", "", "ethereum account json")
	flag.StringVar(&bridgeCfg.AccountPass, "password", "", "ethereum account password")

	flag.StringVar(&bridgeCfg.StellarSeed, "secret", "", "stellar secret")
	flag.StringVar(&bridgeCfg.StellarNetwork, "network", "testnet", "stellar network url")
	flag.StringVar(&bridgeCfg.StellarFeeWallet, "feewallet", "", "stellar fee wallet where the fees for each mint transaction will be kept")

	flag.StringArrayVar(&bridgeCfg.Signers, "signer", nil, "list of signers service addresses")
	flag.BoolVar(&bridgeCfg.RescanBridgeAccount, "rescan", false, "if true is provided, we rescan the bridge stellar account and mint all transactions again")

	flag.BoolVar(&bridgeCfg.Follower, "follower", false, "if true then the bridge will run in follower mode meaning that it will not submit mint transactions to the multisig contract, if false the bridge will also submit transactions")

	flag.StringVar(&bridgeCfg.BridgeID, "bridge", "", "bridge p2p identity as provided by the bridge. Only connections with that ID will be accepted")
	flag.Uint16Var(&bridgeCfg.SignerPort, "signer-port", 14000, "signer p2p port")

	flag.Parse()

	//TODO cfg.Validate()

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	client, err := ethclient.Dial(ethClientUrl)
	if err != nil {
		panic(err)
	}

	timeout, timeoutCancel := context.WithTimeout(ctx, time.Second*15)
	defer timeoutCancel()

	id, err := client.ChainID(timeout)
	if err != nil {
		panic(err)
	}

	log.Debug("Chain ID %+v \n", id)

	host, err := bridge.NewHost(bridgeCfg.StellarSeed, bridgeCfg.BridgeID, int(bridgeCfg.SignerPort))
	if err != nil {
		panic(err)
	}

	ipfs, err := multiaddr.NewMultiaddr(fmt.Sprintf("/ipfs/%s", host.ID().Pretty()))
	if err != nil {
		panic(err)
	}

	for _, addr := range host.Addrs() {
		full := addr.Encapsulate(ipfs)
		log.Info("p2p node address", "address", full.String())
	}

	br, err := bridge.NewBridge(&bridgeCfg, host)
	if err != nil {
		panic(err)
	}

	err = br.Start(ctx)
	if err != nil {
		panic(err)
	}

	if bridgeCfg.Follower {
		err = bridge.NewSigner(host, bridgeCfg.StellarNetwork, bridgeCfg.StellarSeed)
		if err != nil {
			panic(err)
		}
	}

	sigs := make(chan os.Signal, 1)

	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)

	log.Info("awaiting signal")
	sig := <-sigs
	log.Info("signal", "signal", sig)
	cancel()
	err = br.Close()
	if err != nil {
		panic(err)
	}

	host.Close()
	log.Info("exiting")
	time.Sleep(time.Second * 5)
}
