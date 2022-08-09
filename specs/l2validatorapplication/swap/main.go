package main

import (
	"fmt"
	"log"
	"os"
	"strconv"

	"github.com/stellar/go/clients/horizonclient"
	"github.com/stellar/go/keypair"
	"github.com/stellar/go/network"
	"github.com/stellar/go/protocols/horizon"
	"github.com/stellar/go/txnbuild"
)

const TFTFullAssetString = "TFT:GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47"

func GetStrictReceivePaymentPath(xlmToReceive string) (cost float64, path []horizon.Asset, err error) {
	client := horizonclient.DefaultPublicNetClient
	tftAsset, _ := txnbuild.ParseAssetString(TFTFullAssetString)
	pr := horizonclient.PathsRequest{
		DestinationAssetType: horizonclient.AssetTypeNative,
		SourceAssets:         tftAsset.GetCode() + ":" + tftAsset.GetIssuer(),
		DestinationAmount:    xlmToReceive,
	}
	response, err := client.Paths(pr)
	if err != nil {
		return
	}
	for _, record := range response.Embedded.Records {

		source_amount, err := strconv.ParseFloat(record.SourceAmount, 64)
		if err != nil {
			return 0, nil, err
		}
		if cost == 0.0 || source_amount < cost {
			cost = source_amount
			path = record.Path
		}
	}
	return
}

func SubmitOperation(operation txnbuild.Operation, stellarKP *keypair.Full) (err error) {

	client := horizonclient.DefaultPublicNetClient
	ar := horizonclient.AccountRequest{AccountID: stellarKP.Address()}
	sourceAccount, err := client.AccountDetail(ar)
	if err != nil {
		return
	}
	tx, err := txnbuild.NewTransaction(txnbuild.TransactionParams{
		SourceAccount:        &sourceAccount,
		IncrementSequenceNum: true,
		BaseFee:              1000000,
		Operations:           []txnbuild.Operation{operation},
		Preconditions: txnbuild.Preconditions{
			TimeBounds: txnbuild.NewTimeout(300),
		},
	})
	if err != nil {
		return
	}
	// Sign the transaction
	tx, err = tx.Sign(network.PublicNetworkPassphrase, stellarKP)
	if err != nil {
		return
	}

	// Get the base 64 encoded transaction envelope
	txe, err := tx.Base64()
	if err != nil {
		return
	}

	// Send the transaction to the network
	_, err = client.SubmitTransactionXDR(txe)

	return

}
func main() {

	args := os.Args

	if len(args) != 2 {
		fmt.Println("Usage:", args[0], "account_secret")
		os.Exit(1)
	}
	stellarKP := keypair.MustParseFull(args[1])
	requiredXLM := "1"
	cost, path, err := GetStrictReceivePaymentPath(requiredXLM)
	if err != nil {
		panic(err)
	}
	//Let's add 1 TFT to make sure the the transaction goes through ( the price might already have fluctuated a bit)
	maxTFTtoSpend := cost + 1.0

	txnPath := make(txnbuild.Assets, 0, len(path))
	for _, hpath := range path {
		if hpath.Type == "native" {
			txnPath = append(txnPath, txnbuild.NativeAsset{})
		} else {
			txnPath = append(txnPath, txnbuild.CreditAsset{Code: hpath.Code, Issuer: hpath.Issuer})
		}
	}
	tftAsset, _ := txnbuild.ParseAssetString(TFTFullAssetString)
	op := txnbuild.PathPaymentStrictReceive{
		SendMax:     fmt.Sprintf("%.7f", maxTFTtoSpend),
		SendAsset:   txnbuild.CreditAsset{Code: tftAsset.GetCode(), Issuer: tftAsset.GetIssuer()},
		Destination: stellarKP.Address(),
		DestAsset:   txnbuild.NativeAsset{},
		DestAmount:  requiredXLM,
		Path:        txnPath,
	}

	err = SubmitOperation(&op, stellarKP)
	if err == nil {
		log.Println("Swap executed ")
	} else {
		panic(err)
	}
}
