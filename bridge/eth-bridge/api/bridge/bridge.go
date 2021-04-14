package bridge

import (
	"context"
	"crypto/ed25519"
	"encoding/hex"
	"fmt"
	"math/big"
	"path/filepath"
	"sync"

	ethtypes "github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/log"
	"github.com/libp2p/go-libp2p"
	"github.com/libp2p/go-libp2p-core/crypto"
	"github.com/stellar/go/keypair"
	"github.com/stellar/go/strkey"
	"github.com/threefoldfoundation/tft-stellar/bridge/signers"
)

const (
	// EthBlockDelay is the amount of blocks to wait before
	// pushing eth transaction to the tfchain network
	EthBlockDelay = 15
)

// Bridge is a high lvl structure which listens on contract events and bridge-related
// tfchain transactions, and handles them
type Bridge struct {
	bridgeContract   *BridgeContract
	wallet           *stellarWallet
	blockPersistency *ChainPersistency
	mut              sync.Mutex
}

// NewBridge creates a new Bridge.
func NewBridge(ethPort uint16, accountJSON, accountPass string, ethNetworkName string, bootnodes []string, contractAddress string, datadir string, stellarNetwork string, stellarSeed string, rescanBridgeAccount bool, persistencyFile string) (*Bridge, error) {
	contract, err := NewBridgeContract(ethNetworkName, bootnodes, contractAddress, int(ethPort), accountJSON, accountPass, filepath.Join(datadir, "eth"), stellarNetwork, stellarSeed)
	if err != nil {
		return nil, err
	}

	blockPersistency, err := initPersist(persistencyFile)
	if err != nil {
		return nil, err
	}

	w := &stellarWallet{
		network: stellarNetwork,
	}

	if stellarSeed != "" {
		w.keypair, err = keypair.ParseFull(stellarSeed)

		if err != nil {
			return nil, err
		}
	}
	log.Info(fmt.Sprintf("Stellar bridge account %s loaded on Stellar network %s", w.keypair.Address(), stellarNetwork))

	if rescanBridgeAccount {
		// saving the cursor to 1 will trigger the bridge stellar account
		// to scan for every transaction ever made on the bridge account
		// and mint accordingly
		err = blockPersistency.saveStellarCursor("0")
		if err != nil {
			return nil, err
		}
	}

	bridge := &Bridge{
		bridgeContract:   contract,
		blockPersistency: blockPersistency,
		wallet:           w,
	}

	return bridge, nil
}

// Close bridge
func (bridge *Bridge) Close() error {
	bridge.mut.Lock()
	defer bridge.mut.Unlock()
	err := bridge.bridgeContract.Close()
	return err
}

func (bridge *Bridge) mint(receiver ERC20Address, amount *big.Int, txID string) error {
	log.Info(fmt.Sprintf("Minting transaction for %s", hex.EncodeToString(receiver[:])))
	// check if we already know this ID
	known, err := bridge.bridgeContract.IsMintTxID(txID)
	if err != nil {
		return err
	}
	if known {
		log.Info(fmt.Sprintf("Skipping known minting transaction %s", txID))
		// we already know this withdrawal address, so ignore the transaction
		return nil
	}
	return bridge.bridgeContract.Mint(receiver, amount, txID)
}

// GetClient returns bridgecontract lightclient
func (bridge *Bridge) GetClient() *LightClient {
	return bridge.bridgeContract.LightClient()
}

// GetBridgeContract returns this bridge's contract.
func (bridge *Bridge) GetBridgeContract() *BridgeContract {
	return bridge.bridgeContract
}

func (bridge *Bridge) getSignerClient() (*signers.Signer, error) {
	seed, err := strkey.Decode(strkey.VersionByteSeed, bridge.wallet.keypair.Seed())
	if err != nil {
		return nil, err
	}

	if len(seed) != ed25519.SeedSize {
		return nil, fmt.Errorf("invalid seed size '%d' expecting '%d'", len(seed), ed25519.SeedSize)
	}

	sk := ed25519.NewKeyFromSeed(seed)

	privK, err := crypto.UnmarshalEd25519PrivateKey(sk)
	if err != nil {
		return nil, err
	}

	ctx := context.Background()
	host, err := libp2p.New(ctx,
		libp2p.Identity(privK),
		libp2p.ListenAddrStrings("/ip4/127.0.0.1/tcp/0"),
		libp2p.Ping(false),
		libp2p.DisableRelay(),
	)

	return signers.NewSigner(host), nil
}

// Start the main processing loop of the bridge
func (bridge *Bridge) Start(cancel <-chan struct{}) error {
	heads := make(chan *ethtypes.Header)

	go bridge.bridgeContract.Loop(heads)

	// subscribing to these events is not needed for operational purposes, but might be nice to get some info
	go bridge.bridgeContract.SubscribeTransfers()
	go bridge.bridgeContract.SubscribeMint()

	// Monitor the bridge wallet for incoming transactions
	// mint transactions on ERC20 if possible
	go bridge.wallet.MonitorBridgeAndMint(bridge.mint, bridge.blockPersistency)

	withdrawChan := make(chan WithdrawEvent)

	height, err := bridge.blockPersistency.GetHeight()
	if err != nil {
		return err
	}

	var lastHeight uint64
	if height.LastHeight > EthBlockDelay {
		lastHeight = height.LastHeight - EthBlockDelay
	}

	go bridge.bridgeContract.SubscribeWithdraw(withdrawChan, lastHeight)

	go func() {
		txMap := make(map[string]WithdrawEvent)
		for {
			select {
			// Remember new withdraws
			case we := <-withdrawChan:
				log.Info("Remembering withdraw event", "txHash", we.TxHash(), "height", we.BlockHeight())
				txMap[we.txHash.String()] = we
			// If we get a new head, check every withdraw we have to see if it has matured
			case head := <-heads:
				bridge.mut.Lock()
				for id := range txMap {
					we := txMap[id]
					if head.Number.Uint64() >= we.blockHeight+EthBlockDelay {
						log.Info("Attempting to create an ERC20 withdraw tx", "ethTx", we.TxHash())

						err := bridge.wallet.CreateAndSubmitPayment(we.blockchain_address, we.network, we.amount.Uint64())
						if err != nil {
							log.Error(fmt.Sprintf("failed to create payment for withdrawal to %s, %s", we.blockchain_address, err.Error()))
							delete(txMap, id)
							continue
						}
						// forget about our tx
						delete(txMap, id)
					}
				}

				err := bridge.blockPersistency.saveHeight(head.Number.Uint64())
				if err != nil {
					fmt.Println("error occured saving blockheight")
				}

				bridge.mut.Unlock()
			case <-cancel:
				return
			}
		}
	}()

	return nil
}
