package cmd

import (
	"bufio"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strings"

	"github.com/pkg/errors"
	"github.com/stellar/go/network"
	"github.com/stellar/go/txnbuild"
)

func aggregateSignatures(transactionsFilePath, dirPath, outfile string) error {
	transactions := []txnbuild.Transaction{}
	err := HandleFile(transactionsFilePath, func(line string) error {
		tx, err := txnbuild.TransactionFromXDR(line)
		if err != nil {
			return err
		}

		transaction, ok := tx.Transaction()
		if !ok {
			return errors.New("failed to build transactions")
		}

		transactions = append(transactions, *transaction)
		return nil
	})
	if err != nil {
		return err
	}

	filepath.WalkDir(dirPath, func(path string, file fs.DirEntry, err error) error {
		if err != nil {
			return err
		}

		if !file.IsDir() {
			// read file
			signatures := []string{}
			err := HandleFile(path, func(line string) error {
				signatures = append(signatures, line)
				return nil
			})
			if err != nil {
				return err
			}

			for i := 0; i <= len(signatures)-1; i++ {
				parts := strings.Split(signatures[i], ",")
				tx, err := transactions[i].AddSignatureBase64(network.PublicNetworkPassphrase, parts[0], parts[1])
				if err != nil {
					return err
				}
				transactions[i] = *tx
			}
		}

		return nil
	})

	file, err := os.OpenFile(outfile, os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return fmt.Errorf("failed to create out file: %w", err)
	}

	datawriter := bufio.NewWriter(file)

	for _, tx := range transactions {
		txBase64, err := tx.Base64()
		if err != nil {
			return err
		}
		_, _ = datawriter.WriteString(fmt.Sprintf("%s %s", tx.SourceAccount().AccountID, txBase64) + "\n")
	}

	datawriter.Flush()
	file.Close()

	fmt.Printf("\nTransactions ready, see: %s\n", outfile)

	return nil
}
