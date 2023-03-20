package cmd

import (
	"bufio"
	"fmt"
	"os"
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
