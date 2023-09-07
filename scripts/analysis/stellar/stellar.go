package main

import "github.com/stellar/go/txnbuild"

func isTFTorTFTA(asset txnbuild.Asset) bool {
	return (asset.GetCode() == "TFT" && asset.GetIssuer() == "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47") ||
		(asset.GetCode() == "TFTA" && asset.GetIssuer() == "GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2")
}

func getLiquidityPool(liquidityPoolID string) (err error) {
	return
}
