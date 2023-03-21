package cmd

import (
	"bufio"
	"errors"
	"fmt"
	"os"

	"github.com/stellar/go/network"
)

type FileHandlerFunc func(line string) error

func HandleFile(path string, fn FileHandlerFunc) error {
	inFile, err := os.Open(path)
	if err != nil {
		fmt.Println(err.Error() + `: ` + path)
		return err
	}
	defer inFile.Close()

	scanner := bufio.NewScanner(inFile)
	for scanner.Scan() {
		fn(scanner.Text())
	}

	return nil
}

func getStellarNetwork(networkstr string) (string, error) {
	if networkstr == "test" {
		return network.TestNetworkPassphrase, nil
	} else if networkstr == "prod" {
		return network.PublicNetworkPassphrase, nil
	}
	return "", errors.New("network not supported")
}
