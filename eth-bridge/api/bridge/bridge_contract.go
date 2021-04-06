package bridge

import (
	"context"
	"errors"
	"math/big"
	"strings"
	"sync"
	"time"

	"github.com/ethereum/go-ethereum/accounts/abi"
	"github.com/ethereum/go-ethereum/accounts/abi/bind"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/event"
	"github.com/ethereum/go-ethereum/log"
	"github.com/stellar/go/clients/horizonclient"
	hProtocol "github.com/stellar/go/protocols/horizon"
	"github.com/stellar/go/protocols/horizon/effects"
	"github.com/stellar/go/protocols/horizon/operations"

	tfeth "github.com/threefoldtech/eth-bridge/api"
	"github.com/threefoldtech/eth-bridge/api/bridge/contract"
)

const ERC20AddressLength = 20

type ERC20Address [ERC20AddressLength]byte

var (
	ether = new(big.Int).Exp(big.NewInt(10), big.NewInt(18), nil)
)

const (
	// retryDelay is the delay to retry calls when there are no peers
	retryDelay = time.Second * 15
)

// BridgeContract exposes a higher lvl api for specific contract bindings. In case of proxy contracts,
// the bridge needs to use the bindings of the implementation contract, but the address of the proxy.
type BridgeContract struct {
	networkConfig tfeth.NetworkConfiguration // Ethereum network
	networkName   string

	lc *LightClient

	filter     *contract.TokenFilterer
	transactor *contract.TokenTransactor
	caller     *contract.TokenCaller

	contract *bind.BoundContract
	abi      abi.ABI

	// cache some stats in case they might be usefull
	head    *types.Header // Current head header of the bridge
	balance *big.Int      // The current balance of the bridge (note: ethers only!)
	nonce   uint64        // Current pending nonce of the bridge
	price   *big.Int      // Current gas price to issue funds with

	lock sync.RWMutex // Lock protecting the bridge's internals
}

// GetContractAdress returns the address of this contract
func (bridge *BridgeContract) GetContractAdress() common.Address {
	return bridge.networkConfig.ContractAddress
}

// NewBridgeContract creates a new wrapper for an allready deployed contract
func NewBridgeContract(networkName string, bootnodes []string, contractAddress string, port int, accountJSON, accountPass string, datadir string, cancel <-chan struct{}, stellarNetwork string, stellarSeed string) (*BridgeContract, error) {
	// load correct network config
	networkConfig, err := tfeth.GetEthNetworkConfiguration(networkName)
	if err != nil {
		return nil, err
	}
	// override contract address if it's provided
	if contractAddress != "" {
		networkConfig.ContractAddress = common.HexToAddress(contractAddress)
		// TODO: validate ABI of contract,
		//       see https://github.com/threefoldtech/rivine-extension-erc20/issues/3
	}

	bootstrapNodes, err := networkConfig.GetBootnodes(bootnodes)
	if err != nil {
		return nil, err
	}
	lc, err := NewLightClient(LightClientConfig{
		Port:           port,
		DataDir:        datadir,
		BootstrapNodes: bootstrapNodes,
		NetworkName:    networkConfig.NetworkName,
		NetworkID:      networkConfig.NetworkID,
		GenesisBlock:   networkConfig.GenesisBlock,
	})
	if err != nil {
		return nil, err
	}
	err = lc.LoadAccount(accountJSON, accountPass)
	if err != nil {
		return nil, err
	}

	filter, err := contract.NewTokenFilterer(networkConfig.ContractAddress, lc.Client)
	if err != nil {
		return nil, err
	}

	transactor, err := contract.NewTokenTransactor(networkConfig.ContractAddress, lc.Client)
	if err != nil {
		return nil, err
	}

	caller, err := contract.NewTokenCaller(networkConfig.ContractAddress, lc.Client)
	if err != nil {
		return nil, err
	}

	contract, abi, err := bindTTFT20(networkConfig.ContractAddress, lc.Client, lc.Client, lc.Client)
	if err != nil {
		return nil, err
	}

	return &BridgeContract{
		networkName:   networkName,
		networkConfig: networkConfig,
		lc:            lc,
		filter:        filter,
		transactor:    transactor,
		caller:        caller,
		contract:      contract,
		abi:           abi,
	}, nil
}

// Close terminates the Ethereum connection and tears down the stack.
func (bridge *BridgeContract) Close() error {
	return bridge.lc.Close()
}

// AccountAddress returns the account address of the bridge contract
func (bridge *BridgeContract) AccountAddress() (common.Address, error) {
	return bridge.lc.AccountAddress()
}

