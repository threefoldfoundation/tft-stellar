package eth

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"

	"github.com/ethereum/go-ethereum/p2p/enode"

	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core"
)

//NetworkConfiguration defines the Ethereum network specific configuration needed by the bridge
type NetworkConfiguration struct {
	NetworkID               uint64
	NetworkName             string
	GenesisBlock            *core.Genesis
	ContractAddress         common.Address
	MultisigContractAddress common.Address
	bootnodes               []string
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

var TestnetBootstrapNodes = []string{
	"enode://69a90b35164ef862185d9f4d2c5eff79b92acd1360574c0edf36044055dc766d87285a820233ae5700e11c9ba06ce1cf23c1c68a4556121109776ce2a3990bba@52.199.214.252:30311",
	"enode://330d768f6de90e7825f0ea6fe59611ce9d50712e73547306846a9304663f9912bf1611037f7f90f21606242ded7fb476c7285cb7cd792836b8c0c5ef0365855c@18.181.52.189:30311",
	"enode://df1e8eb59e42cad3c4551b2a53e31a7e55a2fdde1287babd1e94b0836550b489ba16c40932e4dacb16cba346bd442c432265a299c4aca63ee7bb0f832b9f45eb@52.51.80.128:30311",
	"enode://0bd566a7fd136ecd19414a601bfdc530d5de161e3014033951dd603e72b1a8959eb5b70b06c87a5a75cbf45e4055c387d2a842bd6b1bd8b5041b3a61bab615cf@34.242.33.165:30311",
	"enode://604ed87d813c2b884ff1dc3095afeab18331f3cc361e8fb604159e844905dfa6e4c627306231d48f46a2edceffcd069264a89d99cdbf861a04e8d3d8d7282e8a@3.209.122.123:30311",
	"enode://4d358eca87c44230a49ceaca123c89c7e77232aeae745c3a4917e607b909c4a14034b3a742960a378c3f250e0e67391276e80c7beee7770071e13f33a5b0606a@52.72.123.113:30311",
}

var MainnetBootstrapNodes = []string{
	"enode://f3cfd69f2808ef64838abd8786342c0b22fdd28268703c8d6812e26e109f9a7cb2b37bd49724ebb46c233289f22da82991c87345eb9a2dadeddb8f37eeb259ac@18.180.28.21:30311",
	"enode://ae74385270d4afeb953561603fcedc4a0e755a241ffdea31c3f751dc8be5bf29c03bf46e3051d1c8d997c45479a92632020c9a84b96dcb63b2259ec09b4fde38@54.178.30.104:30311",
	"enode://d1cabe083d5fc1da9b510889188f06dab891935294e4569df759fc2c4d684b3b4982051b84a9a078512202ad947f9240adc5b6abea5320fb9a736d2f6751c52e@54.238.28.14:30311",
	"enode://f420209bac5324326c116d38d83edfa2256c4101a27cd3e7f9b8287dc8526900f4137e915df6806986b28bc79b1e66679b544a1c515a95ede86f4d809bd65dab@54.178.62.117:30311",
	"enode://c0e8d1abd27c3c13ca879e16f34c12ffee936a7e5d7b7fb6f1af5cc75c6fad704e5667c7bbf7826fcb200d22b9bf86395271b0f76c21e63ad9a388ed548d4c90@54.65.247.12:30311",
	"enode://f1b49b1cf536e36f9a56730f7a0ece899e5efb344eec2fdca3a335465bc4f619b98121f4a5032a1218fa8b69a5488d1ec48afe2abda073280beec296b104db31@13.114.199.41:30311",
	"enode://4924583cfb262b6e333969c86eab8da009b3f7d165cc9ad326914f576c575741e71dc6e64a830e833c25e8c45b906364e58e70cdf043651fd583082ea7db5e3b@18.180.17.171:30311",
	"enode://4d041250eb4f05ab55af184a01aed1a71d241a94a03a5b86f4e32659e1ab1e144be919890682d4afb5e7afd837146ce584d61a38837553d95a7de1f28ea4513a@54.178.99.222:30311",
	"enode://b5772a14fdaeebf4c1924e73c923bdf11c35240a6da7b9e5ec0e6cbb95e78327690b90e8ab0ea5270debc8834454b98eca34cc2a19817f5972498648a6959a3a@54.170.158.102:30311",
	"enode://f329176b187cec87b327f82e78b6ece3102a0f7c89b92a5312e1674062c6e89f785f55fb1b167e369d71c66b0548994c6035c6d85849eccb434d4d9e0c489cdd@34.253.94.130:30311",
	"enode://cbfd1219940d4e312ad94108e7fa3bc34c4c22081d6f334a2e7b36bb28928b56879924cf0353ad85fa5b2f3d5033bbe8ad5371feae9c2088214184be301ed658@54.75.11.3:30311",
	"enode://c64b0a0c619c03c220ea0d7cac754931f967665f9e148b92d2e46761ad9180f5eb5aaef48dfc230d8db8f8c16d2265a3d5407b06bedcd5f0f5a22c2f51c2e69f@54.216.208.163:30311",
	"enode://352a361a9240d4d23bb6fab19cc6dc5a5fc6921abf19de65afe13f1802780aecd67c8c09d8c89043ff86947f171d98ab06906ef616d58e718067e02abea0dda9@79.125.105.65:30311",
	"enode://bb683ef5d03db7d945d6f84b88e5b98920b70aecc22abed8c00d6db621f784e4280e5813d12694c7a091543064456ad9789980766f3f1feb38906cf7255c33d6@54.195.127.237:30311",
	"enode://11dc6fea50630b68a9289055d6b0fb0e22fb5048a3f4e4efd741a7ab09dd79e78d383efc052089e516f0a0f3eacdd5d3ffbe5279b36ecc42ad7cd1f2767fdbdb@46.137.182.25:30311",
	"enode://21530e423b42aed17d7eef67882ebb23357db4f8b10c94d4c71191f52955d97dc13eec03cfeff0fe3a1c89c955e81a6970c09689d21ecbec2142b26b7e759c45@54.216.119.18:30311",
	"enode://d61a31410c365e7fcd50e24d56a77d2d9741d4a57b295cc5070189ad90d0ec749d113b4b0432c6d795eb36597efce88d12ca45e645ec51b3a2144e1c1c41b66a@34.204.129.242:30311",
	"enode://bb91215b1d77c892897048dd58f709f02aacb5355aa8f50f00b67c879c3dffd7eef5b5a152ac46cdfb255295bec4d06701a8032456703c6b604a4686d388ea8f@75.101.197.198:30311",
	"enode://786acbdf5a3cf91b99047a0fd8305e11e54d96ea3a72b1527050d3d6f8c9fc0278ff9ef56f3e56b3b70a283d97c309065506ea2fc3eb9b62477fd014a3ec1a96@107.23.90.162:30311",
	"enode://4653bc7c235c3480968e5e81d91123bc67626f35c207ae4acab89347db675a627784c5982431300c02f547a7d33558718f7795e848d547a327abb111eac73636@54.144.170.236:30311",
	"enode://c6ffd994c4ef130f90f8ee2fc08c1b0f02a6e9b12152092bf5a03dd7af9fd33597d4b2e2000a271cc0648d5e55242aeadd6d5061bb2e596372655ba0722cc704@54.147.151.108:30311",
	"enode://99b07e9dc5f204263b87243146743399b2bd60c98f68d1239a3461d09087e6c417e40f1106fa606ccf54159feabdddb4e7f367559b349a6511e66e525de4906e@54.81.225.170:30311",
	"enode://1479af5ea7bda822e8747d0b967309bced22cad5083b93bc6f4e1d7da7be067cd8495dc4c5a71579f2da8d9068f0c43ad6933d2b335a545b4ae49a846122b261@52.7.247.132:30311",
}

var ethNetworkConfigurations = map[string]NetworkConfiguration{
	"smart-chain-mainnet": {
		56,
		"main",
		GetMainnetGenesisBlock(),
		//Todo: replace with actual address
		common.HexToAddress("0x21826CC49B92029553af86F4e7A62C427E61e53a"),
		common.HexToAddress("0x8a511F1C6C94B051A6CFCF0FdC83e7FA37CF687F"),
		MainnetBootstrapNodes,
	},
	"smart-chain-testnet": {
		97,
		"bsc-testnet",
		GetTestnetGenesisBlock(),
		common.HexToAddress("0xDAD7A460EA562e28fB90cF524B62ea4cBc1685af"),
		common.HexToAddress("0x8a511F1C6C94B051A6CFCF0FdC83e7FA37CF687F"),
		TestnetBootstrapNodes,
	},
}

//GetEthNetworkConfiguration returns the EthNetworkConAfiguration for a specific network
func GetEthNetworkConfiguration(networkname string) (networkconfig NetworkConfiguration, err error) {
	fmt.Println(networkname)
	networkconfig, found := ethNetworkConfigurations[networkname]
	if !found {
		err = fmt.Errorf("Ethereum network %s not supported", networkname)
	}
	return
}

func GetTestnetGenesisBlock() *core.Genesis {
	genesis := &core.Genesis{}
	f, err := os.Open("./genesis/testnet-genesis.json")
	if err != nil {
		panic(err)
	}
	if err := json.NewDecoder(f).Decode(genesis); err != nil {
		panic(err)
	}

	return genesis
}

func GetMainnetGenesisBlock() *core.Genesis {
	genesis := &core.Genesis{}
	f, err := os.Open("./genesis/mainnet-genesis.json")
	if err != nil {
		panic(err)
	}
	if err := json.NewDecoder(f).Decode(genesis); err != nil {
		panic(err)
	}

	return genesis
}
