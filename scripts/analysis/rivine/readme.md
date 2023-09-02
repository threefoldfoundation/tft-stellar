# Rivine transaction data

`rivinetxs` table

| Column          | |
| --------------- | - |
| transaction     |  |
| from | sending adress |
| amount            | stored as text |
| to          |  |
| timestamp       |  time in unix time |
| type            | payment, minerfee, txfee, farming |
| farmingproof    | in case of farming |

`from` is empty if the type is  minerfee or farmed. The genesis transaction(a2ee0aa706c9de46ec57dbba1af8d352fbcc3cc5e9626fc56337fd5e9ca44c8d) has initial TFT's so the `from` is empty there too.

`to` is empty if the type is txfee.

## Optimizations

- The remainder of the used input is sent back to the sender, this can be filtered out

## TODO

- Not all condition types are supported yet, running until encountering a block which fails
