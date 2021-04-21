package bridge

import (
	"context"
	"encoding/hex"
	"fmt"
	"math/big"
	"sync"

	ethtypes "github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/log"
	"github.com/libp2p/go-libp2p-core/host"
	"github.com/stellar/go/keypair"
)

const (
	// EthBlockDelay is the amount of blocks to wait before
	// pushing eth transaction to the tfchain network
	EthBlockDelay = 3
)

// Bridge is a high lvl structure which listens on contract events and bridge-related
// tfchain transactions, and handles them
type Bridge struct {
	bridgeContract   *BridgeContract
	wallet           *stellarWallet
	blockPersistency *ChainPersistency
	signers          []string
	mut              sync.Mutex
	config           *BridgeConfig
	host             host.Host
}

type BridgeConfig struct {
	EthNetworkName          string
	Bootnodes               []string
	ContractAddress         string
	MultisigContractAddress string
	EthPort                 uint16
	AccountJSON             string
	AccountPass             string
	Datadir                 string
	StellarNetwork          string
	StellarSeed             string
	StellarFeeWallet        string
	RescanBridgeAccount     bool
	PersistencyFile         string
	Signers                 []string
	Follower                bool
	BridgeID                string // needed for followers only
	SignerPort              uint16 // also only needed for followers
}

// NewBridge creates a new Bridge.
func NewBridge(config *BridgeConfig, host host.Host) (*Bridge, error) {
	contract, err := NewBridgeContract(config)
	if err != nil {
		return nil, err
	}

	blockPersistency, err := initPersist(config.PersistencyFile)
	if err != nil {
		return nil, err
	}

	client := NewSignersClient(host, config.Signers)

	w := &stellarWallet{
		network:   config.StellarNetwork,
		client:    client,
		feeWallet: config.StellarFeeWallet,
	}

	if config.StellarSeed != "" {
		w.keypair, err = keypair.ParseFull(config.StellarSeed)

		if err != nil {
			return nil, err
		}
	}
	log.Info(fmt.Sprintf("Stellar bridge account %s loaded on Stellar network %s", w.keypair.Address(), config.StellarNetwork))

	if config.RescanBridgeAccount {
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
		signers:          config.Signers,
		config:           config,
		host:             host,
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

// Start the main processing loop of the bridge
func (bridge *Bridge) Start(ctx context.Context) error {
	heads := make(chan *ethtypes.Header)

	go bridge.bridgeContract.Loop(heads)

	// subscribing to these events is not needed for operational purposes, but might be nice to get some info
	go bridge.bridgeContract.SubscribeTransfers()
	go bridge.bridgeContract.SubscribeMint()

	// Channel where withdrawal events are stored
	// Should only be read from by the master bridge
	withdrawChan := make(chan WithdrawEvent)

	// Channel where sumbission events from the multisig contract are stored
	// Should only be read from by the follower bridges, this event channel
	// will indicate when they need to confirm the withdrawal transaction that is submitted
	submissionChan := make(chan SubmissionEvent)

	// Only the bridge running as the master bridge should do the following things:
	// - Monitor the Bridge Stellar account and initiate Minting transactions accordingly
	// - Monitor the Contract for Withdrawal events and initiate a Withdrawal transaction accordingly
	if !bridge.config.Follower {
		// Monitor the bridge wallet for incoming transactions
		// mint transactions on ERC20 if possible
		go bridge.wallet.MonitorBridgeAndMint(bridge.mint, bridge.blockPersistency)

		height, err := bridge.blockPersistency.GetHeight()
		if err != nil {
			return err
		}
		var lastHeight uint64
		if height.LastHeight > EthBlockDelay {
			lastHeight = height.LastHeight - EthBlockDelay
		}
		go bridge.bridgeContract.SubscribeWithdraw(withdrawChan, lastHeight)
	} else {
		go bridge.bridgeContract.SubscribeSubmission(submissionChan)
	}

	go func() {
		txMap := make(map[string]WithdrawEvent)
		for {
			select {
			// Remember new withdraws
			case we := <-withdrawChan:
				log.Info("Remembering withdraw event", "txHash", we.TxHash(), "height", we.BlockHeight())
				txMap[we.txHash.String()] = we
			// If we get a new head, check every withdraw we have to see if it has matured
			case submission := <-submissionChan:
				log.Info("Submission Event seen", "txid", submission.TransactionId())
				err := bridge.bridgeContract.ConfirmTransaction(submission.TransactionId())
				if err != nil {
					log.Error("error occured during confirming transaction")
				}
			case head := <-heads:
				bridge.mut.Lock()
				ids := make([]string, 0, len(txMap))
				for id := range txMap {
					ids = append(ids, id)
				}

				for _, id := range ids {
					we := txMap[id]
					if head.Number.Uint64() >= we.blockHeight+EthBlockDelay {
						log.Info("Attempting to create an ERC20 withdraw tx", "ethTx", we.TxHash())

						err := bridge.wallet.CreateAndSubmitPayment(ctx, we.blockchain_address, we.network, we.amount.Uint64())
						if err != nil {
							log.Error(fmt.Sprintf("failed to create payment for withdrawal to %s, %s", we.blockchain_address, err.Error()))
						}
						// forget about our tx
						delete(txMap, id)
					}
				}

				err := bridge.blockPersistency.saveHeight(head.Number.Uint64())
				if err != nil {
					log.Error("error occured saving blockheight", "error", err)
				}

				bridge.mut.Unlock()
			case <-ctx.Done():
				return
			}
		}
	}()

	return nil
}
