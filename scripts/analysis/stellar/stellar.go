package main

import (
	"fmt"
	"net/http"
	"time"

	"github.com/stellar/go/clients/horizonclient"
	"github.com/stellar/go/protocols/horizon"
	"github.com/stellar/go/protocols/horizon/effects"
	"github.com/stellar/go/txnbuild"
)

func isTFTorTFTA(asset txnbuild.Asset) bool {
	return (asset.GetCode() == "TFT" && asset.GetIssuer() == "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47") ||
		(asset.GetCode() == "TFTA" && asset.GetIssuer() == "GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2")
}

func getLiquidityPoolDepositInfo(transactionID string) (lp string, amount string, err error) {
	effectsReq := horizonclient.EffectRequest{
		ForTransaction: transactionID,
	}
	transactionEffects, err := horizonclient.DefaultPublicNetClient.Effects(effectsReq)
	if err != nil {
		return
	}
	for _, effect := range transactionEffects.Embedded.Records {
		if depositEffect, ok := effect.(effects.LiquidityPoolDeposited); ok {
			assetA := depositEffect.ReservesDeposited[0].Asset
			if assetA == "native" {
				assetA = "XLM"
			}
			assetB := depositEffect.ReservesDeposited[1].Asset
			for _, rd := range depositEffect.ReservesDeposited {
				if rd.Asset == "TFT:GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47" {
					amount = rd.Amount
					lp = fmt.Sprintf("%s/%s", assetA, assetB)
				}
			}
		}
	}
	return
}

func getLiquidityPoolWithdrawInfo(transactionID string) (lp string, amount string, err error) {
	effectsReq := horizonclient.EffectRequest{
		ForTransaction: transactionID,
	}
	transactionEffects, err := horizonclient.DefaultPublicNetClient.Effects(effectsReq)
	if err != nil {
		return
	}
	for _, effect := range transactionEffects.Embedded.Records {
		if withdrawEffect, ok := effect.(effects.LiquidityPoolWithdrew); ok {
			assetA := withdrawEffect.ReservesReceived[0].Asset
			if assetA == "native" {
				assetA = "XLM"
			}
			assetB := withdrawEffect.ReservesReceived[1].Asset
			for _, rd := range withdrawEffect.ReservesReceived {
				if rd.Asset == "TFT:GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47" {
					amount = rd.Amount
					lp = fmt.Sprintf("%s/%s", assetA, assetB)
				}
			}
		}
	}
	return
}
func fetchTransactions(address string, cursor string) (transactions []horizon.Transaction) {
	timeouts := 0
	opRequest := horizonclient.TransactionRequest{
		ForAccount:    address,
		IncludeFailed: false,
		Cursor:        cursor,
		Limit:         100,
	}

	for {

		response, err := horizonclient.DefaultPublicNetClient.Transactions(opRequest)
		if err != nil {
			fmt.Println("Error getting transactions for stellar account", "address", opRequest.ForAccount, "cursor", opRequest.Cursor, "pagelimit", opRequest.Limit, "error", err)
			horizonError, ok := err.(*horizonclient.Error)
			if ok && (horizonError.Response.StatusCode == http.StatusGatewayTimeout || horizonError.Response.StatusCode == http.StatusServiceUnavailable) {
				timeouts++
				if timeouts == 1 {
					opRequest.Limit = 5
				} else if timeouts > 1 {
					opRequest.Limit = 1
				}

				fmt.Println("Request timed out, lowering pagelimit", "pagelimit", opRequest.Limit)
			}
			time.Sleep(5 * time.Second)
			continue
		}
		return response.Embedded.Records

	}

}