// LightClient returns the LightClient driving this bridge contract
func (bridge *BridgeContract) LightClient() *LightClient {
	return bridge.lc
}

// ABI returns the parsed and bound ABI driving this bridge contract
func (bridge *BridgeContract) ABI() abi.ABI {
	return bridge.abi
}

// Refresh attempts to retrieve the latest header from the chain and extract the
// associated bridge balance and nonce for connectivity caching.
func (bridge *BridgeContract) Refresh(head *types.Header) error {
	// Ensure a state update does not run for too long
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	// If no header was specified, use the current chain head
	var err error
	if head == nil {
		if head, err = bridge.lc.HeaderByNumber(ctx, nil); err != nil {
			return err
		}
	}
	// Retrieve the balance, nonce and gas price from the current head
	var (
		nonce   uint64
		price   *big.Int
		balance *big.Int
	)
	if price, err = bridge.lc.SuggestGasPrice(ctx); err != nil {
		return err
	}
	if balance, err = bridge.lc.AccountBalanceAt(ctx, head.Number); err != nil {
		return err
	}
	log.Debug(bridge.lc.account.account.Address.Hex())
	// Everything succeeded, update the cached stats
	bridge.lock.Lock()
	bridge.head, bridge.balance = head, balance
	bridge.price, bridge.nonce = price, nonce
	bridge.lock.Unlock()
	return nil
}

// Loop subscribes to new eth heads. If a new head is received, it is passed on the given channel,
// after which the internal stats are updated if no update is already in progress
func (bridge *BridgeContract) Loop(ch chan<- *types.Header) {
	log.Debug("Subscribing to eth headers")
	// channel to receive head updates from client on
	heads := make(chan *types.Header, 16)
	// subscribe to head upates
	sub, err := bridge.lc.SubscribeNewHead(context.Background(), heads)
	if err != nil {
		log.Error("Failed to subscribe to head events", "err", err)
	}
	defer sub.Unsubscribe()
	// channel so we can update the internal state from the heads
	update := make(chan *types.Header)
	go func() {
		for head := range update {
			// old heads should be ignored during a chain sync after some downtime
			if err := bridge.Refresh(head); err != nil {
				log.Warn("Failed to update state", "block", head.Number, "err", err)
			}
			log.Debug("Internal stats updated", "block", head.Number, "account balance", bridge.balance, "gas price", bridge.price, "nonce", bridge.nonce)
		}
	}()
	for head := range heads {
		ch <- head
		select {
		// only process new head if another isn't being processed yet
		case update <- head:
			log.Debug("Processing new head")
		default:
			log.Debug("Ignoring current head, update already in progress")
		}
	}
	log.Error("Bridge state update loop ended")
}

// SubscribeTransfers subscribes to new Transfer events on the given contract. This call blocks
// and prints out info about any transfer as it happened
func (bridge *BridgeContract) SubscribeTransfers() error {
	sink := make(chan *contract.TokenTransfer)
	opts := &bind.WatchOpts{Context: context.Background(), Start: nil}
	sub, err := bridge.filter.WatchTransfer(opts, sink, nil, nil)
	if err != nil {
		return err
	}
	defer sub.Unsubscribe()
	for {
		select {
		case err = <-sub.Err():
			return err
		case transfer := <-sink:
			log.Debug("Noticed transfer event", "from", transfer.From, "to", transfer.To, "amount", transfer.Tokens)
		}
	}
}

// SubscribeMint subscribes to new Mint events on the given contract. This call blocks
// and prints out info about any mint as it happened
func (bridge *BridgeContract) SubscribeMint() error {
	sink := make(chan *contract.TokenMint)
	opts := &bind.WatchOpts{Context: context.Background(), Start: nil}
	sub, err := bridge.filter.WatchMint(opts, sink, nil, nil)
	if err != nil {
		return err
	}
	defer sub.Unsubscribe()
	for {
		select {
		case err = <-sub.Err():
			return err
		case mint := <-sink:
			log.Info("Noticed mint event", "receiver", mint.Receiver, "amount", mint.Tokens, "TFT tx id", mint.Txid)
		}
	}
}

// WithdrawEvent holds relevant information about a withdraw event
type WithdrawEvent struct {
	receiver           common.Address
	amount             *big.Int
	blockchain_address string
	network            string
	txHash             common.Hash
	blockHash          common.Hash
	blockHeight        uint64
	raw                []byte
}

// Receiver of the withdraw
func (w WithdrawEvent) Receiver() common.Address {
	return w.receiver
}

// Amount withdrawn
func (w WithdrawEvent) Amount() *big.Int {
	return w.amount
}

