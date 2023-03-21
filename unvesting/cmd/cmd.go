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

	rootCmd = &cobra.Command{Use: "unvesting", Short: "A tool for signing unvesting transactions"}

	signCmd = &cobra.Command{
		Use:   "sign",
		Short: "Sign unvesting transactions",
		Args:  cobra.MatchAll(cobra.ExactArgs(0), cobra.OnlyValidArgs),

		RunE: func(cmd *cobra.Command, args []string) error {
			return sign(secret, transactionsFilePath, signaturesOutFilePath)
		},
	}

	aggregateCmd = &cobra.Command{
		Use:   "aggregate",
		Short: "aggregate signatures into xdrs",
		Args:  cobra.MatchAll(cobra.ExactArgs(0), cobra.OnlyValidArgs),

		RunE: func(cmd *cobra.Command, args []string) error {
			return aggregateSignatures(transactionsFilePath, signaturesDirPath, xdrsOutFilePath)
		},
	}
)

func Execute() {
	signCmd.Flags().StringVar(&secret, "secret", "", "Stellar secret")
	signCmd.MarkFlagRequired("secret")
	signCmd.Flags().StringVar(&transactionsFilePath, "path", "./unvesting_transactions.txt", "Transactions to sign file")
	signCmd.Flags().StringVar(&signaturesOutFilePath, "out", "", "File where signatures are stored")

	aggregateCmd.Flags().StringVar(&transactionsFilePath, "path", "unvesting_transactions.txt", "Transactions to sign file")
	aggregateCmd.Flags().StringVar(&signaturesDirPath, "dir", "", "dirpath where signatures were collected")
	aggregateCmd.MarkFlagRequired("dir")
	aggregateCmd.Flags().StringVar(&xdrsOutFilePath, "out", "final.txt", "file where final xdrs are kept")

	viper.BindPFlag("secret", signCmd.Flags().Lookup("secret"))

	rootCmd.AddCommand(signCmd)
	rootCmd.AddCommand(aggregateCmd)

	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
