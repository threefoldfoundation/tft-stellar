# unlock transaction store testscripts

`curl -v -H "Content-Type: application/json" -d '{ "args": { "unlockhash": "TBRWRROFJZ7XITHGYCNI2TMVGSATRAUE5LY2KPBV2RIAVMXUDMTA3APV","transaction_xdr":"AAAAAOZagjJNeF2pQReStULsfSDHk6WoYTloVY7NBq8AbbgsAAAAZAAMY10AAAADAAAAAQAAAABedOIYAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAFAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAAAAAAAAAAAAAAAAAABAG24LAAAAEDPghy9Oq3+WYK0wTYnj3gyFwYqRzkDxkBWLdQAG8ykZxY+CMLBpz4tW6/M+ctInZNdVu6dzrajSC4mrlBY5uoM"  }}' "https://testnet.threefold.io/threefoldfoundation/unlock_service/create_unlockhash_transaction"`

`curl -v -H "Content-Type: application/json" -d '{ "args": { "unlockhash": "TBRWRROFJZ7XITHGYCNI2TMVGSATRAUE5LY2KPBV2RIAVMXUDMTA3APV" }}' "https://testnet.threefold.io/threefoldfoundation/unlock_service/get_unlockhash_transaction"`