// Blockchain address to withdraw to
func (w WithdrawEvent) BlockchainAddress() string {
	return w.blockchain_address
}

// Network to withdraw to
func (w WithdrawEvent) Network() string {
	return w.network
}

// TxHash hash of the transaction
func (w WithdrawEvent) TxHash() common.Hash {
	return w.txHash
}

// BlockHash of the containing block
func (w WithdrawEvent) BlockHash() common.Hash {
	return w.blockHash
}

// BlockHeight of the containing block
func (w WithdrawEvent) BlockHeight() uint64 {
	return w.blockHeight
}

// SubscribeWithdraw subscribes to new Withdraw events on the given contract. This call blocks
// and prints out info about any withdraw as it happened
func (bridge *BridgeContract) SubscribeWithdraw(wc chan<- WithdrawEvent, startHeight uint64) error {
	log.Debug("Subscribing to withdraw events", "start height", startHeight)
	sink := make(chan *contract.TokenWithdraw)
	watchOpts := &bind.WatchOpts{Context: context.Background(), Start: nil}
	sub, err := bridge.WatchWithdraw(watchOpts, sink, nil)
	if err != nil {
		log.Error("Subscribing to withdraw events failed", "err", err)
		return err
	}
	defer sub.Unsubscribe()
	for {
		select {
		case err = <-sub.Err():
			return err
		case withdraw := <-sink:

			if withdraw.Raw.Removed {
				// ignore removed events
				continue
			}
			log.Debug("Noticed withdraw event", "receiver", withdraw.Receiver, "amount", withdraw.Tokens)
			wc <- WithdrawEvent{
				receiver:           withdraw.Receiver,
				amount:             withdraw.Tokens,
				txHash:             withdraw.Raw.TxHash,
				blockHash:          withdraw.Raw.BlockHash,
				blockHeight:        withdraw.Raw.BlockNumber,
				blockchain_address: withdraw.BlockchainAddress,
				network:            withdraw.Network,
				raw:                withdraw.Raw.Data,
			}
		}
	}
}

// WatchWithdraw is a free log subscription operation binding the contract event 0x884edad9ce6fa2440d8a54cc123490eb96d2768479d49ff9c7366125a9424364.
//
// Solidity: e Withdraw(receiver indexed address, tokens uint256)
//
// This method is copied from the generated bindings and slightly modified, so we can add logic to stay backwards compatible with the old withdraw event signature
func (bridge *BridgeContract) WatchWithdraw(opts *bind.WatchOpts, sink chan<- *contract.TokenWithdraw, receiver []common.Address) (event.Subscription, error) {

	var receiverRule []interface{}
	for _, receiverItem := range receiver {
		receiverRule = append(receiverRule, receiverItem)
	}

	logs, sub, err := bridge.contract.WatchLogs(opts, "Withdraw", receiverRule)
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(contract.TokenWithdraw)
				if err := bridge.contract.UnpackLog(event, "Withdraw", log); err != nil {
					return err
				}
				event.Raw = log

				select {
				case sink <- event:
				case err := <-sub.Err():
					return err
				case <-quit:
					return nil
				}
			case err := <-sub.Err():
				return err
			case <-quit:
				return nil
			}
		}
	}), nil
}

// TransferFunds transfers funds from one address to another
func (bridge *BridgeContract) TransferFunds(recipient common.Address, amount *big.Int) error {
	err := bridge.transferFunds(recipient, amount)
	for IsNoPeerErr(err) {
		time.Sleep(retryDelay)
		err = bridge.transferFunds(recipient, amount)
	}
	return err
}

func (bridge *BridgeContract) transferFunds(recipient common.Address, amount *big.Int) error {
	if amount == nil {
		return errors.New("invalid amount")
	}
	accountAddress, err := bridge.lc.AccountAddress()
	if err != nil {
		return err
	}
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*30)
	defer cancel()
	opts := &bind.TransactOpts{
		Context: ctx, From: accountAddress,
		Signer: bridge.getSignerFunc(),
		Value:  nil, Nonce: nil, GasLimit: 0, GasPrice: nil,
	}
	_, err = bridge.transactor.Transfer(opts, recipient, amount)
	return err
}

func (bridge *BridgeContract) Mint(receiver ERC20Address, amount *big.Int, txID string) error {
	err := bridge.mint(receiver, amount, txID)
	for IsNoPeerErr(err) {
		time.Sleep(retryDelay)
		err = bridge.mint(receiver, amount, txID)
	}
	return err
}

