package signer

import (
	"context"
	"log"

	gorpc "github.com/libp2p/go-libp2p-gorpc"
	protocol "github.com/libp2p/go-libp2p-protocol"
)

const ProtocolID = protocol.ID("/tft/guardians/unvesting/1.0.0")

var signerAddresses = map[string][]string{
	"test": {
		"GB7Y3ZZVJ323L4ET35BAV6TYY76ANDMS75D5XQNPYJETMRPUM62VC7BN",
		// "GCNQJSFACL2OOGDEBLPL4MFN7IS34RRH6YXZ7UZPSANJWWM6X67DGQXP",
		// "GCN2ZZHY7PSXMHZYNYTK6O3TZSCSF2IAL4NH3QNXH2SCBXPVSWKAIY4Q",
		// "GDUTZUYHLB5RYJSTWCBFTVBSOTCIXYZCZ2PTUMDFD3D2UIMZKRCOXG6R",
		// "GAFHS5SEW3Y6BUX3FJ5OTVYP56BESVI3PNNKYNZPX2C5KTCXCZFHSADS",
		// "GD2O7XG7CNLAKGZRQBMLOO3GRF3QVQF4ZPWO6ZC2V47WXXWQXEKSQWHQ",
		// "GCHOZZFLIHA2T7YYSMUQU7CFKP2TQVL4WO75DGZLQBD7HGLT4D6Y3LC6",
		// "GDLGTUQQOEY5IG2ZXIUYEJSU34BNRI43VJJNDSBPVMNYVHM2O4E72FGI",
		// "GBUYN7WTS6VZG3JOHETOXXA7DVWVSO5SJBJOLVPDPIZ633JXIBSSMFBU",
	},
	"public": {
		"GARF35OFGW2XFHFG764UVO2UTUOSDRVL5DU7RXMM7JJJOSVWKK7GATXU",
		"GDORF4CKQ2GDOBXXU7R3EXV3XRN6LFCGNYTHMYXDPZ5NECZ6YZLJGAA2",
		"GDTTKKRECHQMYWJWKQ5UTONRMNK54WRN3PB4U7JZAPUHLPI75ALN7ORU",
		"GDSKTNDAIBUBGQZXEJ64F3P37T7Y45ZOZQCRZY2I46F4UT66KG4JJSOU",
		"GCHUIUY5MOBWOXEKZJEQU2DCUG4WHRXM4KAWCEUQK3NTQGBK5RZ6FQBR",
		"GDTFYNE5MKGFL625FNUQUHILILFNNRSRYAAXADFFLMOOF5E6V5FLLSBG",
		"GDOSJPACWZ2DWSDNNKCVIKMUL3BNVVV3IERJPAZXM3PJMDNXYJIZFUL3",
		"GALQ4TZA6VRBBBBYMM3KSBSXJDLC5A7YIGH4SAS6AJ7N4ZA6P6IHWH43",
		"GDMMVCANURBLP6O64QWJM3L2EZTDSGTFL4B2BNXKAQPWYDX6WNAFNWK4",
	},
}

func GetSignerAddresses(network string) []string {
	return signerAddresses[network]
}

type SigningService struct {
	Network string
}

func NewSigningService(network string) (service SigningService) {
	service = SigningService{
		Network: network,
	}
	return
}

type GetStatusRequest struct{}
type GetStatusReply struct {
	Message string
}

func (s *SigningService) GetStatus(ctx context.Context, r GetStatusRequest, reply *GetStatusReply) (err error) {
	peerID, err := gorpc.GetRequestSender(ctx)
	if err != nil {
		log.Println("Unable to get the request sender:", err)
		err = nil
	} else {
		log.Println("GetStatus request from", peerID)
	}

	reply.Message = "Alive and kicking"
	return
}

type SignArgs struct{}
type SignReply struct{}

func (s *SigningService) Sign(ctx context.Context, r SignArgs, reply *SignReply) (err error) {

	return
}
