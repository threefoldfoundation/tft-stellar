package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"

	"github.com/alecthomas/kong"
	"github.com/stellar/go/clients/horizonclient"
	"github.com/stellar/go/keypair"
	stellarNetwork "github.com/stellar/go/network"
	"github.com/stellar/go/txnbuild"
)

const (
	testnetTransactionFundingUrl    = "https://testnet.threefold.io/threefoldfoundation/transactionfunding_service/fund_transaction"
	productionTransactionFundingUrl = "https://tokenservices.threefold.io/threefoldfoundation/transactionfunding_service/fund_transaction"
)

type Globals struct {
	Network string `default:"testnet" enum:"testnet,public" help:"Stellar network [testnet,public]"`
}

type SendCmd struct {
	Secret      string `arg:"" help:"Secret of an existing Stellar account to send TFT from"`
	Destination string `arg:"" help:"Account to send TFT to"`
}

var cli struct {
	Globals
	Send SendCmd `cmd:""`
}

func (cmd *SendCmd) Run(g Globals) (err error) {
	kp, err := keypair.ParseFull(cmd.Secret)
	if err != nil {
		return
	}
	feeAccount, fee, err := getTFTTransactionFundingCondition(g.Network)
	if err != nil {
		return
	}
	payment := txnbuild.Payment{
		Destination: cmd.Destination,
		Amount:      "2",
		Asset:       getTFTAsset(g.Network),
	}
	feePayment := txnbuild.Payment{
		Destination: feeAccount,
		Amount:      fee,
		Asset:       getTFTAsset(g.Network),
	}
	sourceAccount, err := getHorizonClient(g.Network).AccountDetail(horizonclient.AccountRequest{
		AccountID: kp.Address(),
	})
	if err != nil {
		return
	}
	tx, err := txnbuild.NewTransaction(txnbuild.TransactionParams{
		SourceAccount:        &sourceAccount,
		IncrementSequenceNum: true,
		BaseFee:              0,
		Operations:           []txnbuild.Operation{&payment, &feePayment},
		Preconditions: txnbuild.Preconditions{
			TimeBounds: txnbuild.NewInfiniteTimeout(),
		},
	})
	if err != nil {
		return
	}
	tx, err = tx.Sign(getNetworkPassPhrase(g.Network), kp)
	if err != nil {
		return
	}
	xdr, err := tx.Base64()
	if err != nil {
		return
	}
	fmt.Println("XDR before sending to the trandsaction funding service:", xdr)

	err = fundAndSubmitTransaction(xdr, g.Network)

	return
}

func getNetworkPassPhrase(network string) string {
	if network == "public" {
		return stellarNetwork.PublicNetworkPassphrase
	}
	return stellarNetwork.TestNetworkPassphrase
}

func getTFTTransactionFundingCondition(network string) (feeWallet, fee string, err error) {
	baseUrl := "https://testnet.threefold.io/threefoldfoundation/transactionfunding_service"
	if network == "public" {
		baseUrl = "https://tokenservices.threefold.io/threefoldfoundation/transactionfunding_service"
	}
	resp, err := http.Get(baseUrl + "/conditions")
	if err != nil {
		return
	}
	body, err := ioutil.ReadAll(resp.Body)
	type Condition struct {
		Asset          string
		Fee_account_id string
		Fee_fixed      string
	}
	conditions := make([]Condition, 0)
	json.Unmarshal(body, &conditions)
	tftAsset := getTFTAsset(network)
	tftAssetString := tftAsset.GetCode() + ":" + tftAsset.GetIssuer()
	for _, c := range conditions {
		if c.Asset == tftAssetString {
			feeWallet = c.Fee_account_id
			fee = c.Fee_fixed
			return
		}
	}
	err = errors.New("Transaction funding condition for TFT not found")
	return
}

func fundAndSubmitTransaction(xdr, network string) (err error) {
	url := testnetTransactionFundingUrl
	if network == "public" {
		url = productionTransactionFundingUrl
	}
	binaryPostdata, err := json.Marshal(map[string]string{
		"transaction": xdr,
	})
	if err != nil {
		return
	}
	postDataReader := bytes.NewBuffer(binaryPostdata)

	resp, err := http.Post(url, "application/json", postDataReader)
	if err != nil {
		return
	}
	data := map[string]string{}

	err = json.NewDecoder(resp.Body).Decode(&data)
	if err != nil {
		return
	}
	if errorMsg, errorPresent := data["error"]; errorPresent {
		err = errors.New(errorMsg)
		return
	}

	return
}

func getHorizonClient(network string) *horizonclient.Client {
	if network == "public" {
		return horizonclient.DefaultPublicNetClient
	}
	return horizonclient.DefaultTestNetClient
}

func getTFTAsset(network string) txnbuild.Asset {
	issuer := "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3" //testnet issuer
	if network == "public" {
		issuer = "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47"
	}
	return txnbuild.CreditAsset{
		Code:   "TFT",
		Issuer: issuer,
	}
}

func main() {
	ctx := kong.Parse(&cli)

	ctx.FatalIfErrorf(ctx.Run(cli.Globals))

}
