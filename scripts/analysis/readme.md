# Analysis of TFT

## Concept

In order to perform some basic analysis on TFT, data is gathered in an sqlite database. One can then add custom data and perform sql queries to retreive the desired information.

## Available data

The data is available in the tft_data.db sqlite database.

### Rivine closing

`rivine` table:

| Column          | |
| --------------- | - |
| rivineaddress   | Address |
| locktransaction | Transaction that locked the address |
| free            | spendable TFT at the time of locking |
| locked          | Timelocked TFT at the time of locking |
| total           | = free + locked |
| stellaraddress  | If migrated, the corresponding address on Stellar |

#### Data collection

Originally TFT had a custom blockchain built with Rivine. The data is still available and an explorer hosted at <https://explorer2.threefoldtoken.com>.

Before the migration to Stellar the accounts on the Rivine blockchain were locked so no further transactions transferring TFT could occur.

The `conversion/lockedaddresses.py` script finds these lock transactions and prints them with the address that was locked. The output is available at `conversion/deauthorizations.txt`.

The `conversion/tfchainbalances.py` script collects the balance on rivine of the locked addresses. It's being output to  `conversion/deauthorizedbalances.txt`.

The `rivineclosing.py` script combines it in the `rivine` table.

To add the `stellaraddress` column, run the `migrationaddresses.py` script after the `issuertxs.py` script from the next steps.

### Rivine transaction data

`rivinetxs` table

| Column          | |
| --------------- | - |
| transaction     |  |
| from            | sending address |
| amount          | stored as text |
| to              | reveiving address |
| timestamp       | time in unix time |
| type            | payment, minerfee, txfee, farming |
| farmingproof    | in case of farming |

`from` is empty if the type is minerfee or farmed. The genesis transaction(a2ee0aa706c9de46ec57dbba1af8d352fbcc3cc5e9626fc56337fd5e9ca44c8d) has initial TFT's so the `from` is empty there too.

`to` is empty if the type is txfee.

The remainder of the used inputs are sent back to the sender, hence there are payments from addresses to itself.

The `rivinetransactions.py` script populates this data from the rivine explorer.

### TFTA to TFT conversions

When sending TFTA to it's issuer, the tokens are destroyed  and the same amount of TFT is minted and sent to the address that that sent the TFTA.

The TFTA destruction transactions can be found in the `tftadestruction` table.

| Column          | |
| --------------- | - |
| transaction   |  |
| amount            |  |

### Minted tokens on Stellar

`minted` table

| Column          | |
| --------------- | - |
| transaction   |  |
| token | TFT or TFTA |
| amount            | stored as text |
| to          | Stellar address the tokens are sent to |
| memo           |  |

The memo can be

1. a locktransaction on rivine in which case the mint is triggered by a Rivine to stellar migration. Locktransactions can be found in the `rivine` table.
2. a TFTA destruction transaction in which case the mint is triggered by a TFTA to TFT conversion. These transactions can be found in the `tftadestruction` table.
3. the hash of a farming proof in which case the mint is a result of farming.

There is 1 transaction which is not included in this table as it has no hash memo. This was when setting up TFT on Stellar. The transaction is a mint of 5,000,000 TFT: 3066f15facf63818a82e051b6ce1026d54dc3c5f12c2eb4ed817f155c041da3a. These 5,000,000 TFT were later destroyed in transaction 5a102f493cf31eeea1b281d6076411208e780bd16fc01550a485f249e899d5aa which has the minting transaction as memo to show the link.

### Data collection of tftadestruction and minted

These tables are created by the `issuertxs.py` script that queries the Stellar network for all transactions on the TFT and TFTA issuer accounts.

### Special accounts

`specialaccounts` table

| Column          |
| --------------- |
| chain           |
| address         |
| name            |
| description     |
