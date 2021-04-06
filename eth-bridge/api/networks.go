package eth

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"

	"github.com/ethereum/go-ethereum/p2p/enode"

	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core"
	"github.com/ethereum/go-ethereum/params"
)

//NetworkConfiguration defines the Ethereum network specific configuration needed by the bridge
type NetworkConfiguration struct {
	NetworkID       uint64
	NetworkName     string
	GenesisBlock    *core.Genesis
	ContractAddress common.Address
	bootnodes       []string
}

//GetBootnodes returns the bootnodes for the specific network as  slice of *discv5.Node
// The default bootnodes can be overridden by passing a non nil or empty bootnodes parameter
func (config NetworkConfiguration) GetBootnodes(bootnodes []string) ([]*enode.Node, error) {
	if bootnodes == nil || len(bootnodes) == 0 {
		bootnodes = config.bootnodes
	}
	var nodes []*enode.Node
	for _, boot := range bootnodes {
		if url, err := enode.ParseV4(boot); err == nil {
			nodes = append(nodes, url)
		} else {
			err = errors.New("Failed to parse bootnode URL" + "url" + boot + "err" + err.Error())
			return nil, err
		}
	}
	return nodes, nil
}

var BootstrapNodes = []string{
	"enode://69a90b35164ef862185d9f4d2c5eff79b92acd1360574c0edf36044055dc766d87285a820233ae5700e11c9ba06ce1cf23c1c68a4556121109776ce2a3990bba@52.199.214.252:30311",
	"enode://330d768f6de90e7825f0ea6fe59611ce9d50712e73547306846a9304663f9912bf1611037f7f90f21606242ded7fb476c7285cb7cd792836b8c0c5ef0365855c@18.181.52.189:30311",
	"enode://df1e8eb59e42cad3c4551b2a53e31a7e55a2fdde1287babd1e94b0836550b489ba16c40932e4dacb16cba346bd442c432265a299c4aca63ee7bb0f832b9f45eb@52.51.80.128:30311",
	"enode://0bd566a7fd136ecd19414a601bfdc530d5de161e3014033951dd603e72b1a8959eb5b70b06c87a5a75cbf45e4055c387d2a842bd6b1bd8b5041b3a61bab615cf@34.242.33.165:30311",
	"enode://604ed87d813c2b884ff1dc3095afeab18331f3cc361e8fb604159e844905dfa6e4c627306231d48f46a2edceffcd069264a89d99cdbf861a04e8d3d8d7282e8a@3.209.122.123:30311",
	"enode://4d358eca87c44230a49ceaca123c89c7e77232aeae745c3a4917e607b909c4a14034b3a742960a378c3f250e0e67391276e80c7beee7770071e13f33a5b0606a@52.72.123.113:30311",
}

var ethNetworkConfigurations = map[string]NetworkConfiguration{
	"main": {
		1,
		"main",
		core.DefaultGenesisBlock(),
		//Todo: replace with actual address
		common.HexToAddress("0x21826CC49B92029553af86F4e7A62C427E61e53a"),
		params.MainnetBootnodes,
	},
	"smart-chain-testnet": {
		97,
		"bsc-testnet",
		GetTestnetGenesisBlock(),
		common.HexToAddress("0xDAD7A460EA562e28fB90cF524B62ea4cBc1685af"),
		BootstrapNodes,
	},
}

//GetEthNetworkConfiguration returns the EthNetworkConAfiguration for a specific network
func GetEthNetworkConfiguration(networkname string) (networkconfig NetworkConfiguration, err error) {
	networkconfig, found := ethNetworkConfigurations[networkname]
	if !found {
		err = fmt.Errorf("Ethereum network %s not supported", networkname)
	}
	return
}

func GetTestnetGenesisBlock() *core.Genesis {
	genesis := &core.Genesis{}
	f, err := os.Open("./genesis.json")
	if err != nil {
		panic(err)
	}
	if err := json.NewDecoder(f).Decode(genesis); err != nil {
		panic(err)
	}

	return genesis
}