func (bridge *BridgeContract) mint(receiver ERC20Address, amount *big.Int, txID string) error {
	log.Debug("Calling mint function in contract")
	if amount == nil {
		return errors.New("invalid amount")
	}
	accountAddress, err := bridge.lc.AccountAddress()
	if err != nil {
		return err
	}

	// TODO estimate gas more correctly ..
	gas, err := bridge.lc.SuggestGasPrice(context.Background())
	if err != nil {
		return err
	}
	newGas := big.NewInt(10 * gas.Int64())

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*30)
	defer cancel()
	opts := &bind.TransactOpts{
		Context: ctx, From: accountAddress,
		Signer: bridge.getSignerFunc(),
		Value:  nil, Nonce: nil, GasLimit: 100000, GasPrice: newGas,
	}
	_, err = bridge.transactor.MintTokens(opts, common.Address(receiver), amount, txID)
	return err
}

func (bridge *BridgeContract) IsMintTxID(txID string) (bool, error) {
	res, err := bridge.isMintTxID(txID)
	for IsNoPeerErr(err) {
		time.Sleep(retryDelay)
		res, err = bridge.isMintTxID(txID)
	}
	return res, err
}

func (bridge *BridgeContract) isMintTxID(txID string) (bool, error) {
	log.Debug("Calling isMintID")
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*30)
	defer cancel()
	opts := &bind.CallOpts{Context: ctx}
	return bridge.caller.IsMintID(opts, txID)
}

func (bridge *BridgeContract) getSignerFunc() bind.SignerFn {
	return func(signer types.Signer, address common.Address, tx *types.Transaction) (*types.Transaction, error) {
		accountAddress, err := bridge.lc.AccountAddress()
		if err != nil {
			return nil, err
		}
		if address != accountAddress {
			return nil, errors.New("not authorized to sign this account")
		}
		networkID := int64(bridge.networkConfig.NetworkID)
		return bridge.lc.SignTx(tx, big.NewInt(networkID))
	}
}

func (bridge *BridgeContract) TokenBalance(address common.Address) (*big.Int, error) {
	log.Debug("Calling TokenBalance function in contract")
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*30)
	defer cancel()
	opts := &bind.CallOpts{Context: ctx}
	return bridge.caller.BalanceOf(opts, common.Address(address))
}

func (bridge *BridgeContract) EthBalance() (*big.Int, error) {
	err := bridge.Refresh(nil) // force a refresh
	return bridge.balance, err
}

// bindTTFT20 binds a generic wrapper to an already deployed contract.
//
// This method is copied from the generated bindings as a convenient way to get a *bind.Contract, as this is needed to implement the WatchWithdraw function ourselves
func bindTTFT20(address common.Address, caller bind.ContractCaller, transactor bind.ContractTransactor, filterer bind.ContractFilterer) (*bind.BoundContract, abi.ABI, error) {
	parsed, err := abi.JSON(strings.NewReader(contract.TokenABI))
	if err != nil {
		return nil, parsed, err
	}
	return bind.NewBoundContract(address, parsed, caller, transactor, filterer), parsed, nil
}

// GetHorizonClient gets the horizon client based on the wallet's network
func (b *BridgeContract) GetHorizonClient() (*horizonclient.Client, error) {
	switch b.networkName {
	case "smart-chain-testnet":
		return horizonclient.DefaultTestNetClient, nil
	case "main":
		return horizonclient.DefaultPublicNetClient, nil
	default:
		return nil, errors.New("network is not supported")
	}
}

func (b *BridgeContract) StreamStellarAccountPayments(ctx context.Context, accountID string, handler func(op operations.Operation)) error {
	client, err := b.GetHorizonClient()
	if err != nil {
		return err
	}

	opRequest := horizonclient.OperationRequest{
		ForAccount: accountID,
	}

	return client.StreamPayments(ctx, opRequest, handler)
}

func (b *BridgeContract) StreamStellarAccountTransactions(ctx context.Context, accountID string, handler func(op hProtocol.Transaction)) error {
	client, err := b.GetHorizonClient()
	if err != nil {
		return err
	}

	opRequest := horizonclient.TransactionRequest{
		ForAccount: accountID,
	}

	return client.StreamTransactions(ctx, opRequest, handler)
}

func (b *BridgeContract) GetTransactionEffects(txHash string) (effects effects.EffectsPage, err error) {
	client, err := b.GetHorizonClient()
	if err != nil {
		return effects, err
	}

	effectsReq := horizonclient.EffectRequest{
		ForTransaction: txHash,
	}
	effects, err = client.Effects(effectsReq)
	if err != nil {
		return effects, err
	}

	return effects, nil
}
