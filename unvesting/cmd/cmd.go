package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var (
	secret                string
	transactionsFilePath  string
	signaturesOutFilePath string
	signaturesDirPath     string
	xdrsOutFilePath       string
	stellarNetwork        string

	rootCmd = &cobra.Command{Use: "unvesting", Short: "A tool for signing unvesting transactions"}

	signCmd = &cobra.Command{
		Use:   "sign",
		Short: "Sign unvesting transactions",
		Args:  cobra.MatchAll(cobra.ExactArgs(0), cobra.OnlyValidArgs),

		RunE: func(cmd *cobra.Command, args []string) error {
			return sign(secret, stellarNetwork, transactionsFilePath, signaturesOutFilePath)
		},
	}

	aggregateCmd = &cobra.Command{
		Use:   "aggregate",
		Short: "aggregate signatures into xdrs",
		Args:  cobra.MatchAll(cobra.ExactArgs(0), cobra.OnlyValidArgs),

		RunE: func(cmd *cobra.Command, args []string) error {
			return aggregateSignatures(transactionsFilePath, stellarNetwork, signaturesDirPath, xdrsOutFilePath)
		},
	}
)

func Execute() {
	signCmd.Flags().StringVar(&secret, "secret", "", "Stellar secret")
	signCmd.MarkFlagRequired("secret")
	signCmd.Flags().StringVar(&transactionsFilePath, "path", "./unvesting_transactions.txt", "Transactions to sign file")
	signCmd.Flags().StringVar(&signaturesOutFilePath, "out", "", "File where signatures are stored")
	signCmd.Flags().StringVar(&stellarNetwork, "network", "main", "Stellar network [test, main]")

	aggregateCmd.Flags().StringVar(&transactionsFilePath, "path", "unvesting_transactions.txt", "Transactions to sign file")
	aggregateCmd.Flags().StringVar(&signaturesDirPath, "dir", "", "dirpath where signatures were collected")
	aggregateCmd.MarkFlagRequired("dir")
	aggregateCmd.Flags().StringVar(&xdrsOutFilePath, "out", "signed_unvesting_transactions.txt", "file where final xdrs are kept")
	aggregateCmd.Flags().StringVar(&stellarNetwork, "network", "prod", "Stellar network [test, prod]")

	viper.BindPFlag("secret", signCmd.Flags().Lookup("secret"))

	rootCmd.AddCommand(signCmd)
	rootCmd.AddCommand(aggregateCmd)

	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
