package main

import (
	"context"
	"crypto/ed25519"
	"encoding/hex"
	"fmt"

	"github.com/libp2p/go-libp2p"
	"github.com/libp2p/go-libp2p-core/crypto"
	"github.com/stellar/go/txnbuild"
	"github.com/threefoldfoundation/tft-stellar/signers"
)

const (
	SeedHex = "27a12a82ffdd17f4174452430a3772e2fa626b3cd88604465a5b8afd7aff00f9"
)

func app(target string) error {
	seed, err := hex.DecodeString(SeedHex)
	if err != nil {
		return err
	}

	sk := ed25519.NewKeyFromSeed(seed)
	identity, err := crypto.UnmarshalEd25519PrivateKey(sk)
	if err != nil {
		return err
	}

	ctx := context.Background()
	host, err := libp2p.New(ctx,
		libp2p.ListenAddrStrings("/ip4/127.0.0.1/tcp/0"),
		libp2p.Identity(identity),
	)
	if err != nil {
		return err
	}

	// the signer must be started with `-bridge <this identity>` to make
	// it accept connections from this bridge
	fmt.Println("Identity: ", host.ID())
	signer := signers.NewSigner(host)

	txnBuild := txnbuild.TransactionParams{
		//Operations:           []txnbuild.Operation{&paymentOP},
		Timebounds: txnbuild.NewTimeout(300),
		//SourceAccount:        &sourceAccount,
		BaseFee:              txnbuild.MinBaseFee,
		IncrementSequenceNum: true,
	}

	tx, err := txnbuild.NewTransaction(txnBuild)
	if err != nil {
		return err
	}
	msg, err := tx.Base64()
	if err != nil {
		return err
	}
	result, err := signer.Sign(ctx, target, msg)
	if err != nil {
		return err
	}

	fmt.Printf("%+v\n", result)
	return nil
}

func main() {
	if err := app("/ip4/192.168.0.143/tcp/14000/p2p/12D3KooWAmsMPqyQX7EpHBTWk728akfGzTeqhAeGMyL35fSxdg3y"); err != nil {
		panic(err)
	}
}
