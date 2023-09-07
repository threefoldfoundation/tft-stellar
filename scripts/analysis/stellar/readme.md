# Stellar TFT transaction ingestion

`stellartxs` table

| Column          | |
| --------------- | - |
| transaction     |  |
| from            | sending address |
| amount          | stored as text |
| to              | reveiving address |
| timestamp       | time in unix time |
| type            | payment, trade |

## Go instead of Python

While the rest of the analysis ingestion programs is written Python, the ingestion of TFT Stellar transactions is written in Go as the Python sdk gives errors on loading certain transactions from an envelope xdr.

## Ingestion

Compile/run `main.go`. The program uses the addresses from the [minted table](../readme.md#minted-tokens-on-stellar) to start from so make sure that table is populated properly.

## Remarks

- Trades are not listed in the transactions, will have to use `trades for account` to list them, Arbitragetraders using pathpayments never have a TFT trustline and do massive amounts of trades.

- We have to list all transactions as not everything are payments and trades (like adding/removing from liquidity pools).

- Addresses that got TFT by only buying from liquidity pools are not included at the moment

- claimable balances are ignored at the moment ( an already claimed claimable balance can not be searched for bt id in horizon)

## Support tables

`stellartxcursor` holds a stellar address and the last paging token for `Transactions for Account` requests.
