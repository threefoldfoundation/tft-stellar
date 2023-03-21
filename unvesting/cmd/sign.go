package cmd

import (
	"bufio"
	"encoding/base64"
	"fmt"
	"os"

	"github.com/pkg/errors"
	"github.com/stellar/go/keypair"
	"github.com/stellar/go/txnbuild"
)

func sign(secret, stellarNetwork, transactionsFilePath, out string) error {
	kp, err := keypair.ParseFull(secret)
	if err != nil {
		return errors.Wrap(err, "invalid stellar secret")
	}

	sNetwork, err := getStellarNetwork(stellarNetwork)
	if err != nil {
		return err
	}

	if out == "" {
		out = fmt.Sprintf("%s.txt", kp.Address())
	}

	signatures := []string{}

	err = HandleFile(transactionsFilePath, func(xdr string) error {
		tx, err := txnbuild.TransactionFromXDR(xdr)
		if err != nil {
			return err
		}

		transaction, ok := tx.Transaction()
		if !ok {
			return errors.New("failed to build transactions")
		}

		signedTx, _ := transaction.Sign(sNetwork, kp)

		signatures = append(signatures, base64.StdEncoding.EncodeToString(signedTx.Signatures()[0].Signature))

		return nil
	})
	if err != nil {
		return errors.Wrap(err, "failed to handle signing")
	}

	file, err := os.OpenFile(out, os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return fmt.Errorf("failed to create out file: %w", err)
	}

	datawriter := bufio.NewWriter(file)

	for _, sig := range signatures {
		_, _ = datawriter.WriteString(fmt.Sprintf("%s,%s", kp.Address(), sig) + "\n")
	}

	datawriter.Flush()
	file.Close()

	fmt.Printf("\nsigned transactions can be found at: %s\n \nSend this file back to Rob!\n", out)

	return nil
}
