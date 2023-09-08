package main

import (
	"database/sql"
	"flag"
	"fmt"

	"github.com/stellar/go/txnbuild"
	_ "modernc.org/sqlite"
)

func main() {
	var dbPath string
	var preview bool
	flag.StringVar(&dbPath, "db", "tft_data.db", "Path of the sqlite db")
	flag.BoolVar(&preview, "preview", false, "Print the information instead of storing it in the db")
	flag.Parse()
	db, err := sql.Open("sqlite", dbPath)
	if err != nil {
		panic(err)
	}
	defer db.Close()
	err = createStellarTables(db)
	if err != nil {
		panic(err)
	}
	addressesToAnalyse, err := LoadAddressesToAnalyse(db)
	if err != nil {
		panic(err)
	}
	knownAddresses := addressesToAnalyse
	newAddresses := make(map[string]bool)
	for len(addressesToAnalyse) > 0 {
		for address := range addressesToAnalyse {
			fmt.Println(address)
			cursor, err := loadTransactionCursor(db, address)
			if err != nil {
				panic(err)
			}
			transactions := fetchTransactions(address, cursor)
			for len(transactions) > 0 {
				dbTx, err := db.Begin()
				if err != nil {
					panic(err)
				}
				for _, transaction := range transactions {
					gt, err := txnbuild.TransactionFromXDR(transaction.EnvelopeXdr)
					if err != nil {
						fmt.Println("ERROR loading transaction xdr for transaction", transaction.ID)
					}
					var tx *txnbuild.Transaction
					if feeBumpTx, isFeebump := gt.FeeBump(); isFeebump {
						tx = feeBumpTx.InnerTransaction()
					} else {
						tx, _ = gt.Transaction()
					}
					var textMemo string
					if m, ok := tx.Memo().(*txnbuild.MemoText); ok {
						textMemo = string(*m)
					}
					for _, op := range tx.Operations() {
						if paymentOperation, ok := op.(*txnbuild.Payment); ok {
							if !isTFTorTFTA(paymentOperation.Asset) {
								continue
							}
							if paymentOperation.Destination == address {
								continue //Only consider the sending payments to avoid doubles
							}
							if _, known := knownAddresses[paymentOperation.Destination]; !known {
								newAddresses[paymentOperation.Destination] = true
							}
							if preview {
								fmt.Println(transaction.ID, address, "sent", paymentOperation.Amount, paymentOperation.Asset.GetCode(), "to", paymentOperation.Destination, "with memo", textMemo, "at", transaction.LedgerCloseTime.Unix())
							} else {
								if err = StorePayment(dbTx, transaction.ID, address, paymentOperation.Amount, paymentOperation.Destination, paymentOperation.Asset.GetCode(), textMemo, transaction.LedgerCloseTime.Unix()); err != nil {
									panic(err)
								}
							}
							continue
						} else if _, ok := op.(*txnbuild.SetOptions); ok {
							continue
						} else if _, ok := op.(*txnbuild.ChangeTrust); ok {
							continue
						} else if _, ok := op.(*txnbuild.AccountMerge); ok {
							continue
						} else if _, ok := op.(*txnbuild.CreateAccount); ok {
							continue
						} else if _, ok := op.(*txnbuild.ManageData); ok {
							continue
						} else if _, ok := op.(*txnbuild.BumpSequence); ok {
							continue
						} else if _, ok := op.(*txnbuild.BeginSponsoringFutureReserves); ok {
							continue
						} else if _, ok := op.(*txnbuild.EndSponsoringFutureReserves); ok {
							continue
						} else if _, ok := op.(*txnbuild.RevokeSponsorship); ok {
							continue
						} else if _, ok := op.(*txnbuild.ManageSellOffer); ok {
							continue //TODO has to be handled in getting trades for account
						} else if _, ok := op.(*txnbuild.ManageBuyOffer); ok {
							continue //TODO has to be handled in getting trades for account
						} else if _, ok := op.(*txnbuild.CreateClaimableBalance); ok {
							continue //probably never used, let's see if there are relevant claimable balances claimed
						} else if _, ok := op.(*txnbuild.PathPaymentStrictSend); ok {
							continue //Swap, has to be handled in getting trades for account
							//TODO a rare case where the swap does not incur a trade should be handled
						} else if _, ok := op.(*txnbuild.PathPaymentStrictReceive); ok {
							continue //Swap, has to be handled in getting trades for account
							//TODO a rare case where the swap does not incur a trade should be handled
						} else if _, ok := op.(*txnbuild.ClaimClaimableBalance); ok {
							continue //probably never used
						} else if _, ok := op.(*txnbuild.LiquidityPoolDeposit); ok {
							lp, amount, err := getLiquidityPoolDepositInfo(transaction.ID)
							if err != nil {
								panic(err) // Is recoverable, should retry
							}
							if amount == "" {
								continue
							}
							if preview {
								fmt.Println(transaction.ID, address, "sent", amount, "TFT", "to", lp, "with memo", textMemo, "at", transaction.LedgerCloseTime.Unix())
							} else {
								if err = StorePayment(dbTx, transaction.ID, address, amount, "lp "+lp, "TFT", textMemo, transaction.LedgerCloseTime.Unix()); err != nil {
									panic(err)
								}
							}
							continue

						}
						panic(fmt.Sprintf("Unsupported Operation of type %T", op))

					}
					cursor = transaction.PagingToken()
				}
				if !preview {
					err = storeTransactionCursor(dbTx, address, cursor)
				}
				if err = dbTx.Commit(); err != nil {
					panic(err)
				}
				transactions = fetchTransactions(address, cursor)
			}
		}
		addAddresses(knownAddresses, addressesToAnalyse) //a bit of overhead the first time
		addressesToAnalyse = newAddresses
		newAddresses = make(map[string]bool)
	}

}

func addAddresses(addresses map[string]bool, addressesToAdd map[string]bool) {
	for address := range addressesToAdd {
		addresses[address] = true
	}
}
